# Auditoria de deploy privado

Este documento registra a auditoria do projeto `curriculo-gerador` para uso local via `.bat` e deploy privado em plataformas Linux como Render ou Railway.

## Como a UI Flask inicia hoje

A UI local fica em `ui/app.py` e expõe o objeto Flask:

```python
app = Flask(__name__)
```

O entrypoint WSGI para produção é:

```bash
gunicorn ui.app:app
```

O comando local usado pelo BAT é:

```bat
python ui\app.py
```

O arquivo `abrir_gerador_curriculo_ui.bat`:

- entra na raiz do projeto;
- ativa `.venv`, se existir;
- instala `requirements.txt` se Flask não estiver disponível;
- abre `http://127.0.0.1:5000`;
- executa `python ui\app.py`.

## Porta e host

`ui/app.py` respeita a variável de ambiente `PORT`, exigida por Render/Railway:

```python
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port, debug=False)
```

Para produção, usar:

```bash
gunicorn ui.app:app
```

Se a plataforma exigir bind explícito:

```bash
gunicorn ui.app:app --bind 0.0.0.0:$PORT
```

## Proteção mínima

A aplicação não deve ficar pública sem proteção. A UI usa `APP_ACCESS_TOKEN` como proteção mínima.

Com `APP_ACCESS_TOKEN` configurado, o acesso exige HTTP Basic Auth. O usuário pode ser qualquer valor; a senha deve ser o token.

Em produção, se `PORT` estiver definido e `APP_ACCESS_TOKEN` não estiver configurado, a aplicação responde `503` e não libera a UI.

No uso local via `.bat`, se `APP_ACCESS_TOKEN` não existir, a UI continua abrindo normalmente sem senha para não quebrar o fluxo atual.

Variáveis recomendadas no deploy:

```env
APP_ACCESS_TOKEN=um-token-longo-e-privado
CODEX_CLI_PATH=
CODEX_MODEL=
CODEX_PROFILE=
```

## Como a geração funciona

Fluxo pela UI:

1. O usuário cola a descrição da vaga na rota `/`.
2. O frontend envia `POST /generate`.
3. `ui/app.py` chama `generate_resume_from_description()` em `generator/ui_service.py`.
4. `generator/ui_service.py` salva a vaga em `legacy/`.
5. O serviço chama o CLI antigo:

```bash
python gerador_de_cv.py --job <arquivo-da-vaga> --one-page --pdf-only --no-portfolio --output-name <nome-do-pdf>
```

6. `gerador_de_cv.py` chama `generator.pipeline.main()`.
7. `generator/pipeline.py` carrega:
   - `career/career_master.md`;
   - `career/raw_notes.md`, se existir;
   - templates HTML/CSS;
   - personas;
   - referências legadas.
8. A pipeline monta o prompt e chama o Codex CLI.
9. O retorno HTML é sanitizado, recebe o modo `one-page` e é salvo temporariamente em `output/`.
10. O HTML é exportado para PDF por Chrome/Chromium/Edge headless.
11. Com `--pdf-only`, o HTML intermediário é removido.
12. A UI retorna o link `/output/<arquivo>.pdf`.

## Como o PDF é gerado

A função principal é `export_html_to_pdf()` em `generator/pipeline.py`.

No Windows:

- procura Edge/Chrome;
- usa PowerShell para chamar o navegador em modo headless;
- gera PDF com `--print-to-pdf`.

No Linux:

- procura `google-chrome`, `google-chrome-stable`, `chromium` ou `chromium-browser`;
- chama o navegador diretamente, sem PowerShell;
- usa flags de headless e `--print-to-pdf`;
- usa `--no-sandbox`, necessário em muitos ambientes containerizados.

Se nenhum navegador compatível estiver instalado, a exportação PDF é ignorada e a UI falha porque espera o PDF final.

## Dependências Python

`requirements.txt` deve conter:

- `Flask`: UI web local;
- `gunicorn`: servidor WSGI de produção;
- `python-dotenv`: carregamento opcional de `.env` local;
- `pypdf`: usado quando o fluxo antigo anexa `portfolio-visual.pdf`.

