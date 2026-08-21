import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import urllib.parse

st.set_page_config(page_title="Wilfer Trading Pro", layout="wide")

# Título Principal
st.title("🚀 WILFER TRADING PRO")
st.subheader("Tu Asistente Profesional de Trading en Tiempo Real")

# ==========================================
# 1. GRÁFICO PROFESIONAL DE VELAS
# ==========================================
st.header("📊 Gráfico de Velas Japonesas")
activo_sel = st.selectbox("Selecciona activo para el gráfico:", ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "EURUSD=X"])

with st.spinner("Cargando gráfico profesional..."):
    df = yf.download(activo_sel, period="1mo", interval="1d", progress=False)
    
    if not df.empty:
        # Limpieza de formato para evitar columnas duplicadas
        open_col = df['Open'].iloc[:, 0] if isinstance(df['Open'], pd.DataFrame) else df['Open']
        high_col = df['High'].iloc[:, 0] if isinstance(df['High'], pd.DataFrame) else df['High']
        low_col = df['Low'].iloc[:, 0] if isinstance(df['Low'], pd.DataFrame) else df['Low']
        close_col = df['Close'].iloc[:, 0] if isinstance(df['Close'], pd.DataFrame) else df['Close']

        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=open_col,
            high=high_col,
            low=low_col,
            close=close_col,
            name="Precio"
        )])
        
        # Diseño limpio y profesional (sin panel de volumen abajo para que no se vea doble)
        fig.update_layout(
            template="plotly_dark",
            title=f"Evolución de {activo_sel}",
            xaxis_rangeslider_visible=False,
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No se pudieron cargar los datos del gráfico.")

# ==========================================
# 2. ESCÁNER DE MERCADO
# ==========================================
st.markdown("---")
st.header("🔍 Radar de Mercados")
if st.button("INICIAR ESCÁNER"):
    with st.spinner("Analizando tendencias..."):
        activos_radar = ["BTC-USD", "ETH-USD", "SOL-USD"]
        for act in activos_radar:
            df_rad = yf.download(act, period="5d", interval="15m", progress=False)
            if not df_rad.empty:
                precio_actual = float(df_rad['Close'].iloc[-1].item())
                st.success(f"📈 {act} | Precio actual: {precio_actual:,.2f} USD")

# ==========================================
# 3. CALCULADORA DE GESTIÓN DE RIESGO
# ==========================================
st.markdown("---")
st.header("🧮 Calculadora de Take Profit / Stop Loss")

col1, col2 = st.columns(2)
with col1:
    precio_entrada = st.number_input("Precio de Entrada (USD):", value=50000.0)
    tipo_operacion = st.radio("Tipo de Operación:", ["LONG (Compra)", "SHORT (Venta)"])
with col2:
    porcentaje_ganancia = st.slider("Objetivo de Ganancia (Take Profit %):", 1.0, 20.0, 5.0)
    porcentaje_riesgo = st.slider("Límite de Pérdida (Stop Loss %):", 1.0, 10.0, 2.0)

if st.button("CALCULAR NIVELES"):
    if tipo_operacion == "LONG (Compra)":
        tp = precio_entrada * (1 + (porcentaje_ganancia / 100))
        sl = precio_entrada * (1 - (porcentaje_riesgo / 100))
    else:
        tp = precio_entrada * (1 - (porcentaje_ganancia / 100))
        sl = precio_entrada * (1 + (porcentaje_riesgo / 100))
        
    st.success(f"🎯 **TAKE PROFIT (Meta):** {tp:,.2f} USD")
    st.error(f"🛑 **STOP LOSS (Límite):** {sl:,.2f} USD")

# ==========================================
# 4. BARRA LATERAL - VIRALIZACIÓN
# ==========================================
st.sidebar.header("🌐 ¡Comparte Wilfer Trading Pro!")
st.sidebar.write("Lleva esta herramienta a tus redes y grupos.")

url_app = "https://wilfer-trading-pro-wswpgyfaccxrhg6uyvq4dv.streamlit.app/"
texto_compartir = urllib.parse.quote("¡Mira los gráficos en vivo y la calculadora de Wilfer Trading Pro! 🚀📈 Pruébala aquí:")

whatsapp_url = f"https://api.whatsapp.com/send?text={texto_compartir}%20{url_app}"
telegram_url = f"https://t.me/share/url?url={url_app}&text={texto_compartir}"
twitter_url = f"https://twitter.com/intent/tweet?text={texto_compartir}&url={url_app}"

st.sidebar.markdown(f"💬 [Compartir en WhatsApp]({whatsapp_url})")
st.sidebar.markdown(f"✈️ [Compartir en Telegram]({telegram_url})")
st.sidebar.markdown(f"🐦 [Compartir en Twitter/X]({twitter_url})")

st.sidebar.markdown("---")
st.sidebar.text("Wilfer Trading Pro - Versión Final")
