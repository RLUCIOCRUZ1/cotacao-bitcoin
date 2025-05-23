# plot.py
import plotly.graph_objects as go
import pandas as pd
import datetime
import requests

# Função para buscar histórico do Bitcoin em USD via CoinGecko
def get_btc_usd_historico(dias):
    hoje = datetime.date.today()
    inicio = hoje - datetime.timedelta(days=dias)
    url = (
        f"https://api.coinpaprika.com/v1/coins/btc-bitcoin/ohlcv/historical"
        f"?start={inicio.strftime('%Y-%m-%d')}&end={hoje.strftime('%Y-%m-%d')}"
    )
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        datas = [item['time_close'][:10] for item in data]
        valores = [item['close'] for item in data]
        df = pd.DataFrame({'Data': datas, 'Bitcoin (USD)': valores})
        df['Data'] = pd.to_datetime(df['Data']).dt.strftime('%d/%m/%Y')
        return df
    except Exception as e:
        print("Erro CoinPaprika BTCUSD:", e)
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

    print("BTC/USD:", df_btc_usd.shape, df_btc_usd.head())
    print("USD/BRL:", df_usd.shape, df_usd.head())

    fig_btc_usd = go.Figure()
    if not df_btc_usd.empty:
        fig_btc_usd.add_trace(go.Scatter(x=df_btc_usd['Data'], y=df_btc_usd['Bitcoin (USD)'], mode='lines+markers', name='BTC (USD)'))
    fig_btc_usd.update_layout(title=f'Bitcoin (USD) - Últimos {dias} dias', xaxis_title='Data', yaxis_title='US$')

    fig_usd = go.Figure()
    if not df_usd.empty:
        fig_usd.add_trace(go.Scatter(x=df_usd['Data'], y=df_usd['Dólar (USD)'], mode='lines+markers', name='USD/BRL'))
    fig_usd.update_layout(title=f'Dólar (USD) - Últimos {dias} dias', xaxis_title='Data', yaxis_title='R$')

    return fig_btc_usd, fig_usd