## Dependências Linux

Além das dependências Python, o ambiente Linux precisa ter:

- Python 3.11+ recomendado;
- Codex CLI disponível e autenticado/configurado;
- Chrome ou Chromium instalado;
- fontes básicas do sistema para renderização consistente do PDF.

Exemplos de pacotes do sistema, dependendo da imagem:

```bash
chromium
fonts-liberation
```

Em plataformas sem instalação de pacotes do sistema, pode ser necessário usar Docker ou configurar um build step que instale Chromium.

## Dependências de Windows

O uso local atual depende de `.bat` e pode usar Edge/Chrome via caminhos do Windows.

O deploy Linux não depende dos `.bat` e não usa PowerShell para PDF.

Os `.bat` foram preservados:

- `abrir_gerador_curriculo_ui.bat`;
- `gerar_curriculo_pdf.bat`;
- `gerar_cv_automatico.bat`.

## Dependência de navegador/headless

Sim. O PDF é gerado a partir de HTML usando navegador headless.

Isso é uma dependência obrigatória para que a UI entregue PDF final. Sem Chrome/Chromium/Edge, o HTML pode ser criado, mas o PDF não será produzido.

## Pastas necessárias em runtime

Estas pastas precisam existir ou ser criadas pelo app:

- `legacy/`: recebe as descrições das vagas salvas pela UI;
- `output/`: recebe PDFs finais e arquivos temporários;
- `career/`: contém a base de conhecimento usada pela pipeline.

Em deploys com filesystem efêmero, `legacy/` e `output/` podem ser perdidos a cada restart. Para persistência real, configurar volume/disk persistente na plataforma.

## Arquivos que não podem ser públicos

Não devem ser expostos por rota HTTP:

- `.env`;
- `career/career_master.md`;
- `career/raw_notes.md`;
- `generator/persona_headhunter_pt.md`;
- `generator/persona_headhunter_en.md`;
- arquivos internos de `legacy/`;
- HTML intermediário em `output/`;
- qualquer output gerado fora dos PDFs explicitamente servidos.

A rota `/output/<filename>` só permite servir arquivos `.pdf` dentro de `output/`.

## Git e arquivos gerados

`.gitignore` cobre:

- `.env`;
- caches Python;
- logs e temporários;
- HTML/PDF/TXT em `output/`;
- perfis temporários de navegador;
- saída temporária do Codex CLI.

Não commitar PDFs, HTMLs finais ou outputs gerados.

## Riscos de segurança

Riscos principais:

- Se `APP_ACCESS_TOKEN` for fraco, a UI pode ser acessada por terceiros.
- O app executa subprocessos locais para chamar a pipeline e o navegador.
- O app usa o Codex CLI e envia conteúdo da vaga e base profissional para geração.
- `legacy/` e `output/` podem acumular dados sensíveis.
- Em plataforma com filesystem efêmero, os PDFs podem desaparecer após restart.
- O link `/output/<pdf>` fica acessível para quem estiver autenticado.
- Logs da plataforma podem conter mensagens de erro com caminhos locais.

Mitigações mínimas:

- Usar `APP_ACCESS_TOKEN` forte.
- Manter o repositório/deploy privado.
- Não commitar `.env`, PDFs ou outputs.
- Preferir plataforma com HTTPS.
- Limpar `legacy/` e `output/` periodicamente.
- Usar volume persistente se precisar manter histórico.

## Checklist de deploy

1. Instalar dependências Python:

```bash
pip install -r requirements.txt
```

2. Garantir Chrome/Chromium disponível no ambiente.
3. Configurar variáveis:

```env
APP_ACCESS_TOKEN=...
CODEX_CLI_PATH=...
CODEX_MODEL=...
CODEX_PROFILE=...
```

4. Start command:

```bash
gunicorn ui.app:app --bind 0.0.0.0:$PORT
```

5. Testar:

- abrir `/`;
- autenticar com o token;
- gerar currículo simples;
- confirmar vaga em `legacy/`;
- confirmar PDF em `output/`;
- abrir PDF pelo botão da UI.
