import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import os
import urllib.parse

st.set_page_config(page_title="Wilfer Trading Pro", page_icon="☯️", layout="wide")

# --- LOGOTIPO Y TÍTULO ---
try:
    st.image("logo.wilfer.jpg", width=250)
except Exception:
    st.markdown("<h1 style='text-align: center;'>☯️ WILFER TRADING PRO</h1>", unsafe_allow_html=True)

# --- FUNCIONES DE SEGURIDAD PARA LA BITÁCORA ---
def cargar_bitacora(file_path):
    columnas_esperadas = ["P/L", "Activo", "Estado", "Psicologia/Notas"]
    try:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            for col in columnas_esperadas:
                if col not in df.columns:
                    df[col] = ""
            return df
        else:
            return pd.DataFrame(columns=columnas_esperadas)
    except Exception:
        return pd.DataFrame(columns=columnas_esperadas)

# --- CONFIGURACIÓN BARRA LATERAL Y MENÚ ---
st.sidebar.markdown("---")
tipo_cuenta = st.sidebar.radio("Seleccione el Tipo de Cuenta:", ["Demo (Virtual)", "Real"])
FILE_PATH = "bitacora_demo.csv" if tipo_cuenta == "Demo (Virtual)" else "bitacora_real.csv"
capital_inicial = 10000.0 if tipo_cuenta == "Demo (Virtual)" else 1000.0

df = cargar_bitacora(FILE_PATH)
pl_total = pd.to_numeric(df["P/L"], errors='coerce').fillna(0).sum()
balance_total = capital_inicial + pl_total

menu_seleccionado = st.sidebar.radio("Ir a:", [
    "Centro de Operaciones", 
    "Gráfico de Velas en Vivo", 
    "Calculadora de Riesgo", 
    "Análisis de Rendimiento"
])

# --- 1. CENTRO DE OPERACIONES ---
if menu_seleccionado == "Centro de Operaciones":
    st.title("🎯 Centro de Operaciones")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Capital Actual", f"${balance_total:,.2f}")
    col2.metric("P/L Neto Acumulado", f"${pl_total:,.2f}")
    col3.metric("Total Operaciones", len(df))
    
    with st.form("form_operacion"):
        st.subheader("📝 Registrar Nueva Operación")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            pl_input = st.number_input("Resultado P/L ($)", value=0.0, step=10.0)
            activo_input = st.selectbox("Activo / Mercado", ["BTC", "EURUSD", "ETH", "NQ", "ES", "GOLD"])
        with col_f2:
            estado_input = st.selectbox("Resultado", ["Ganadora", "Perdedora", "BreakEven"])
            notas_input = st.text_input("Notas de Psicología / Configuración")
            
        if st.form_submit_button("Registrar Operación con Notas"):
            try:
                nueva_fila = pd.DataFrame({
                    "P/L": [pl_input], 
                    "Activo": [activo_input], 
                    "Estado": [estado_input],
                    "Psicologia/Notas": [notas_input]
                })
                df = pd.concat([df, nueva_fila], ignore_index=True)
                df.to_csv(FILE_PATH, index=False)
                st.success("¡Operación registrada con éxito!")
                st.rerun()
            except Exception as e:
                st.error(f"Error al guardar: {e}")
            
    st.markdown("---")
    st.subheader("📋 Historial de Operaciones y Psicología")
    if len(df) > 0:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No hay operaciones registradas todavía.")

# --- 2. GRÁFICO DE VELAS EN VIVO ---
elif menu_seleccionado == "Gráfico de Velas en Vivo":
    st.title("📊 Gráfico de Velas Japonesas")
    activo_sel = st.selectbox("Selecciona activo para el gráfico:", ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "EURUSD=X"])

    with st.spinner("Cargando gráfico profesional..."):
        df_graf = yf.download(activo_sel, period="1mo", interval="1d", progress=False)
        if not df_graf.empty:
            open_c = df_graf['Open'].iloc[:, 0] if isinstance(df_graf['Open'], pd.DataFrame) else df_graf['Open']
            high_c = df_graf['High'].iloc[:, 0] if isinstance(df_graf['High'], pd.DataFrame) else df_graf['High']
            low_c = df_graf['Low'].iloc[:, 0] if isinstance(df_graf['Low'], pd.DataFrame) else df_graf['Low']
            close_c = df_graf['Close'].iloc[:, 0] if isinstance(df_graf['Close'], pd.DataFrame) else df_graf['Close']

            fig = go.Figure(data=[go.Candlestick(
                x=df_graf.index, open=open_c, high=high_c, low=low_c, close=close_c
            )])
            fig.update_layout(
                template="plotly_dark",
                title=f"Evolución y Precios de {activo_sel}",
                height=550,
                xaxis_rangeslider_visible=False,
                yaxis=dict(showticklabels=True, side="right")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("No se pudieron cargar los datos del gráfico.")

# --- 3. CALCULADORA DE RIESGO ---
elif menu_seleccionado == "Calculadora de Riesgo":
    st.title("🧮 Calculadora de Posición y Riesgo")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        cap = st.number_input("Capital disponible ($)", value=balance_total)
        riesgo = st.number_input("Riesgo por operación (%)", value=1.0)
    with col_c2:
        stop = st.number_input("Distancia al Stop Loss ($)", value=100.0)
        take_profit = st.number_input("Distancia al Take Profit ($)", value=200.0)
    if st.button("Calcular Tamaño y Beneficio"):
        cantidad = (cap * (riesgo/100)) / stop if stop > 0 else 0
        beneficio_potencial = cantidad * take_profit
        ratio_rr = take_profit / stop if stop > 0 else 0
        st.success(f"📌 Tamaño recomendado: **{cantidad:.4f} unidades**")
        st.info(f"🎯 Beneficio: **${beneficio_potencial:,.2f}** | Ratio: **1:{ratio_rr:.2f}**")

# --- 4. ANÁLISIS DE RENDIMIENTO ---
elif menu_seleccionado == "Análisis de Rendimiento":
    st.title("📊 Análisis de Rendimiento")
    if len(df) > 0:
        st.dataframe(df, use_container_width=True)
        st.subheader("Evolución del P/L Acumulado")
        st.line_chart(pd.to_numeric(df["P/L"], errors='coerce').cumsum())
    else:
        st.info("Aún no hay operaciones para analizar.")

# --- BARRA LATERAL DE VIRALIZACIÓN ---
st.sidebar.markdown("---")
st.sidebar.header("🌐 ¡Comparte Wilfer Trading!")
url_app = "https://wilfer-trading-pro-wswpgyfaccxrhg6uyvq4dv.streamlit.app/"
texto_compart = urllib.parse.quote("¡Mira mi plataforma Wilfer Trading Pro con gráficos en vivo y bitácora!")
st.sidebar.markdown(f"💬 [WhatsApp](https://api.whatsapp.com/send?text={texto_compart}%20{url_app})")
st.sidebar.markdown(f"✈️ [Telegram](https://t.me/share/url?url={url_app}&text={texto_compart})")
st.sidebar.markdown(f"🐦 [Twitter/X](https://twitter.com/intent/tweet?text={texto_compart}&url={url_app})")
