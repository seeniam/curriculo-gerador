# Codex Tailored CV Generator

## Nova arquitetura

Este projeto agora separa claramente:

- `career/` = source of truth da carreira em Markdown
- `templates/` = template de apresentacao HTML/CSS
- `generator/` = pipeline e personas
- `legacy/` = arquivos antigos preservados como referencia
- `output/` = curriculos gerados

## Source of truth

O arquivo principal agora e `career/career_master.md`.

Ele deve conter a verdade estruturada da sua carreira:

- identidade
- posicionamento
- experiencias
- projetos
- resultados
- formacao
- certificacoes
- idiomas
- provas de senioridade
- restricoes de verdade

`career/raw_notes.md` e um apoio para anotar conteudo cru ainda nao lapidado.

## Template

O HTML nao e mais a base de conhecimento.

Agora:

- `templates/resume_base.html` define a estrutura semantica
- `templates/resume.css` define a apresentacao

O gerador usa esses arquivos para orientar o HTML final ATS-friendly.

Ao final da geracao, o pipeline usa o Codex CLI em modo nao interativo e salva:

- o arquivo `.html`
- o arquivo `.pdf` correspondente, gerado automaticamente via Chrome/Edge headless quando disponivel

Isso melhora a consistencia da exportacao e tende a preservar hyperlinks clicaveis no PDF final.
O fluxo continua sendo sempre `HTML primeiro -> PDF depois`.

## Como gerar

1. Garanta que o Codex CLI esteja instalado e autenticado.
2. Preencha `career/career_master.md`.
3. Opcionalmente preencha `career/raw_notes.md`.
4. Coloque uma vaga em um arquivo `vaga*.md` ou `job*.md` no diretorio raiz, em `jobs/` ou use um arquivo legado em `legacy/`.
5. Opcionalmente crie `.env` com `CODEX_CLI_PATH`, `CODEX_MODEL` ou `CODEX_PROFILE` se quiser fixar o executavel/modelo/perfil.
6. Rode:

```bash
python gerador_de_cv.py
```

Para gerar para todas as vagas detectadas:

```bash
python gerador_de_cv.py --all
```

Para gerar apenas para uma vaga específica:

```bash
python gerador_de_cv.py --job legacy/vaga_itss.md
```

Para forcar um nome especifico de saida:

```bash
python gerador_de_cv.py --job "legacy/vaga-dev frontend pleno.md" --output-name curriculo-frontend_neemias.pdf
```

Para gerar uma versao compacta pensada para caber em 1 pagina A4:

```bash
python gerador_de_cv.py --one-page
```

Tambem pode combinar com uma vaga especifica:

```bash
python gerador_de_cv.py --job "legacy/vaga-devjr buzz.md" --one-page
```

No Windows, tambem pode usar:

```bat
gerar_cv_automatico.bat
```

## Compatibilidade

Os arquivos antigos foram preservados em `legacy/`.
O pipeline atual continua aproveitando esse material como referencia, mas a fonte principal de verdade agora e o Markdown em `career/career_master.md`.

## Provedor de IA

Esta branch alternativa nao usa Gemini nem `GEMINI_API_KEY`.

No Windows, o gerador tenta encontrar o Codex no `PATH` e tambem dentro das extensoes do VS Code/Cursor. Se ainda assim nao encontrar, defina no `.env`:

```env
CODEX_CLI_PATH=C:\Users\neemi\.vscode\extensions\openai.chatgpt-26.406.31014-win32-x64\bin\windows-x86_64\codex.exe
```

O gerador chama:

```bash
codex exec -
```

O prompt completo e enviado via stdin, e a ultima mensagem do Codex e tratada como o HTML final. O restante do fluxo continua igual: sanitizacao, modo 1 pagina, salvamento em `output/` e exportacao PDF via Chrome/Edge quando disponivel.

## Portfolio visual

Se existir um arquivo `portfolio-visual.pdf` na raiz do projeto, ele sera anexado automaticamente ao final do PDF exportado do curriculo.

O PDF final fica no mesmo arquivo de saida, com esta ordem:

1. Curriculo gerado para a vaga
2. `portfolio-visual.pdf` como pagina(s) final(is)

Para isso, o projeto usa `pypdf`:

```bash
pip install pypdf
```
