import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

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

st.sidebar.markdown("---")
st.sidebar.text("Wilfer Trading Pro v1.0")
