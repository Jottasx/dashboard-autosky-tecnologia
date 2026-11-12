import time
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

# ==========================================
# CONFIGURAÇÕES - SUAS DUAS URLS
# ==========================================
URL_GRUPO_1 = "https://admin01.autosky.cloud/partners/6f678788-3c94-47ac-99b6-4b6eacaaedfe/instances"
URL_GRUPO_2 = "https://admin01.autosky.cloud/partners/19db221b-ce85-4a52-ba3b-15e710f2007a/instances"
INTERVALO_SEGUNDOS = 60

print("Iniciando o Microsoft Edge para coleta...")

edge_options = Options()
edge_options.add_argument("--start-maximized")
edge_options.add_argument("--disable-session-crashed-bubble")
edge_options.add_argument("--no-first-run")
edge_options.add_argument("--inprivate")
# Impede que o navegador reduza a prioridade ou pause abas em segundo plano
edge_options.add_argument("--disable-background-timer-throttling")
edge_options.add_argument("--disable-backgrounding-occluded-windows")
edge_options.add_argument("--disable-renderer-backgrounding")

try:
    driver = webdriver.Edge(options=edge_options)
except Exception as e:
    print("\n" + "!"*55)
    print("ERRO AO ABRIR O MICROSOFT EDGE:")
    print(e)
    print("!"*55)
    input("\nPressione ENTER para fechar...")
    exit(1)

def extrair_numero(texto):
    try:
        return int(texto.replace("%", "").strip())
    except ValueError:
        return 0

def extrair_tabela():
    servidores = []
    linhas = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
    
    for linha in linhas:
        colunas = linha.find_elements(By.TAG_NAME, "td")
        if len(colunas) >= 6:
            ambiente = colunas[1].text.strip()
            instancia = colunas[2].text.strip()
            cpu_txt = colunas[3].text.strip()
            mem_txt = colunas[4].text.strip()
            disco_txt = colunas[5].text.strip()

            servidores.append({
                "Ambiente": ambiente,
                "Instância": instancia,
                "CPU": extrair_numero(cpu_txt),
                "Memória": extrair_numero(mem_txt),
                "Disco": extrair_numero(disco_txt)
            })
    return servidores

# 1. Abre o portal e aguarda automaticamente o fim do login + MFA
driver.get(URL_GRUPO_1)
print("\n" + "="*55)
print("Aguardando autenticação no Microsoft Edge...")
print("(Preencha e-mail, senha e Google Authenticator no Edge)")
print("="*55 + "\n")

while True:
    url_atual = driver.current_url.lower()
    if "admin01.autosky.cloud/environments" in url_atual or "admin01.autosky.cloud/partners/" in url_atual:
        if len(driver.find_elements(By.TAG_NAME, "table")) > 0:
            print("Login detectado automaticamente!")
            break
    time.sleep(1.5)

# 2. Carrega as duas abas
print("Carregando abas das duas contas...")
driver.get(URL_GRUPO_1)
time.sleep(4)

driver.execute_script(f"window.open('{URL_GRUPO_2}', '_blank');")
abas = driver.window_handles
time.sleep(5)

# 3. Move a janela para fora da tela e minimiza (impede roubo de foco no Windows)
driver.set_window_position(-32000, -32000)
driver.minimize_window()
print("Edge ocultado! Monitoramento rodando sem roubar foco (Ctrl+C para parar).\n")

while True:
    try:
        driver.switch_to.window(abas[0])
        time.sleep(1)
        dados_g1 = extrair_tabela()

        driver.switch_to.window(abas[1])
        time.sleep(1)
        dados_g2 = extrair_tabela()

        payload = {
            "atualizado_em": datetime.now().strftime("%H:%M:%S"),
            "grupo_1": dados_g1,
            "grupo_2": dados_g2
        }

        with open("dados_autosky.json", "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        print(f"[{payload['atualizado_em']}] Atualizado: {len(dados_g1)} instâncias (Fortes) | {len(dados_g2)} instâncias (AutoSky)")

    except Exception as e:
        print(f"Erro durante a coleta: {e}")

    time.sleep(INTERVALO_SEGUNDOS)