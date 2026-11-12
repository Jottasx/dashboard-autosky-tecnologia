@echo off
chcp 65001 > nul
title NOC Skyone Autosky - Inicializador

:: Garante que o script rode dentro da pasta onde o .bat está salvo
cd /d "%~dp0"

set PRECISOU_INSTALAR=0

echo ==================================================
echo 0. Verificando pre-requisitos (Git e Python)...
echo ==================================================

git --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Git nao encontrado. Instalando via winget...
    winget install -e --id Git.Git --accept-package-agreements --accept-source-agreements
    set PRECISOU_INSTALAR=1
) else (
    echo [OK] Git instalado.
)

python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python nao encontrado. Instalando via winget...
    winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
    set PRECISOU_INSTALAR=1
) else (
    echo [OK] Python instalado.
)

if %PRECISOU_INSTALAR% equ 1 (
    echo.
    echo ==================================================
    echo Instalacao concluida!
    echo Feche esta janela e de duplo clique no rodar_painel.bat
    echo novamente para o Windows carregar o Git e o Python.
    echo ==================================================
    pause
    exit /b
)

echo.
echo ==================================================
echo 1. Atualizando codigo do GitHub...
echo ==================================================
git pull

echo.
echo ==================================================
echo 2. Verificando dependencias do Python...
echo ==================================================
python -m pip install -r requirements.txt --quiet

echo.
echo ==================================================
echo 3. Iniciando Coletor e Painel Visual...
echo ==================================================
:: Inicia o coletor em uma janela separada
start "Coletor Autosky" cmd /k "python coletor.py"

:: Aguarda 3 segundos e inicia o Streamlit em outra janela
timeout /t 3 /nobreak > nul
start "Painel Streamlit" cmd /k "python -m streamlit run painel.py --server.headless true"

:: Aguarda 4 segundos para o servidor subir e abre o painel no Edge
timeout /t 4 /nobreak > nul
start msedge "http://localhost:8501"

echo.
echo Faca o login na janela do Edge que abriu.
timeout /t 5 > nul