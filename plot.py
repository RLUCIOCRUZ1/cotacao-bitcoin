# plot.py
import plotly.graph_objects as go
import pandas as pd
import datetime
import requests
import streamlit as st  # necessário para visualizar dentro do app

# Função para buscar histórico do Bitcoin em USD via CoinGecko
def get_btc_usd_historico(dias):
    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days={dias}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            st.error(f"Erro HTTP {response.status_code} da CoinGecko.")
            return pd.DataFrame(columns=["Data", "Bitcoin (USD)"])

        json_data = response.json()
        data = json_data.get("prices", [])

        if not data:
            st.error("CoinGecko não retornou dados de preços.")
            return pd.DataFrame(columns=["Data", "Bitcoin (USD)"])

        datas = [datetime.datetime.fromtimestamp(p[0] / 1000).strftime("%d/%m/%Y") for p in data]
        valores = [p[1] for p in data]
        df = pd.DataFrame({"Data": datas, "Bitcoin (USD)": valores})

        st.subheader("📦 Dados brutos CoinGecko:")
        st.dataframe(df.head(10))  # Exibe os primeiros registros

        return df
    except Exception as e:
        st.error(f"Erro ao buscar dados da CoinGecko: {e}")
        return pd.DataFrame(columns=["Data", "Bitcoin (USD)"])

# Função para buscar histórico do Dólar via AwesomeAPI
def get_usd_brl_historico(dias):
    url = f"https://economia.awesomeapi.com.br/json/daily/USD-BRL/{dias}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        datas = [datetime.datetime.fromtimestamp(int(d['timestamp'])).strftime('%d/%m/%Y') for d in reversed(data)]
        valores = [float(d['bid']) for d in reversed(data)]
        return pd.DataFrame({'Data': datas, 'Dólar (USD)': valores})
    except:
        return pd.DataFrame(columns=['Data', 'Dólar (USD)'])

def gerar_graficos(periodo):
    dias = 7 if periodo == "7 dias" else 30 if periodo == "30 dias" else 90

    df_btc_usd = get_btc_usd_historico(dias)
    df_usd = get_usd_brl_historico(dias)

    fig_btc_usd = go.Figure()
    if not df_btc_usd.empty:
        fig_btc_usd.add_trace(go.Scatter(x=df_btc_usd['Data'], y=df_btc_usd['Bitcoin (USD)'],
                                         mode='lines+markers', name='BTC (USD)'))
    fig_btc_usd.update_layout(title=f'Bitcoin (USD) - Últimos {dias} dias',
                              xaxis_title='Data', yaxis_title='US$')

    fig_usd = go.Figure()
    if not df_usd.empty:
        fig_usd.add_trace(go.Scatter(x=df_usd['Data'], y=df_usd['Dólar (USD)'],
                                     mode='lines+markers', name='USD/BRL'))
    fig_usd.update_layout(title=f'Dólar (USD) - Últimos {dias} dias',
                          xaxis_title='Data', yaxis_title='R$')

    return fig_btc_usd, fig_usd
