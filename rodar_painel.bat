@echo off
chcp 65001 > nul
title NOC Skyone Autosky - Inicializador

set REPO_URL=https://github.com/Jottasx/dashboard-autosky-tecnologia.git

:: Trabalha diretamente na pasta onde este .bat está salvo
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
echo 1. Baixando / Atualizando projeto do GitHub...
echo ==================================================
if not exist ".git" (
    echo Vinculando pasta atual ao repositorio do GitHub...
    git init
    git remote add origin "%REPO_URL%"
    git fetch origin
    git checkout -B main
    git reset --hard origin/main
    git branch --set-upstream-to=origin/main main
) else (
    echo Atualizando arquivos existentes...
    git fetch origin
    git reset --hard origin/main
)

echo.
echo ==================================================
echo 2. Verificando dependencias do Python...
echo ==================================================
python -m pip install -r requirements.txt --quiet

echo.
echo ==================================================
echo 3. Iniciando Coletor e Painel Visual...
echo ==================================================
start "Coletor Autosky" cmd /k "python coletor.py"

timeout /t 3 /nobreak > nul
start "Painel Streamlit" cmd /k "python -m streamlit run painel.py --server.headless true"

timeout /t 4 /nobreak > nul
start msedge "http://localhost:8501"

echo.
echo Tudo iniciado! Faca o login + MFA na janela do Edge que abriu.
timeout /t 5 > nul