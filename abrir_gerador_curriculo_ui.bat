@echo off
setlocal
cd /d "%~dp0"

echo ==========================================
echo  Gerador de Curriculo Inteligente - UI
echo ==========================================
echo.

if exist ".venv\Scripts\activate.bat" (
    echo Ativando ambiente virtual .venv...
    call ".venv\Scripts\activate.bat"
)

python -c "import flask" >nul 2>nul
if errorlevel 1 (
    echo Flask nao encontrado. Instalando dependencias minimas...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo Nao foi possivel instalar as dependencias.
        echo Rode manualmente: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo Abrindo http://127.0.0.1:5000 ...
start "" "http://127.0.0.1:5000"

python ui\app.py

echo.
pause
