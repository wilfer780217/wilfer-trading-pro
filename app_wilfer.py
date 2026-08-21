import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import urllib.parse

# Configuración de la página
st.set_page_config(page_title="Wilfer Trading Pro", layout="centered")

# Mostrar logo y títulos
st.image("logo.wilfer.jpg", width=400)
st.title("🚀 WILFER TRADING PRO")
st.subheader("Tu Asistente Profesional de Trading")

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

# SECCIÓN 1: RADAR DE MERCADOS
st.markdown("---")
st.header("🔍 Radar de Mercados en Tiempo Real")
if st.button("INICIAR ESCÁNER"):
    with st.spinner("Analizando activos..."):
        for activo in ACTIVOS:
            ticker = yf.Ticker(activo)
            df = ticker.history(period="5d", interval="15m")
            if not df.empty:
                df = calcular_indicadores(df)
                ultimo = df.iloc[-1]
                
                if ultimo['Close'] > ultimo['EMA50'] and ultimo['RSI'] < 40:
                    st.success(f"{activo}: SEÑAL LONG (Alcista) - Precio: {ultimo['Close']:.2f}")
                elif ultimo['Close'] < ultimo['EMA50'] and ultimo['RSI'] > 60:
                    st.error(f"{activo}: SEÑAL SHORT (Bajista) - Precio: {ultimo['Close']:.2f}")
                else:
                    st.info(f"{activo}: Precio {ultimo['Close']:.2f} | Monitoreando...")

# SECCIÓN 2: GRÁFICOS PROFESIONALES
st.markdown("---")
st.header("📊 Gráfico Interactivo de Activos")
activo_seleccionado = st.selectbox("Selecciona un activo para ver el gráfico:", ACTIVOS)

with st.spinner("Cargando gráfico..."):
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

# SECCIÓN 3: CALCULADORA DE GESTIÓN DE RIESGO (TAKE PROFIT / STOP LOSS)
st.markdown("---")
st.header("🧮 Calculadora de Take Profit / Stop Loss")
precio_entrada = st.number_input("Precio de Entrada (USD):", value=100.0)
tipo_operacion = st.radio("Tipo de Operación:", ["LONG (Compra)", "SHORT (Venta)"])
porcentaje_ganancia = st.slider("Objetivo de Ganancia (%):", 1.0, 20.0, 5.0)
porcentaje_riesgo = st.slider("Riesgo / Stop Loss (%):", 1.0, 10.0, 2.0)

if st.button("CALCULAR NIVELES"):
    if tipo_operacion == "LONG (Compra)":
        tp = precio_entrada * (1 + (porcentaje_ganancia / 100))
        sl = precio_entrada * (1 - (porcentaje_riesgo / 100))
    else:
        tp = precio_entrada * (1 - (porcentaje_ganancia / 100))
        sl = precio_entrada * (1 + (porcentaje_riesgo / 100))
        
    st.success(f"🎯 **Take Profit (Meta):** {tp:.2f} USD")
    st.error(f"🛑 **Stop Loss (Límite de pérdida):** {sl:.2f} USD")

# SECCIÓN 4: BARRA LATERAL CON VIRALIZACIÓN
st.sidebar.markdown("---")
st.sidebar.subheader("🌐 ¡Comparte Wilfer Trading Pro!")
st.sidebar.write("Ayuda a que más traders conozcan la plataforma.")

url_app = "https://wilfer-trading-pro-wswpgyfaccxrhg6uyvq4dv.streamlit.app/"
texto_compartir = urllib.parse.quote("¡Mira los análisis y gráficos profesionales de Wilfer Trading Pro! 🚀📈 Pruébala aquí:")

whatsapp_url = f"https://api.whatsapp.com/send?text={texto_compartir}%20{url_app}"
telegram_url = f"https://t.me/share/url?url={url_app}&text={texto_compartir}"
twitter_url = f"https://twitter.com/intent/tweet?text={texto_compartir}&url={url_app}"

st.sidebar.markdown(f"💬 [Compartir en WhatsApp]({whatsapp_url})")
st.sidebar.markdown(f"✈️ [Compartir en Telegram]({telegram_url})")
st.sidebar.markdown(f"🐦 [Compartir en X / Twitter]({twitter_url})")

st.sidebar.markdown("---")
st.sidebar.text("Wilfer Trading Pro v1.0")
