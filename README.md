# GRAPHIK ONE, LDA - Website institucional animado

Website de pagina unica (HTML5 + CSS3 + JavaScript) para a GRAPHIK ONE, LDA
(grafica, serigrafia, bordados e papelaria), em Lichinga, Mocambique.

- Slogan: **"Sua marca, nosso cuidado. Sua ideia, nossa impressao."**
- Objectivo: apresentar a empresa e converter visitantes em pedidos de orcamento
  (formulario, WhatsApp e Messenger).

## Como abrir

Use o servidor incluido (serve o site e a API do painel):

```bash
python3 server.py
```

Depois aceda a `http://localhost:8000`. O painel fica em `http://localhost:8000/admin.html`.

Palavra-passe actual do painel: `admin999` (altere em Seguranca no painel).

## Publicar na Vercel

O site e estatico. O painel (`/admin.html`) usa funcoes Python em `/api`.

```bash
npx vercel
```

Na primeira vez, inicie sessao na Vercel e aceite criar o projecto. Depois:

```bash
npx vercel --prod
```

Para o painel **guardar** alteracoes e uploads na Vercel (o disco do servidor nao persiste):

1. No projecto da Vercel, abra **Storage** e crie um **Blob** (acesso Public).
2. Ligue o Blob ao projecto. Fica a variavel `BLOB_READ_WRITE_TOKEN`.
3. Volte a fazer deploy.

Sem Blob, o site publica na mesma; o catalogo lido e o `data/catalog.json` do deploy, e o Guardar no painel devolve erro ate existir o Blob.

O login do painel na Vercel usa a mesma palavra-passe (hash em `data/admin.json`).

> O Three.js (hero 3D), o GSAP e o Lenis sao carregados por CDN, por isso e
> necessaria ligacao a internet na primeira visita. O site funciona na mesma
> sem essas bibliotecas (tem fallbacks).

## Estrutura de ficheiros

```text
.
├── index.html          Pagina unica (HTML + CSS + JavaScript)
├── admin.html          Painel de administracao (login + CRUD visual)
├── server.py           Servidor local com API de gravacao e upload
├── data/
│   ├── catalog.json    Conteudo editavel (produtos, servicos, videos, empresa)
│   └── admin.json      Palavra-passe do painel (hash)
├── media/
│   ├── logo-horizontal.png        Logotipo a cores, formato horizontal (menu)
│   ├── logo-horizontal-white.png  Logotipo branco horizontal (rodape)
│   ├── logo.png                   Logotipo a cores, formato vertical (preloader)
│   ├── logo-white.png             Logotipo branco vertical
│   ├── logo-mark.png              Simbolo (sem texto) a cores
│   ├── logo-mark-white.png        Simbolo branco (avatar do Facebook)
│   ├── favicon.png / favicon.svg  Icone do separador
│   ├── apple-touch-icon.png       Icone para iOS
│   ├── og-image.jpg               Imagem de partilha (Open Graph)
│   ├── about.jpg                  Imagem da seccao "Sobre nos"
│   ├── products/       Imagens dos produtos (p1.jpg..p12.jpg)
│   ├── works/          Imagens dos trabalhos (w1.jpg..w9.jpg + fb1..fb4)
│   ├── partners/       Logotipos dos parceiros (pt1..pt8)
│   └── video/          Miniaturas (v1.jpg..v3.jpg) e videos demo (demo1..demo3.mp4)
└── README.md
```

As fotografias de produtos, trabalhos, "Sobre nos" e as miniaturas/videos demo
foram obtidas de bancos de imagens e video de **uso livre** (Pixabay e Coverr,
licencas que permitem uso comercial). Sao imagens de apoio: substitua-as pelas
fotos e videos reais da empresa mantendo os mesmos nomes de ficheiro. Os
logotipos dos parceiros (`media/partners/pt1..pt8.svg`) continuam genericos, a
substituir pelos logotipos reais de cada parceiro.

## Onde trocar conteudos

### 1. Dados da empresa (telefones, e-mail, Facebook, horario)

Procure no fim do `index.html` o bloco `const CONFIG = { ... }`.
Altere apenas aqui:

