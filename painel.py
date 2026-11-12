import streamlit as st
import pandas as pd
import json
import os
import html

st.set_page_config(
    page_title="NOC | Skyone Autosky",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS global da página Streamlit
st.markdown("""
<style>
header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
.block-container { padding-top: 1.2rem; padding-bottom: 1rem; padding-left: 1.5rem; padding-right: 1.5rem; }
div[data-testid="stMetric"] {
    background-color: #161b22;
    border: 1px solid #30363d;
    padding: 12px 16px;
    border-radius: 8px;
}
div[data-testid="stMetricLabel"] { font-size: 0.85rem; color: #8b949e; }
div[data-testid="stMetricValue"] { font-size: 1.6rem; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

def cor_barra(valor):
    if valor >= 90:
        return "#f85149" # Vermelho (Crítico >= 90%)
    elif valor >= 70:
        return "#d29922" # Amarelo (Atenção 70-89%)
    return "#2ea043" # Verde (Normal < 70%)

def html_barra(valor):
    cor = cor_barra(valor)
    largura = min(max(valor, 0), 100)
    return (
        f'<div class="bar-container">'
        f'<div class="bar-bg"><div class="bar-fill" style="width:{largura}%; background-color:{cor};"></div></div>'
        f'<span class="bar-val">{valor}%</span>'
        f'</div>'
    )

def renderizar_tabela_html(df, mostrar_coluna_grupo=True):
    linhas_html = []
    for _, row in df.iterrows():
        cpu = int(row["CPU"])
        mem = int(row["Memória"])
        disco = int(row["Disco"])
        
        if cpu >= 90:
            classe_linha = "row-critico"
            status_txt = "🔴 Crítico"
        elif cpu >= 70:
            classe_linha = "row-atencao"
            status_txt = "🟡 Atenção"
        else:
            classe_linha = ""
            status_txt = "🟢 Normal"

        ambiente_seguro = html.escape(str(row["Ambiente"]))
        instancia_segura = html.escape(str(row["Instância"]))

        col_grupo_html = ""
        if mostrar_coluna_grupo:
            badge_cls = "badge-g1" if row["Grupo"] == "Tecnologia" else "badge-g2"
            col_grupo_html = f'<td><span class="{badge_cls}">{row["Grupo"]}</span></td>'

        linhas_html.append(
            f'<tr class="{classe_linha}">'
            f'<td>{status_txt}</td>'
            f'<td class="ambiente-cell" title="Instância: {instancia_segura}">{ambiente_seguro}</td>'
            f'{col_grupo_html}'
            f'<td>{html_barra(cpu)}</td>'
            f'<td>{html_barra(mem)}</td>'
            f'<td>{html_barra(disco)}</td>'
            f'</tr>'
        )

    th_grupo = '<th style="width: 105px;">Grupo</th>' if mostrar_coluna_grupo else ""
    
    # Larguras otimizadas para nunca cortar a coluna Disco mesmo no modo Lado a Lado
    largura_barra = "115px" if mostrar_coluna_grupo else "88px"
    largura_status = "90px" if mostrar_coluna_grupo else "84px"

    tabela = (
        '<style>'
        '.noc-wrapper { max-height: 650px; overflow-y: auto; overflow-x: hidden; border: 1px solid #30363d; border-radius: 8px; background-color: #0d1117; }'
        '.noc-table { width: 100%; table-layout: fixed; border-collapse: collapse; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 0.85rem; color: #c9d1d9; }'
        '.noc-table th { position: sticky; top: 0; background-color: #161b22; color: #8b949e; text-align: left; padding: 9px 8px; border-bottom: 1px solid #30363d; font-weight: 600; z-index: 2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }'
        '.noc-table td { padding: 7px 8px; border-bottom: 1px solid #21262d; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }'
        '.noc-table tr:hover { background-color: rgba(255, 255, 255, 0.05); }'
        '.row-critico { background-color: rgba(248, 81, 73, 0.18) !important; }'
        '.row-atencao { background-color: rgba(210, 153, 34, 0.14) !important; }'
        '.ambiente-cell { cursor: help; font-weight: 500; color: #f0f6fc; }'
        '.badge-g1 { background-color: rgba(56, 139, 253, 0.15); color: #58a6ff; border: 1px solid rgba(56, 139, 253, 0.4); padding: 2px 8px; border-radius: 12px; font-size: 0.76rem; font-weight: 600; }'
        '.badge-g2 { background-color: rgba(163, 113, 247, 0.15); color: #bc8cff; border: 1px solid rgba(163, 113, 247, 0.4); padding: 2px 8px; border-radius: 12px; font-size: 0.76rem; font-weight: 600; }'
        '.bar-container { display: flex; align-items: center; gap: 5px; width: 100%; }'
        '.bar-bg { flex-grow: 1; height: 6px; background-color: #21262d; border-radius: 4px; overflow: hidden; min-width: 24px; }'
        '.bar-fill { height: 100%; border-radius: 4px; }'
        '.bar-val { width: 32px; flex-shrink: 0; text-align: right; font-variant-numeric: tabular-nums; font-size: 0.80rem; font-weight: 600; }'
        '</style>'
        '<div class="noc-wrapper">'
        '<table class="noc-table">'
        '<thead><tr>'
        f'<th style="width: {largura_status};">Status</th>'
        '<th>Ambiente <span style="font-weight:normal; font-size:0.72rem;">(hover = instância)</span></th>'
        f'{th_grupo}'
        f'<th style="width: {largura_barra};">CPU</th>'
        f'<th style="width: {largura_barra};">Memória</th>'
        f'<th style="width: {largura_barra};">Disco</th>'
        '</tr></thead>'
        f'<tbody>{"".join(linhas_html)}</tbody>'
        '</table>'
        '</div>'
    )
    st.markdown(tabela, unsafe_allow_html=True)

# Cabeçalho com Controles de Visualização e Filtro
col_titulo, col_modo, col_filtro = st.columns([2.2, 1.4, 1.4])

with col_titulo:
    st.markdown("### 🖥️ Monitoramento — Skyone Autosky")

with col_modo:
    modo_exibicao = st.radio(
        "Modo de visualização",
        ["📋 Painel Único (Todos)", "Columns Lado a Lado"],
        horizontal=True,
        label_visibility="collapsed"
    )

with col_filtro:
    filtro_status = st.selectbox(
        "Filtro",
        ["Todas as instâncias", "Atenção e Críticas (CPU ≥ 70%)", "Somente Críticas (CPU ≥ 90%)"],
        label_visibility="collapsed"
    )

def aplicar_filtro(df):
    if filtro_status == "Atenção e Críticas (CPU ≥ 70%)":
        return df[df["CPU"] >= 70]
    elif filtro_status == "Somente Críticas (CPU ≥ 90%)":
        return df[df["CPU"] >= 90]
    return df

@st.fragment(run_every=15)
def renderizar_painel_dados(modo, filtro):
    if not os.path.exists("dados_autosky.json"):
        st.warning("⏳ Aguardando o script `coletor.py` gerar a primeira leitura...")
        return

    with open("dados_autosky.json", "r", encoding="utf-8") as f:
        dados = json.load(f)

    st.caption(f"🟢 Online • Última coleta: **{dados.get('atualizado_em', '--:--:--')}** (Atualiza a cada 15s)")

    g1_lista = dados.get("grupo_1", [])
    g2_lista = dados.get("grupo_2", [])

    for item in g1_lista:
        item["Grupo"] = "Tecnologia"
    for item in g2_lista:
        item["Grupo"] = "AutoSky"

    area_conteudo = st.empty()
    with area_conteudo.container():
        if modo == "📋 Painel Único (Todos)":
            df_total = pd.DataFrame(g1_lista + g2_lista)
            if df_total.empty:
                st.info("Aguardando dados dos grupos...")
            else:
                df_total = df_total.sort_values(by="CPU", ascending=False)
                
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Total Geral", len(df_total))
                m2.metric("Tecnologia / AutoSky", f"{len(g1_lista)} / {len(g2_lista)}")
                m3.metric("Atenção (70-89%)", len(df_total[(df_total["CPU"] >= 70) & (df_total["CPU"] < 90)]))
                m4.metric("Críticas (≥ 90%)", len(df_total[df_total["CPU"] >= 90]))

                df_filtrado = aplicar_filtro(df_total)
                if df_filtrado.empty:
                    st.success("✅ Nenhuma instância neste nível de alerta.")
                else:
                    renderizar_tabela_html(df_filtrado, mostrar_coluna_grupo=True)
        else:
            col_esq, col_dir = st.columns(2, gap="small")

            for coluna, titulo, lista in [
                (col_esq, "🏢 Tecnologia", g1_lista),
                (col_dir, "☁️ AutoSky", g2_lista)
            ]:
                with coluna:
                    st.markdown(f"#### {titulo}")
                    df_g = pd.DataFrame(lista)
                    if df_g.empty:
                        st.info("Aguardando dados...")
                    else:
                        df_g = df_g.sort_values(by="CPU", ascending=False)
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Instâncias", len(df_g))
                        c2.metric("Atenção (70-89%)", len(df_g[(df_g["CPU"] >= 70) & (df_g["CPU"] < 90)]))
                        c3.metric("Críticas (≥ 90%)", len(df_g[df_g["CPU"] >= 90]))

                        df_filtrado = aplicar_filtro(df_g)
                        if df_filtrado.empty:
                            st.success("✅ Nenhuma instância neste nível de alerta.")
                        else:
                            renderizar_tabela_html(df_filtrado, mostrar_coluna_grupo=False)

renderizar_painel_dados(modo_exibicao, filtro_status)