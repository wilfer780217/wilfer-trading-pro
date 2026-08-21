import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import urllib.parse

st.set_page_config(page_title="Wilfer Trading Pro", layout="wide")

st.image("logo.wilfer.jpg", width=300)
st.title("🚀 WILFER TRADING PRO")

# 1. RADAR
st.header("🔍 Radar de Mercados")
if st.button("ACTUALIZAR ESCÁNER"):
    tickers = ["BTC-USD", "ETH-USD"]
    for t in tickers:
        df = yf.download(t, period="5d", interval="15m", progress=False)
        if not df.empty:
            st.write(f"**{t}**: Precio actual {df['Close'].iloc[-1]:.2f}")

# 2. EL GRÁFICO (El que querías ver)
st.header("📊 Gráfico de Velas")
activo = st.selectbox("Elige activo:", ["BTC-USD", "ETH-USD", "SOL-USD"])

with st.spinner('Cargando gráfico profesional...'):
    try:
        # Descarga forzada
        df = yf.download(activo, period="1mo", interval="1d", progress=False)
        
        if not df.empty:
            fig = go.Figure(data=[go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']
            )])
            fig.update_layout(template="plotly_dark", title=f"Gráfico de {activo}", height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No hay datos disponibles para este activo ahora mismo.")
    except Exception as e:
        st.error(f"Error al cargar: {e}")

# 3. CALCULADORA
st.header("🧮 Calculadora de Riesgo")
entrada = st.number_input("Precio entrada:", value=50000.0)
if st.button("CALCULAR"):
    tp = entrada * 1.05
    sl = entrada * 0.98
    st.write(f"Target: {tp:.2f} | Stop: {sl:.2f}")

# 4. VIRALIZACIÓN
st.sidebar.subheader("¡Comparte!")
url = "https://wilfer-trading-pro-wswpgyfaccxrhg6uyvq4dv.streamlit.app/"
st.sidebar.markdown(f"[Compartir en WhatsApp](https://api.whatsapp.com/send?text=Mira%20Wilfer%20Trading%20Pro:%20{url})")