```javascript
const CONFIG = {
  whatsapp: '258861104897',   // sem + nem espacos
  phones: ['+258861104897', '+258848831243'],
  phoneSecondary: '+258860740240',
  email: 'graphikonelda@gmail.com',
  facebookPage: 'https://www.facebook.com/profile.php?id=61585165623463',
  messenger: 'https://m.me/61585165623463',
  timezone: 'Africa/Maputo',
  address: 'Av. do Trabalho, Predio 24 ...',
  mapsQuery: 'Lichinga Av do Trabalho Predio 24',
  catalogUrl: 'data/catalog.json',
  form: { provider: 'formspree', endpoint: '', emailjs: {}, subject: '...' },
  analytics: { ga4: '' },             // ex.: 'G-XXXXXXXXXX'
  social: { facebookPlugin: true, instagram: '' },
  hours: { /* minutos desde a meia-noite; 0 = Domingo */ }
};
```

Os contactos tambem aparecem escritos na seccao **Contacto** e no **Rodape**.
Se trocar de numero, atualize esses textos nos mesmos locais (procure por
`861104897`).

### 2. Painel de administracao

Abra `admin.html` (precisa do `server.py` a correr). Entre com a palavra-passe
`graphikone` e altere:

- Empresa: contactos, morada, textos e foto de Sobre nos
- Servicos: titulos, descricoes e listas
- Produtos, trabalhos, videos e parceiros (adicionar, remover, trocar foto/video)
- Horario de funcionamento
- Palavra-passe do painel

Clique **Guardar alteracoes** e recarregue o site. Os ficheiros vao para
`media/` e o conteudo fica em `data/catalog.json`.

Estrutura de cada item:

```javascript
// produto / trabalho
{ "img": "media/products/p1.jpg", "name": "Cartazes e Banners",
  "nameEn": "Posters and Banners", "cat": "grafica" }

// parceiro
{ "img": "media/partners/pt1.svg", "url": "https://site-do-parceiro.mz" }
```

- `cat` so aceita: `grafica`, `serigrafia` ou `papelaria`.
- `nameEn` e opcional mas recomendado: e o nome mostrado na versao inglesa.
- Se o JSON falhar ou estiver ausente, o site usa as listas de recurso
  `PRODUCTS`, `WORKS` e `PARTNERS` embutidas no `index.html` (nada quebra).
- Os cartoes de produto passam a ter o botao **Pedir orcamento**, que
  pre-preenche o formulario com o produto e o servico correspondente.
- A galeria masonry continua com lightbox (setas, teclado, swipe e zoom) e
  inclui o botao **Pedir orcamento** para o trabalho aberto.

### 3. Versao bilingue (PT / EN)

O site tem um seletor **PT / EN** no menu e no menu mobile. A escolha fica
guardada em `localStorage` e pode ser forcada por URL (`?lang=en`).

- Textos fixos: dicionario `I18N_EN` (e `I18N_ATTR_EN` para `placeholder`,
  `aria-label`, `title` e `alt`), no bloco de JavaScript.
- Nomes de produtos/trabalhos: campo `nameEn` no catalogo.
- Meta titulo/descricao e `<html lang>` sao trocados automaticamente.

Para traduzir um texto novo, acrescente a entrada com a mesma grafia do texto
portugues (sem acentos no codigo, tal como no HTML).

### 4. Formulario (Formspree / EmailJS)

O formulario funciona em tres modos, configurados em `CONFIG.form`:

```javascript
form: {
  provider: 'formspree',            // 'formspree' | 'emailjs' | 'none'
  endpoint: '',                     // Formspree: https://formspree.io/f/SEU-ID
  emailjs: { publicKey: '', serviceId: '', templateId: '' },
  subject: 'Novo pedido de orcamento - site GRAPHIK ONE'
}
```

- **Formspree:** crie um formulario em formspree.io e cole o endpoint.
- **EmailJS:** crie a conta, o servico e o template, e preencha as tres chaves.
- **none / vazio:** o site abre o WhatsApp com a mensagem ja preenchida.

