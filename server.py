#!/usr/bin/env python3
"""GRAPHIK ONE — servidor local com API de catalogo e upload."""
from __future__ import annotations

import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from lib.cms import (
    ADMIN_FILE,
    FOLDERS,
    IMG_EXT,
    MAX_UPLOAD,
    ROOT,
    VID_EXT,
    load_admin,
    load_catalog,
    make_token,
    merge_catalog,
    new_recovery_code,
    parse_multipart,
    save_admin,
    save_catalog,
    save_json_file,
    safe_name,
    sha,
    token_ok,
    unique_path,
)

PORT = int(os.environ.get("PORT", "8000"))

for folder in FOLDERS.values():
    (ROOT / folder).mkdir(parents=True, exist_ok=True)
(ROOT / "data").mkdir(exist_ok=True)


def write_recovery_file(code: str) -> None:
    (ROOT / "data" / "RECOVERY.txt").write_text(
        "Codigo de recuperacao do painel GRAPHIK ONE\n"
        "Guarde este codigo. Serve para repor a palavra-passe se a esquecer.\n\n"
        + code
        + "\n",
        encoding="utf-8",
    )


def ensure_admin():
    data = load_admin() or {}
    changed = False
    if not data.get("password"):
        data["password"] = sha("graphikone")
        changed = True
    if not data.get("recovery"):
        code = new_recovery_code()
        data["recovery"] = sha(code)
        data["recoveryPending"] = code
        write_recovery_file(code)
        changed = True
    if changed:
        save_json_file(ADMIN_FILE, data)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _json(self, code: int, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self, limit=MAX_UPLOAD):
        length = int(self.headers.get("Content-Length") or 0)
        if length > limit:
            return None
        return self.rfile.read(length) if length else b""

    def _auth(self) -> bool:
        token = self.headers.get("X-Admin-Token") or ""
        if token_ok(token):
            return True
        self._json(401, {"ok": False, "error": "Nao autenticado."})
        return False

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        blocked = path.lower() in {"/data/admin.json", "/data/recovery.txt"}
        if blocked or path.lower().startswith("/data/admin") or path.lower().endswith("recovery.txt"):
            return self._json(403, {"ok": False, "error": "Acesso negado."})
        if path == "/api/catalog":
            return self._json(200, load_catalog())
        if path == "/api/session":
            token = self.headers.get("X-Admin-Token") or ""
            return self._json(200, {"ok": token_ok(token)})
        return super().do_GET()

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        if path == "/api/login":
            raw = self._read_body(4096)
            try:
                data = json.loads(raw or b"{}")
            except Exception:
                return self._json(400, {"ok": False, "error": "Pedido invalido."})
            admin = load_admin()
            if sha(str(data.get("password") or "")) != admin.get("password"):
                return self._json(401, {"ok": False, "error": "Palavra-passe incorrecta."})
            pending = admin.pop("recoveryPending", None)
            extra = {"ok": True, "token": make_token()}
            if pending:
                save_admin(admin)
                extra["recoveryCode"] = pending
            extra["hasRecovery"] = bool(admin.get("recovery"))
            return self._json(200, extra)

        if path == "/api/logout":
            return self._json(200, {"ok": True})

        if path == "/api/password":
            if not self._auth():
                return
            raw = self._read_body(4096)
            try:
                data = json.loads(raw or b"{}")
            except Exception:
                return self._json(400, {"ok": False, "error": "Pedido invalido."})
            admin = load_admin()
            if sha(str(data.get("current") or "")) != admin.get("password"):
                return self._json(401, {"ok": False, "error": "Palavra-passe actual incorrecta."})
            nxt = str(data.get("next") or "")
            if len(nxt) < 6:
                return self._json(400, {"ok": False, "error": "A nova palavra-passe precisa de 6 caracteres."})
            admin["password"] = sha(nxt)
            save_admin(admin)
            return self._json(200, {"ok": True})

        if path == "/api/recover":
            raw = self._read_body(4096)
            try:
                data = json.loads(raw or b"{}")
            except Exception:
                return self._json(400, {"ok": False, "error": "Pedido invalido."})
            admin = load_admin()
            code = str(data.get("code") or "").strip().upper().replace(" ", "")
            nxt = str(data.get("next") or "")
            stored = str(admin.get("recovery") or "")
            if not stored or sha(code) != stored:
                return self._json(401, {"ok": False, "error": "Codigo de recuperacao incorrecto."})
            if len(nxt) < 6:
                return self._json(400, {"ok": False, "error": "A nova palavra-passe precisa de 6 caracteres."})
            fresh = new_recovery_code()
            admin["password"] = sha(nxt)
            admin["recovery"] = sha(fresh)
            save_admin(admin)
            write_recovery_file(fresh)
            return self._json(200, {"ok": True, "recovery": fresh})

        if path == "/api/recovery":
            if not self._auth():
                return
            admin = load_admin()
            fresh = new_recovery_code()
            admin["recovery"] = sha(fresh)
            save_admin(admin)
            write_recovery_file(fresh)
            return self._json(200, {"ok": True, "code": fresh})

        if path == "/api/upload":
            if not self._auth():
                return
            return self._upload()

        return self._json(404, {"ok": False, "error": "Nao encontrado."})

    def do_PUT(self):
        path = self.path.split("?", 1)[0]
        if path != "/api/catalog":
            return self._json(404, {"ok": False, "error": "Nao encontrado."})
        if not self._auth():
            return
        raw = self._read_body(2 * 1024 * 1024)
        try:
            data = json.loads(raw or b"{}")
        except Exception:
            return self._json(400, {"ok": False, "error": "JSON invalido."})
        if not isinstance(data, dict):
            return self._json(400, {"ok": False, "error": "O catalogo deve ser um objeto."})
        try:
            data = merge_catalog(load_catalog(), data)
            save_catalog(data)
        except ValueError as err:
            return self._json(400, {"ok": False, "error": str(err)})
        return self._json(200, {"ok": True, "updated": data.get("updated")})

    def _upload(self):
        ctype = self.headers.get("Content-Type") or ""
        if "multipart/form-data" not in ctype:
            return self._json(400, {"ok": False, "error": "Use multipart/form-data."})
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_UPLOAD:
            return self._json(413, {"ok": False, "error": "Ficheiro demasiado grande (max 25 MB)."})
        body = self.rfile.read(length)
        folder_key, filename, file_bytes = parse_multipart(ctype, body)
        if not file_bytes:
            return self._json(400, {"ok": False, "error": "Ficheiro em falta."})
        folder_rel = FOLDERS.get(folder_key, "media")
        dest_dir = ROOT / folder_rel
        dest_dir.mkdir(parents=True, exist_ok=True)
        name = safe_name(filename)
        ext = os.path.splitext(name)[1].lower()
        if ext not in IMG_EXT | VID_EXT:
            return self._json(400, {"ok": False, "error": "Tipo de ficheiro nao permitido."})
        dest = unique_path(dest_dir, name)
        dest.write_bytes(file_bytes)
        if ext in IMG_EXT - {".svg", ".gif"}:
            try:
                from PIL import Image
                im = Image.open(dest)
                im = im.convert("RGB")
                w, h = im.size
                scale = min(1.0, 1600 / max(w, h))
                if scale < 1:
                    im = im.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
                out = dest.with_suffix(".jpg") if dest.suffix.lower() != ".jpg" else dest
                im.save(out, "JPEG", quality=80, optimize=True, progressive=True)
                if out != dest and dest.exists():
                    dest.unlink()
                    dest = out
            except Exception:
                pass
        rel = dest.relative_to(ROOT).as_posix()
        return self._json(200, {"ok": True, "path": rel, "size": dest.stat().st_size})

    def end_headers(self):
        if self.path.split("?", 1)[0].startswith("/data/"):
            self.send_header("Cache-Control", "no-store")
        super().end_headers()


def main():
    ensure_admin()
    httpd = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"GRAPHIK ONE a servir em http://localhost:{PORT}", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
