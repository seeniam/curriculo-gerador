@echo off
setlocal
cd /d "%~dp0"

echo ====================================
echo  Gerador de Curriculo PDF - 1 pagina
echo ====================================
echo.
echo Este comando usa a vaga mais recente encontrada em:
echo - raiz do projeto
echo - jobs\
echo - legacy\
echo.

python gerador_de_cv.py --one-page --pdf-only --no-portfolio

echo.
pause
