import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import urllib.parse

st.set_page_config(page_title="Wilfer Trading Pro", layout="wide")

st.title("🚀 WILFER TRADING PRO")

# 1. GRÁFICO (LO MÁS IMPORTANTE)
st.header("📊 Gráfico de Velas en Tiempo Real")
activo_sel = st.selectbox("Selecciona activo:", ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "EURUSD=X"])

with st.spinner("Cargando gráfico profesional..."):
    # Descarga directa y aplanada
    df = yf.download(activo_sel, period="1mo", interval="1d")
    
    # Esto asegura que el formato sea limpio para el gráfico
    if not df.empty:
        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=df['Open'].iloc[:, 0] if isinstance(df['Open'], type(df)) else df['Open'],
            high=df['High'].iloc[:, 0] if isinstance(df['High'], type(df)) else df['High'],
            low=df['Low'].iloc[:, 0] if isinstance(df['Low'], type(df)) else df['Low'],
            close=df['Close'].iloc[:, 0] if isinstance(df['Close'], type(df)) else df['Close']
        )])
        fig.update_layout(template="plotly_dark", title=f"Evolución de {activo_sel}", height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("No se pudieron cargar los datos del gráfico. Por favor, refresca.")

# 2. ESCÁNER
if st.button("INICIAR ESCÁNER"):
    st.success("Radar activo: Analizando mercados...")

# 3. CALCULADORA
st.header("🧮 Calculadora de Riesgo")
entrada = st.number_input("Precio entrada:", value=50000.0)
if st.button("CALCULAR NIVELES"):
    st.success(f"🎯 Target: {entrada * 1.05:.2f} | 🛑 Stop: {entrada * 0.98:.2f}")

# 4. VIRALIZACIÓN
st.sidebar.header("🌐 ¡Comparte!")
url = "https://wilfer-trading-pro-wswpgyfaccxrhg6uyvq4dv.streamlit.app/"
st.sidebar.markdown(f"[💬 Compartir en WhatsApp](https://api.whatsapp.com/send?text=Mira%20esta%20app%20de%20trading:%20{url})")
