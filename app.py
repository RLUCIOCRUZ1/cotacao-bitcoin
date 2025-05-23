# app.py
import streamlit as st
from fetch import get_cotacoes
from plot import gerar_graficos
from carteira import carregar_saldo, salvar_saldo
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import os
import pytz

st.set_page_config(page_title="Cotação BTC e Dólar", layout="centered")

# Estilo responsivo
st.markdown("""
    <style>
    @media (max-width: 768px) {
        .css-1v0mbdj, .stMetric, .stButton, .css-1cpxqw2 {
            font-size: 16px !important;
            text-align: center !important;
        }
        .stMetric {
            margin-bottom: 12px !important;
        }
        .css-1r6slb0, .block-container {
            padding: 1rem !important;
        }
    }
    body {
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Cotação do Bitcoin e Dólar")

# Inicializar saldo persistente na sessão
if "saldo_btc" not in st.session_state:
    st.session_state.saldo_btc = carregar_saldo()


# Atualização automática a cada 2 minutos (120000 ms)
st_autorefresh(interval=120000, key="auto_refresh")

st.button("🔁 Atualizar agora")  # Apenas visual (sem função extra)

fuso_brasilia = pytz.timezone("America/Sao_Paulo")
agora_brasilia = datetime.now(fuso_brasilia)

st.caption(f"⏱️ Última atualização: {agora_brasilia.strftime('%d/%m/%Y %H:%M:%S')}")

# Buscar cotações
cotacoes = get_cotacoes()

if cotacoes:
    st.metric("💵 Dólar (USD/BRL)", f"R$ {cotacoes['usd_brl']:.2f}")
    st.metric("₿ Bitcoin (BRL)", f"R$ {cotacoes['btc_brl']:,.2f}")
    st.metric("₿ Bitcoin (USD)", f"$ {cotacoes['btc_usd']:,.2f}")

    st.markdown("---")
    st.subheader("💼 Minha Carteira de Bitcoin")
    st.write(f"Saldo atual de BTC: **{st.session_state.saldo_btc:.8f}**")

    col1, col2 = st.columns(2)
    with col1:
        add_btc = st.number_input("Adicionar BTC", min_value=0.0, step=0.00001, format="%f", key="add")
        if st.button("➕ Adicionar"):
            st.session_state.saldo_btc += add_btc
            salvar_saldo(st.session_state.saldo_btc)
            os._exit(0)

    with col2:
        remove_btc = st.number_input("Retirar BTC", min_value=0.0, step=0.00001, format="%f", key="remove")
        if st.button("➖ Retirar"):
            st.session_state.saldo_btc = max(0.0, st.session_state.saldo_btc - remove_btc)
            salvar_saldo(st.session_state.saldo_btc)
            # app.py
import streamlit as st
from fetch import get_cotacoes
from plot import gerar_graficos
from carteira import carregar_saldo, salvar_saldo
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import os
import pytz

st.set_page_config(page_title="Cotação BTC e Dólar", layout="centered")

# Estilo responsivo
st.markdown("""
    <style>
    @media (max-width: 768px) {
        .css-1v0mbdj, .stMetric, .stButton, .css-1cpxqw2 {
            font-size: 16px !important;
            text-align: center !important;
        }
        .stMetric {
            margin-bottom: 12px !important;
        }
        .css-1r6slb0, .block-container {
            padding: 1rem !important;
        }
    }
    body {
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Cotação do Bitcoin e Dólar")

# Inicializar saldo persistente na sessão
if "saldo_btc" not in st.session_state:
    st.session_state.saldo_btc = carregar_saldo()


# Atualização automática a cada 2 minutos (120000 ms)
st_autorefresh(interval=120000, key="auto_refresh")

st.button("🔁 Atualizar agora")  # Apenas visual (sem função extra)

fuso_brasilia = pytz.timezone("America/Sao_Paulo")
agora_brasilia = datetime.now(fuso_brasilia)

st.caption(f"⏱️ Última atualização: {agora_brasilia.strftime('%d/%m/%Y %H:%M:%S')}")

# Buscar cotações
cotacoes = get_cotacoes()

if cotacoes:
    st.metric("💵 Dólar (USD/BRL)", f"R$ {cotacoes['usd_brl']:.2f}")
    st.metric("₿ Bitcoin (BRL)", f"R$ {cotacoes['btc_brl']:,.2f}")
    st.metric("₿ Bitcoin (USD)", f"$ {cotacoes['btc_usd']:,.2f}")

    st.markdown("---")
    st.subheader("💼 Minha Carteira de Bitcoin")
    st.write(f"Saldo atual de BTC: **{st.session_state.saldo_btc:.8f}**")

    col1, col2 = st.columns(2)
    with col1:
        add_btc = st.number_input("Adicionar BTC", min_value=0.0, step=0.00001, format="%f", key="add")
        if st.button("➕ Adicionar"):
            st.session_state.saldo_btc += add_btc
            salvar_saldo(st.session_state.saldo_btc)
            st.rerun()

    with col2:
        remove_btc = st.number_input("Retirar BTC", min_value=0.0, step=0.00001, format="%f", key="remove")
        if st.button("➖ Retirar"):
            st.session_state.saldo_btc = max(0.0, st.session_state.saldo_btc - remove_btc)
            salvar_saldo(st.session_state.saldo_btc)
            st.rerun()

    valor_em_brl = st.session_state.saldo_btc * cotacoes['btc_brl']
    valor_em_usd = st.session_state.saldo_btc * cotacoes['btc_usd']

    col3, col4 = st.columns(2)
    col3.metric("💰 Valor em Reais (BRL)", f"R$ {valor_em_brl:,.2f}")
    col4.metric("💵 Valor em Dólar (USD)", f"$ {valor_em_usd:,.2f}")

    st.markdown("---")
    st.subheader("📊 Histórico de Preços")
    periodo = st.selectbox("Escolha o período:", ["7 dias", "30 dias", "90 dias"])

    fig_btc_usd, fig_usd = gerar_graficos(periodo)
    st.plotly_chart(fig_btc_usd, use_container_width=True)
    st.plotly_chart(fig_usd, use_container_width=True)
else:
    st.error("Erro ao buscar cotações. Verifique sua conexão.")

    valor_em_brl = st.session_state.saldo_btc * cotacoes['btc_brl']
    valor_em_usd = st.session_state.saldo_btc * cotacoes['btc_usd']

    col3, col4 = st.columns(2)
    col3.metric("💰 Valor em Reais (BRL)", f"R$ {valor_em_brl:,.2f}")
    col4.metric("💵 Valor em Dólar (USD)", f"$ {valor_em_usd:,.2f}")

    st.markdown("---")
    st.subheader("📊 Histórico de Preços")
    periodo = st.selectbox("Escolha o período:", ["7 dias", "30 dias", "90 dias"])

    fig_btc_usd, fig_usd = gerar_graficos(periodo)
    st.plotly_chart(fig_btc_usd, use_container_width=True)
    st.plotly_chart(fig_usd, use_container_width=True)
else:
    st.error("Erro ao buscar cotações. Verifique sua conexão.")

