@echo off
chcp 65001 > nul
title NOC Skyone Autosky - Inicializador

:: Garante que o script rode dentro da pasta onde o .bat está salvo
cd /d "%~dp0"

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
echo Tudo iniciado! Faca o login na janela do Edge que abriu.
timeout /t 5 > nul