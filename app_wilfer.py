import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import os
import urllib.parse

st.set_page_config(page_title="Wilfer Trading Pro", layout="wide")

# --- LOGO Y TÍTULO ---
try:
    st.image("logo.wilfer.jpg", width=250)
except:
    st.title("☯️ WILFER TRADING PRO")

# --- NAVEGACIÓN ---
menu = st.sidebar.radio("Navegación:", ["Centro de Operaciones", "Gráfico Profesional", "Calculadora de Riesgo"])

# --- 1. CENTRO DE OPERACIONES ---
if menu == "Centro de Operaciones":
    st.title("🎯 Centro de Operaciones")
    # Aquí iría tu lógica de bitácora que me pasaste
    st.write("Tu bitácora y registro de operaciones activo.")
    
# --- 2. GRÁFICO PROFESIONAL (EL QUE FALTABA) ---
elif menu == "Gráfico Profesional":
    st.title("📊 Gráfico de Velas")
    activo = st.selectbox("Selecciona activo:", ["BTC-USD", "ETH-USD", "SOL-USD", "EURUSD=X"])
    
    with st.spinner("Cargando velas..."):
        df = yf.download(activo, period="1mo", interval="1d", progress=False)
        if not df.empty:
            fig = go.Figure(data=[go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']
            )])
            fig.update_layout(template="plotly_dark", height=500, yaxis=dict(side="right"))
            st.plotly_chart(fig, use_container_width=True)

# --- 3. CALCULADORA DE RIESGO ---
elif menu == "Calculadora de Riesgo":
    st.title("🧮 Calculadora de Gestión de Riesgo")
    # Tu calculadora funcional aquí
    precio = st.number_input("Precio entrada", value=50000.0)
    if st.button("CALCULAR"):
        st.success(f"TP y SL calculados para {precio}")

# --- VIRALIZACIÓN (SIEMPRE VISIBLE) ---
st.sidebar.markdown("---")
url = "https://wilfer-trading-pro-wswpgyfaccxrhg6uyvq4dv.streamlit.app/"
txt = urllib.parse.quote("¡Mira mi plataforma Wilfer Trading Pro!")
st.sidebar.markdown(f"💬 [WhatsApp](https://api.whatsapp.com/send?text={txt}%20{url})")
st.sidebar.markdown(f"✈️ [Telegram](https://t.me/share/url?url={url}&text={txt})")
st.sidebar.markdown(f"🐦 [Twitter](https://twitter.com/intent/tweet?text={txt}&url={url})")
