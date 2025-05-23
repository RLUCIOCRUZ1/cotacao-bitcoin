# plot.py
import plotly.graph_objects as go
import pandas as pd
import datetime
import requests

# Função para buscar histórico do Bitcoin em USD via CoinGecko
def get_btc_usd_historico(dias):
    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days={dias}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()['prices']
        datas = [datetime.datetime.fromtimestamp(x[0] / 1000).strftime('%d/%m/%Y') for x in data]
        valores = [x[1] for x in data]
        return pd.DataFrame({'Data': datas, 'Bitcoin (USD)': valores})
    except:
        return pd.DataFrame(columns=['Data', 'Bitcoin (USD)'])

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
        fig_btc_usd.add_trace(go.Scatter(x=df_btc_usd['Data'], y=df_btc_usd['Bitcoin (USD)'], mode='lines+markers', name='BTC (USD)'))
    fig_btc_usd.update_layout(title=f'Bitcoin (USD) - Últimos {dias} dias', xaxis_title='Data', yaxis_title='US$')

    fig_usd = go.Figure()
    if not df_usd.empty:
        fig_usd.add_trace(go.Scatter(x=df_usd['Data'], y=df_usd['Dólar (USD)'], mode='lines+markers', name='USD/BRL'))
    fig_usd.update_layout(title=f'Dólar (USD) - Últimos {dias} dias', xaxis_title='Data', yaxis_title='R$')

    return fig_btc_usd, fig_usd