@echo off
:: Muda o diretorio ativo para a pasta onde este arquivo .bat esta localizado
cd /d "%~dp0"

echo Verificando e instalando dependencias (isso e rapido)...
pip install google-generativeai python-dotenv -q

echo ====================================
echo Iniciando Gerador de Curriculo Baseado em IA...
echo ====================================

python gerador_de_cv.py

pause