O formulario tem _honeypot_ antispam (`_gotcha`), validacao em tempo real e
estados de envio (a enviar, sucesso, erro). Os botoes **WhatsApp** e **E-mail**
continuam disponiveis como alternativa.

Pre-preenchimento: qualquer botao de produto, o botao do lightbox e o URL
`?produto=Cartoes%20de%20Visita` (aceita nome PT ou EN) preenchem o campo
oculto `produto`, a categoria e a mensagem.

### 5. Redes sociais (Facebook + Instagram)

- **Feed automatico:** usa o Page Plugin oficial do Facebook (iframe, sem chave
  de API). Ativa/desativa em `CONFIG.social.facebookPlugin`.
- **Destaques:** grelha fixa de publicacoes (troque o `href` de cada
  `<a class="fb-post">` pelo link real).
- **Instagram:** defina `CONFIG.social.instagram` com o perfil publico (ex.:
  `'graphikone'`) para ativar o separador e o embed. Vazio = desativado.

### 6. Google Analytics e consentimento

Defina `CONFIG.analytics.ga4` com o ID GA4 (ex.: `'G-XXXXXXXXXX'`). Com o valor
vazio nada e carregado. Quando definido, aparece um aviso de cookies; o GA4 so
e carregado depois de **Aceitar** (a escolha fica em `localStorage`).

Eventos enviados: `language_change`, `select_product`, `generate_lead`.

### 7. Google Business Profile

O bloco JSON-LD `LocalBusiness` no `<head>` ja descreve nome, morada,
coordenadas, telefones, horario e Facebook. Para aparecer no Google Maps:

1. Crie/valide a ficha em business.google.com com o mesmo nome e morada.
2. Use a mesma morada e telefones do site (coerencia NAP).
3. Associe o dominio `https://graphikone.co.mz/` a ficha.
4. O mapa embutido usa `CONFIG.mapsQuery`; ajuste se a localizacao exata mudar.

### 8. Videos

Cada cartao usa `data-video="media/video/demo1.mp4"` (os ficheiros `demo1.mp4`,
`demo2.mp4` e `demo3.mp4` ja existem, de uso livre/Coverr). Coloque os videos
reais nessa pasta e atualize o atributo. A miniatura e a imagem `<img>` do cartao
(`media/video/v1.jpg`..`v3.jpg`). Se trocar a miniatura, substitua o ficheiro
mantendo o nome.

### 9. Links do Facebook

Na seccao "Siga a Graphik One":
- Botoes "Seguir" e "Enviar mensagem": substitua
  `https://www.facebook.com/profile.php?id=61585165623463` e
  `https://m.me/61585165623463`.
- Cartoes de publicacoes/fotos/reels: troque o `href` de cada `<a class="fb-post">`
  pelo link real da publicacao.

### 10. Logotipo

O logotipo real foi aplicado a partir do ficheiro original. Foram criadas estas
variantes (todas em `media/`):

| Ficheiro | Uso |
| --- | --- |
| `logo-horizontal.png` | Menu (navbar) |
| `logo-horizontal-white.png` | Rodape |
| `logo.png` | Preloader |
| `logo-white.png` | Versao branca vertical (disponivel) |
| `logo-mark.png` | Simbolo a cores (uso avulso) |
| `logo-mark-white.png` | Avatar do bloco de Facebook |
| `favicon.png` / `favicon.svg` | Icone do separador |
| `apple-touch-icon.png` | Icone iOS |
| `og-image.jpg` | Imagem de partilha (Open Graph) |

Para trocar o logotipo, substitua os ficheiros por versoes com o mesmo nome
(mantenha fundo transparente nos PNG). O simbolo tambem aparece no selo rotativo
do hero (SVG embutido no HTML); se a forma do simbolo mudar, atualize esse bloco.

Cores de referencia do logotipo: magenta #FF208C, roxo #AB3ADE, laranja #FF8A1F,
amarelo/ambar #FDB405, sobre fundo escuro #0D0716.

### 11. Textos e SEO

- Titulo e meta descricao: no topo do `index.html` (`<title>` e
  `<meta name="description">`).
