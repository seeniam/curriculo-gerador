# AI Tailored CV Generator

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

Ao final da geracao, o pipeline salva:

- o arquivo `.html`
- o arquivo `.pdf` correspondente, gerado automaticamente via Chrome/Edge headless quando disponivel

Isso melhora a consistencia da exportacao e tende a preservar hyperlinks clicaveis no PDF final.

## Como gerar

1. Crie `.env` com `GEMINI_API_KEY`.
2. Preencha `career/career_master.md`.
3. Opcionalmente preencha `career/raw_notes.md`.
4. Coloque uma vaga em um arquivo `vaga*.md` ou `job*.md` no diretorio raiz, em `jobs/` ou use um arquivo legado em `legacy/`.
5. Rode:

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

No Windows, tambem pode usar:

```bat
gerar_cv_automatico.bat
```

## Compatibilidade

Os arquivos antigos foram preservados em `legacy/`.
O pipeline atual continua aproveitando esse material como referencia, mas a fonte principal de verdade agora e o Markdown em `career/career_master.md`.
