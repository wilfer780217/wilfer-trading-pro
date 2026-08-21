import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import urllib.parse

st.set_page_config(page_title="Wilfer Trading Pro", layout="wide")

# Logo y Título
st.image("logo.wilfer.jpg", width=300)
st.title("🚀 WILFER TRADING PRO")

# 1. RADAR DE MERCADO
st.header("🔍 Radar de Mercados en Tiempo Real")
if st.button("INICIAR ESCÁNER DE MERCADO"):
    activos = ["BTC-USD", "ETH-USD", "SOL-USD"]
    for activo in activos:
        df = yf.download(activo, period="5d", interval="15m", progress=False)
        if not df.empty:
            ultimo_precio = df['Close'].iloc[-1]
            st.success(f"📈 {activo} | Precio: {ultimo_precio:.2f}")

# 2. GRÁFICO PROFESIONAL
st.header("📊 Gráfico de Velas Japonesas")
activo_sel = st.selectbox("Selecciona activo para el gráfico:", ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD"])

with st.spinner("Cargando velas..."):
    df = yf.download(activo_sel, period="1mo", interval="1d", progress=False)
    if not df.empty:
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.update_layout(template="plotly_dark", title=f"Evolución {activo_sel}", height=500)
        st.plotly_chart(fig, use_container_width=True)

# 3. CALCULADORA DE RIESGO
st.header("🧮 Calculadora de Gestión de Riesgo")
col1, col2 = st.columns(2)
with col1:
    precio_entrada = st.number_input("Precio de entrada (USD)", value=50000.0)
    tipo = st.radio("Tipo de operación", ["LONG", "SHORT"])
with col2:
    tp_pct = st.slider("Take Profit (%)", 1, 20, 5)
    sl_pct = st.slider("Stop Loss (%)", 1, 10, 2)

if st.button("CALCULAR NIVELES"):
    if tipo == "LONG":
        tp = precio_entrada * (1 + tp_pct/100)
        sl = precio_entrada * (1 - sl_pct/100)
    else:
        tp = precio_entrada * (1 - tp_pct/100)
        sl = precio_entrada * (1 + sl_pct/100)
    st.write(f"🎯 **TAKE PROFIT:** {tp:.2f} USD")
    st.write(f"🛑 **STOP LOSS:** {sl:.2f} USD")

# 4. BARRA LATERAL (VIRALIZACIÓN)
st.sidebar.header("🌐 ¡Comparte Wilfer Trading!")
url = "https://wilfer-trading-pro-wswpgyfaccxrhg6uyvq4dv.streamlit.app/"
texto = urllib.parse.quote("¡Mira Wilfer Trading Pro, la mejor app de análisis!")

st.sidebar.markdown(f"[💬 WhatsApp](https://api.whatsapp.com/send?text={texto}%20{url})")
st.sidebar.markdown(f"[✈️ Telegram](https://t.me/share/url?url={url}&text={texto})")
st.sidebar.markdown(f"[🐦 Twitter](https://twitter.com/intent/tweet?text={texto}&url={url})")
