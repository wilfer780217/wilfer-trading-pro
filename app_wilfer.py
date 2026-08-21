import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import urllib.parse

# Configuración de la página (DEBE SER LO PRIMERO)
st.set_page_config(page_title="Wilfer Trading Pro", layout="centered")

# Mostrar logo y títulos
st.image("logo.wilfer.jpg", width=400)
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

st.markdown("---")

# SECCIÓN DE GRÁFICOS PROFESIONALES
st.subheader("📊 Gráfico Interactivo de Activos")
activo_seleccionado = st.selectbox("Selecciona un activo para ver el gráfico:", ACTIVOS)

# Descargar datos para el gráfico seleccionado (vela diaria, último mes)
data_grafico = yf.download(activo_seleccionado, period="1mo", interval="1d")

if not data_grafico.empty:
    fig = go.Figure(data=[go.Candlestick(
        x=data_grafico.index,
        open=data_grafico['Open'],
        high=data_grafico['High'],
        low=data_grafico['Low'],
        close=data_grafico['Close'],
        name="Velas"
    )])
    
    fig.update_layout(
        title=f"Evolución de {activo_seleccionado}",
        xaxis_title="Fecha",
        yaxis_title="Precio USD",
        xaxis_rangeslider_visible=False,
        template="plotly_dark"
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No se pudieron cargar los datos para el gráfico.")

# SECCIÓN DE VIRALIZACIÓN EN LA BARRA LATERAL
st.sidebar.markdown("---")
st.sidebar.subheader("🌐 ¡Comparte Wilfer Trading Pro!")
st.sidebar.write("Ayuda a que más traders conozcan la plataforma.")

# Enlace de tu aplicación (reemplázalo con tu URL real de Streamlit cuando la tengas a mano)
url_app = "https://share.streamlit.io/" 
texto_compartir = urllib.parse.quote("¡Mira los análisis y gráficos profesionales de Wilfer Trading Pro! 🚀📈 Pruébala aquí:")

whatsapp_url = f"https://api.whatsapp.com/send?text={texto_compartir}%20{url_app}"
telegram_url = f"https://t.me/share/url?url={url_app}&text={texto_compartir}"
twitter_url = f"https://twitter.com/intent/tweet?text={texto_compartir}&url={url_app}"

st.sidebar.markdown(f"💬 [Compartir en WhatsApp]({whatsapp_url})")
st.sidebar.markdown(f"✈️ [Compartir en Telegram]({telegram_url})")
st.sidebar.markdown(f"🐦 [Compartir en X / Twitter]({twitter_url})")

st.sidebar.markdown("---")
st.sidebar.text("Wilfer Trading Pro v1.0")
