# fetch.py
import requests

def get_cotacoes():
    try:
        usd_response = requests.get("https://economia.awesomeapi.com.br/json/last/USD-BRL", timeout=10)
        usd_brl = float(usd_response.json()['USDBRL']['bid'])

        btc_brl_response = requests.get("https://www.mercadobitcoin.net/api/BTC/ticker/", timeout=10)
        btc_brl = float(btc_brl_response.json()['ticker']['last'])

        btc_usd_response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=10)
        btc_usd_data = btc_usd_response.json()
        btc_usd = float(btc_usd_data.get('bitcoin', {}).get('usd', 0.0))

        return {
            'usd_brl': usd_brl,
            'btc_brl': btc_brl,
            'btc_usd': btc_usd
        }
    except Exception as e:
        print(f"Erro ao buscar cotações: {e}")
        return None