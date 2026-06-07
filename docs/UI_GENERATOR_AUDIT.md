# Auditoria do Fluxo de Geracao de Curriculo

## Como o fluxo atual funciona

O projeto usa `gerador_de_cv.py` como entrypoint principal. Esse arquivo delega para `generator.pipeline.main()`, que:

1. Resolve os caminhos principais do projeto em `resolve_context()`.
2. Carrega `career/career_master.md`, `career/raw_notes.md`, templates HTML/CSS, personas e referencias legadas.
3. Localiza a vaga de entrada por argumento `--job`, por `--all` ou, sem argumentos, pela vaga mais recente encontrada.
4. Monta um prompt com a vaga, o career master e os templates.
5. Chama o Codex CLI em modo nao interativo.
6. Sanitiza o HTML retornado.
7. Salva o HTML em `output/`.
8. Exporta PDF via Chrome/Edge headless.
9. Opcionalmente remove o HTML intermediario com `--pdf-only`.
10. Opcionalmente anexa `portfolio-visual.pdf`, exceto quando usado `--no-portfolio`.

## Entrada usada pela pipeline

A busca de vagas fica em `generator/io_utils.py`.

Ordem de busca:

- `jobs/`
- raiz do projeto
- `legacy/`

Padroes aceitos:

- `vaga*.md`
- `job*.md`

Sem argumentos, a pipeline usa o arquivo mais recente por data de modificacao. Com `--job`, usa o caminho informado diretamente.

## Como HTML e PDF sao gerados

O HTML e produzido pelo Codex CLI a partir do prompt montado em `generator/pipeline.py`. Depois passa por:

- `sanitize_html_output()`
- `apply_layout_mode()` quando `--one-page` esta ativo
- `export_html_to_pdf()`, que chama Chrome/Edge headless

O fluxo continua sendo HTML primeiro, PDF depois.

## Onde o nome do arquivo final e definido

O nome do HTML e definido por `build_output_path()` em `generator/pipeline.py`.

Regras atuais:

- Com `--output-name`, usa o nome informado e troca a extensao para `.html`.
- Sem `--output-name`, cria `curriculo-{slug-da-vaga}_neemias.html`.
- Com `--one-page`, adiciona `_1pagina`.
- Se o HTML ja existir, adiciona timestamp.

O PDF usa o mesmo nome do HTML com extensao `.pdf`, por `build_pdf_output_path()`.

## BATs atuais

`gerar_curriculo_pdf.bat` roda:

```bat
python gerador_de_cv.py --one-page --pdf-only --no-portfolio
```

Esse BAT usa a vaga mais recente encontrada e deve continuar funcionando como fallback.

`gerar_cv_automatico.bat` roda o fluxo antigo mais amplo, instalando `pypdf` e chamando:

```bat
python gerador_de_cv.py
```

## Riscos encontrados

- O workspace possui muitos arquivos gerados e vagas soltas nao rastreadas, o que exige staging cuidadoso.
- `.gitignore` ainda estava minimo no momento da auditoria e nao cobria caches, PDFs, HTMLs finais e temporarios.
- A pipeline depende do Codex CLI autenticado e de Chrome/Edge disponivel para exportar PDF.
- A chamada ao Codex pode demorar e precisa de feedback visual na UI.
- A geracao salva arquivos em `legacy/` e `output/`; a UI deve evitar sobrescrita e nomes invalidos no Windows.
- `.env` nao deve ser lido, exibido ou exposto pela UI.

## Estrategia de integracao da UI

A UI sera uma camada local simples em Flask, sem build frontend pesado.

Fluxo proposto:

1. Usuario cola cargo, empresa e descricao da vaga.
2. `generator/ui_service.py` sanitiza cargo/empresa.
3. O servico salva um `.md` em `legacy/`.
4. O servico chama a pipeline existente via Python subprocess:
   `python gerador_de_cv.py --job <vaga.md> --one-page --pdf-only --no-portfolio --output-name <nome-final.pdf>`
5. A UI retorna caminho do PDF final em `output/`.

## O que sera mantido intacto

- `gerar_curriculo_pdf.bat` continua funcionando como fallback.
- `gerar_cv_automatico.bat` nao sera alterado sem necessidade.
- A pipeline principal sera reutilizada.
- `career_master.md` e `.env` nao serao expostos pela UI.
- Arquivos gerados de `output/` nao devem entrar em commit.