- Dados estruturados `LocalBusiness`: bloco `<script type="application/ld+json">`
  no `<head>` (nome, morada, telefones, horario, redes).
- Imagem de partilha: `media/og-image.jpg` (substitua por um JPG/PNG real de
  1200x630 para melhor compatibilidade em redes sociais).

## Funcionalidades incluidas

- Preloader com o simbolo a desenhar-se e barra em degradé.
- Hero 3D (Three.js): fita em degradé + esfera brilhante que reage ao rato, com
  objetos flutuantes e selo "Estamos abertos".
- Menu fixo com efeito vidro, seccao ativa e hamburger animado em mobile.
- Scroll suave (Lenis) e animacoes ao scroll (GSAP + ScrollTrigger).
- Contadores animados, parallax, timeline de processo animada.
- Servicos em cartoes com tilt 3D e listas expansíveis.
- Produtos com filtros e pedido direto por WhatsApp.
- Galeria masonry com filtros e lightbox (setas, teclado, swipe, zoom).
- Videos em modal com player personalizado.
- Carrossel infinito de parceiros (a preto e branco -> cor no hover).
- Bloco de Facebook com seguidores, Messenger e publicacoes.
- Indicador **Aberto agora / Fechado** calculado pela hora de Mocambique
  (`Africa/Maputo`), com proxima abertura e destaque do dia de hoje.
- Formulario validado com envio por Formspree/EmailJS (ou WhatsApp/e-mail) e
  pre-preenchimento a partir do produto escolhido.
- Catalogo dinamico (`data/catalog.json`) com editor em `admin.html`.
- Versao bilingue PT/EN com seletor no menu e persistencia local.
- Feed automatico do Facebook (Page Plugin) e suporte a Instagram.
- Google Analytics 4 com consentimento e dados estruturados `LocalBusiness`.
- Botoes flutuantes de WhatsApp e "voltar ao topo".
- Cursor personalizado com rasto de tinta, barra de progresso de scroll e
  fundos animados.
- 100% responsivo, imagens em `lazy-loading`, respeito por
  `prefers-reduced-motion` e SEO/Open Graph.

## Otimizacao para ligacoes lentas

- As fotografias de apoio foram comprimidas (JPG, ~60-180 KB). Ao trocar pelas
  fotos reais, comprima-as (WebP/JPG, ~100-200 KB) e mantenha as dimensoes
  indicadas nos atributos `width`/`height`.
- Os videos demo usam `preload="none"` (so carregam quando o utilizador abre o
  cartao), por isso nao pesam na primeira visita.
- O 3D e simplificado automaticamente em ecra pequeno e a densidade de pixels e
  limitada.
- Se quiser um site ainda mais leve, pode remover o `initHero3D()` e ficar
  apenas com as animacoes CSS/GSAP.

## Acessibilidade

- Navegacao por teclado com foco visivel, labels em controlos e `aria-label` em
  botoes/icones.
- Texto alternativo (`alt`) em imagens.
- Com `prefers-reduced-motion` ativo, todas as animacoes sao desligadas.

## Sugestoes de melhorias futuras

1. Substituir as fotografias e videos de apoio pelos reais da empresa (produtos,
   trabalhos, "Sobre nos" e videos), e os logotipos genericos dos parceiros.
2. Publicar o site num dominio proprio (ex.: `graphikone.co.mz`) com HTTPS.
3. ~~Ligar o formulario a um servico de envio (Formspree/EmailJS).~~ Feito.
4. ~~Adicionar um catalogo dinamico (CMS simples).~~ Feito (`data/catalog.json` + `admin.html`).
5. ~~Integrar um feed automatico do Facebook/Instagram.~~ Feito (Page Plugin + embed).
6. ~~Preenchimento automatico do formulario com o produto escolhido.~~ Feito.
7. ~~Configurar o Google Business Profile e o Google Analytics.~~ Preparado (JSON-LD + GA4 com consentimento).
8. ~~Criar versao bilingue (Portugues / Ingles).~~ Feito.

Pendente: preencher `CONFIG.form.endpoint` (ou EmailJS) e `CONFIG.analytics.ga4`
com dados reais, e validar a ficha do Google Business Profile.
