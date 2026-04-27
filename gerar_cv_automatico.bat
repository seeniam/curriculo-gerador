@echo off
:: Muda o diretorio ativo para a pasta onde este arquivo .bat esta localizado
cd /d "%~dp0"

echo Verificando e instalando dependencias (isso e rapido)...
pip install pypdf -q
where codex >nul 2>nul
if errorlevel 1 (
    echo ERRO: Codex CLI nao encontrado no PATH.
    echo Instale ou faca login no Codex CLI antes de gerar o curriculo.
    pause
    exit /b 1
)

echo ====================================
echo Iniciando Gerador de Curriculo com Codex...
echo Arquitetura: Markdown como source of truth + HTML ATS-friendly
echo ====================================

python gerador_de_cv.py

pause
