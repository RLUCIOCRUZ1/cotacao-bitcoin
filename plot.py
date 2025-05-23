# plot.py
import plotly.graph_objects as go
import pandas as pd
import datetime
import requests
import streamlit as st  # necessário para visualizar dentro do app

# Função para buscar histórico do Bitcoin em USD via CoinGecko
def get_btc_usd_historico(dias: int, max_retries: int = 3) -> pd.DataFrame:
    """
    Busca dados históricos do Bitcoin com tratamento de rate limiting
    
    Args:
        dias: Número de dias para buscar dados históricos
        max_retries: Número máximo de tentativas em caso de erro
    
    Returns:
        DataFrame com dados históricos ou DataFrame vazio em caso de erro
    """
    
    # Headers para parecer mais com um navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache'
    }
    
    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days={dias}"
    
    for tentativa in range(max_retries):
        try:
            # Adiciona delay entre tentativas
            if tentativa > 0:
                delay = 2 ** tentativa  # Backoff exponencial: 2s, 4s, 8s...
                st.info(f"Aguardando {delay}s antes da tentativa {tentativa + 1}...")
                time.sleep(delay)
            
            st.info(f"Tentativa {tentativa + 1}: Buscando dados da CoinGecko...")
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                json_data = response.json()
                data = json_data.get("prices", [])
                
                if not data:
                    st.error("CoinGecko não retornou dados de preços.")
                    return pd.DataFrame(columns=["Data", "Bitcoin (USD)"])
                
                # Processa os dados
                datas = [datetime.datetime.fromtimestamp(p[0] / 1000).strftime("%d/%m/%Y") for p in data]
                valores = [p[1] for p in data]
                
                df = pd.DataFrame({"Data": datas, "Bitcoin (USD)": valores})
                
                st.success(f"✅ Dados obtidos com sucesso! {len(df)} registros encontrados.")
                st.subheader("📦 Dados brutos CoinGecko:")
                st.dataframe(df.head(10))
                
                return df
                
            elif response.status_code == 429:
                # Rate limit exceeded
                retry_after = response.headers.get('Retry-After', '60')
                st.warning(f"⚠️ Rate limit excedido (HTTP 429). Aguardando {retry_after}s...")
                time.sleep(int(retry_after))
                continue
                
            else:
                st.error(f"Erro HTTP {response.status_code}: {response.text}")
                if tentativa == max_retries - 1:
                    return pd.DataFrame(columns=["Data", "Bitcoin (USD)"])
                continue
                
        except requests.exceptions.Timeout:
            st.error(f"Timeout na tentativa {tentativa + 1}")
            if tentativa == max_retries - 1:
                return pd.DataFrame(columns=["Data", "Bitcoin (USD)"])
            continue
            
        except requests.exceptions.RequestException as e:
            st.error(f"Erro de conexão na tentativa {tentativa + 1}: {e}")
            if tentativa == max_retries - 1:
                return pd.DataFrame(columns=["Data", "Bitcoin (USD)"])
            continue
            
        except Exception as e:
            st.error(f"Erro inesperado: {e}")
            return pd.DataFrame(columns=["Data", "Bitcoin (USD)"])
    
    st.error("❌ Todas as tentativas falharam. Tente novamente em alguns minutos.")
    return pd.DataFrame(columns=["Data", "Bitcoin (USD)"])


def get_btc_usd_alternativo(dias: int) -> pd.DataFrame:
    """
    Função alternativa usando API gratuita diferente (Yahoo Finance via yfinance)
    """
    try:
        import yfinance as yf
        
        # Calcula data de início
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=dias)
        
        st.info("Tentando fonte alternativa (Yahoo Finance)...")
        
        # Busca dados do Bitcoin
        btc = yf.Ticker("BTC-USD")
        hist = btc.history(start=start_date.strftime('%Y-%m-%d'), 
                          end=end_date.strftime('%Y-%m-%d'))
        
        if hist.empty:
            st.error("Nenhum dado encontrado na fonte alternativa.")
            return pd.DataFrame(columns=["Data", "Bitcoin (USD)"])
        
        # Formata os dados
        df = pd.DataFrame({
            "Data": [d.strftime("%d/%m/%Y") for d in hist.index],
            "Bitcoin (USD)": hist['Close'].values
        })
        
        st.success(f"✅ Dados obtidos da fonte alternativa! {len(df)} registros.")
        st.subheader("📦 Dados Yahoo Finance:")
        st.dataframe(df.head(10))
        
        return df
        
    except ImportError:
        st.error("Para usar fonte alternativa, instale: pip install yfinance")
        return pd.DataFrame(columns=["Data", "Bitcoin (USD)"])
    except Exception as e:
        st.error(f"Erro na fonte alternativa: {e}")
        return pd.DataFrame(columns=["Data", "Bitcoin (USD)"])


def get_btc_data_with_fallback(dias: int) -> pd.DataFrame:
    """
    Função principal que tenta CoinGecko primeiro, depois fonte alternativa
    """
    # Tenta CoinGecko primeiro
    df = get_btc_usd_historico(dias)
    
    # Se falhou, tenta fonte alternativa
    if df.empty:
        st.info("🔄 Tentando fonte de dados alternativa...")
        df = get_btc_usd_alternativo(dias)
    
    return df


# Exemplo de uso com cache do Streamlit
@st.cache_data(ttl=300)  # Cache por 5 minutos
def get_cached_btc_data(dias: int) -> pd.DataFrame:
    """Versão com cache para evitar muitas chamadas à API"""
    return get_btc_data_with_fallback(dias)
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
