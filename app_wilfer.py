import streamlit as st
import yfinance as yf
import pandas as pd
st.image("logo.wilfer.jpg", width=400)
# Configuración de la página para móviles y escritorio
st.set_page_config(page_title="Wilfer Trading Pro", layout="centered")

st.title("🚀 WILFER TRADING PRO")
st.subheader("Radar de Mercados en Tiempo Real")

ACTIVOS = [
    "BTC-USD", 
    "ETH-USD", 
    "SOL-USD", 
    "BNB-USD", 
    "XRP-USD", 
    "EURUSD=X"
]
    

def calcular_indicadores(df):
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

# Botón para ejecutar el escáner
if st.button("INICIAR ESCÁNER"):
    st.write("Analizando activos...")
    for activo in ACTIVOS:
        ticker = yf.Ticker(activo)
        df = ticker.history(period="5d", interval="15m")
        if not df.empty:
            df = calcular_indicadores(df)
            ultimo = df.iloc[-1]
            
            if ultimo['Close'] > ultimo['EMA50'] and ultimo['RSI'] < 40:
                st.success(f"{activo}: SEÑAL LONG (Alcista)")
            elif ultimo['Close'] < ultimo['EMA50'] and ultimo['RSI'] > 60:
                st.error(f"{activo}: SEÑAL SHORT (Bajista)")
            else:
                st.info(f"{activo}: Precio {ultimo['Close']:.2f} | Monitoreando...")

st.sidebar.markdown("---")
st.sidebar.text("Wilfer Trading Pro v1.0")