# Gerador de Curriculo Inteligente

Aplicacao local em Python/Flask para gerar curriculos personalizados em PDF a partir da descricao de uma vaga.

O fluxo principal e simples:

1. Clicar no atalho `.bat` na area de trabalho.
2. A interface web abre no navegador.
3. Colar a descricao da vaga.
4. Clicar em `Gerar curriculo`.
5. O sistema salva a vaga localmente e gera o PDF final.

## O que sobe para o Git

Este repositorio deve subir apenas o que automatiza a geracao do curriculo:

- codigo Python da pipeline;
- UI Flask;
- templates HTML/CSS;
- scripts `.bat`;
- configuracoes de deploy;
- documentacao;
- base mestre em `career/`;
- arquivos de referencia necessarios para a pipeline.

Nao devem subir:

- vagas geradas em `legacy/vaga*.md`;
- curriculos temporarios em `legacy/curriculo*.md`;
- PDFs, HTMLs, imagens ou textos gerados em `output/`;
- `.env`;
- `__pycache__/`;
- perfis temporarios de navegador;
- arquivos temporarios do Codex CLI.

Essas regras ficam em `.gitignore`.

## Estrutura principal

```text
career/
  career_master.md          base principal da carreira
  raw_notes.md              notas opcionais

generator/
  pipeline.py               pipeline principal de geracao
  ui_service.py             integra UI Flask com a pipeline
  io_utils.py               funcoes de leitura, busca e diretorios
  persona_headhunter_*.md   personas usadas no prompt

templates/
  resume_base.html          template HTML do curriculo
  resume.css                estilos do curriculo

ui/
  app.py                    aplicacao Flask
  templates/index.html      tela web local
  static/                   CSS, JS, logo e favicon da UI

legacy/
  default.html              referencia legada em ingles
  default_pt.html           referencia legada em portugues
  vaga*.md                  vagas geradas localmente, ignoradas pelo Git

output/
  *.pdf                     curriculos gerados, ignorados pelo Git

abrir_gerador_curriculo_ui.bat
gerar_curriculo_pdf.bat
gerar_cv_automatico.bat
gerador_de_cv.py
requirements.txt
```

## Requisitos

- Windows para uso pelos `.bat`.
- Python instalado e disponivel no terminal.
- Codex CLI instalado e autenticado.
- Chrome, Edge ou Chromium instalado para exportar PDF.

Dependencias Python:

```bash
pip install -r requirements.txt
```

O `.bat` da UI tenta instalar as dependencias automaticamente se o Flask nao estiver disponivel.

## Configuracao opcional

Crie um arquivo `.env` na raiz se quiser fixar caminho/modelo/perfil do Codex CLI:

```env
CODEX_CLI_PATH=
CODEX_MODEL=
CODEX_PROFILE=
```

Para deploy privado, tambem use:

```env
APP_ACCESS_TOKEN=um-token-longo-e-privado
PORT=
```

Nunca commite `.env`.

## Como usar pela interface local

O arquivo principal para uso diario e:

```bat
abrir_gerador_curriculo_ui.bat
```

Ele faz o seguinte:

1. Entra na pasta do projeto.
2. Ativa `.venv`, se existir.
3. Verifica dependencias basicas.
4. Abre `http://127.0.0.1:5000`.
5. Inicia o Flask com `python ui\app.py`.

Na tela:

1. Informe o cargo ou nome da vaga.
2. Informe a empresa.
3. Cole a descricao completa da vaga.
4. Clique em `Gerar curriculo`.
5. Aguarde o estado de sucesso.
6. Clique em `Abrir PDF` ou veja o arquivo em `output/`.

O sistema salva:

- a vaga em `legacy/`;
- o PDF final em `output/`.

Esses arquivos sao locais e nao devem ser versionados.

## Criar atalho na area de trabalho

Para deixar o fluxo com um clique:

1. Encontre `abrir_gerador_curriculo_ui.bat` na raiz do projeto.
2. Clique com o botao direito.
3. Escolha `Enviar para > Area de trabalho (criar atalho)`.
4. Renomeie o atalho para `Gerador de Curriculo Inteligente`, se quiser.

Depois disso, basta clicar no atalho da area de trabalho para abrir o site local.

## Fluxo interno da geracao

Quando voce clica em `Gerar curriculo`, a UI chama:

```text
POST /generate
```

O backend executa este fluxo:

1. `ui/app.py` recebe os dados da vaga.
2. `generator/ui_service.py` salva a descricao em `legacy/`.
3. O servico chama a pipeline via subprocess:

```bash
python gerador_de_cv.py --job <vaga> --one-page --pdf-only --no-portfolio --output-name <arquivo.pdf>
```

4. `generator/pipeline.py` carrega `career/career_master.md`.
5. A pipeline monta o prompt com a vaga, templates e personas.
6. O Codex CLI gera o HTML final.
7. O HTML e sanitizado e ajustado para uma pagina.
8. Chrome/Edge/Chromium headless exporta o PDF.
9. O HTML temporario e removido.
10. A UI mostra o link do PDF.

## Geracao por terminal

Gerar usando a vaga mais recente:

```bash
python gerador_de_cv.py --one-page --pdf-only --no-portfolio
```

Gerar para uma vaga especifica:

```bash
python gerador_de_cv.py --job "legacy/nome-da-vaga.md" --one-page --pdf-only --no-portfolio
```

Gerar com nome de saida definido:

```bash
python gerador_de_cv.py --job "legacy/nome-da-vaga.md" --one-page --pdf-only --no-portfolio --output-name "Curriculo - Minha Vaga.pdf"
```

## Scripts BAT

`abrir_gerador_curriculo_ui.bat`

Abre a interface web local. Este e o fluxo recomendado.

`gerar_curriculo_pdf.bat`

Gera um PDF direto pela vaga mais recente, sem abrir a UI.

`gerar_cv_automatico.bat`

Executa o fluxo legado mais amplo.

## Deploy privado

A aplicacao Flask esta preparada para Gunicorn:

```bash
gunicorn ui.app:app --bind 0.0.0.0:$PORT
```

Em producao, configure obrigatoriamente:

```env
APP_ACCESS_TOKEN=um-token-longo-e-privado
```

Se `PORT` estiver definido e `APP_ACCESS_TOKEN` nao estiver configurado, a UI bloqueia o acesso.

Para Linux, o ambiente precisa ter Chrome ou Chromium disponivel para gerar PDF.

Mais detalhes estao em:

```text
docs/DEPLOY_AUDIT.md
```

## Cuidados antes de commit

Antes de commitar, confira:

```bash
git status --short
```

Pode commitar:

- codigo;
- templates;
- UI;
- `.bat`;
- docs;
- `requirements.txt`;
- `.env.example`;
- `.gitignore`;
- `career/career_master.md`.

Nao commitar:

- `legacy/vaga*.md`;
- `legacy/curriculo*.md`;
- `output/`;
- `*.pdf` gerado;
- `.env`;
- `__pycache__/`.

## Validacao rapida

Compile os modulos Python:

```bash
python -m compileall generator ui
```

Abra a UI:

```bat
abrir_gerador_curriculo_ui.bat
```

Gere um curriculo de teste e confirme:

- a vaga foi salva em `legacy/`;
- o PDF saiu em `output/`;
- o botao `Abrir PDF` funciona;
- `git status --short` nao mostra `legacy/vaga*.md` nem arquivos de `output/` como itens para commit.
