import streamlit as st
import pandas as pd
import os
import urllib.parse

st.set_page_config(page_title="Wilfer Trading Pro", page_icon="☯️", layout="wide")

# --- LOGOTIPO Y TÍTULO ---
try:
    st.image("logo.wilfer.jpg", width=250)
except:
    st.markdown("<h1 style='text-align: center;'>☯️ WILFER TRADING PRO</h1>", unsafe_allow_html=True)

# --- FUNCIONES DE SEGURIDAD (Bitácora) ---
def cargar_bitacora(file_path):
    columnas = ["P/L", "Activo", "Estado", "Psicologia/Notas"]
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame(columns=columnas)

# --- DICCIONARIO Y BARRA LATERAL ---
TRADUCCIONES = {
    "Español": {"menu": ["Centro de Operaciones", "Calculadora", "Análisis", "Configuración"], "btn": "Registrar"},
    "English": {"menu": ["Operations Center", "Calculator", "Analysis", "Settings"], "btn": "Register"}
}

idioma = st.sidebar.selectbox("🌐 Idioma", ["Español", "English"])
t = TRADUCCIONES[idioma]
tipo_cuenta = st.sidebar.radio("Cuenta:", ["Demo (Virtual)", "Real"])
FILE_PATH = "bitacora_demo.csv" if tipo_cuenta == "Demo (Virtual)" else "bitacora_real.csv"
df = cargar_bitacora(FILE_PATH)

# --- VIRALIZACIÓN EN BARRA LATERAL ---
st.sidebar.markdown("---")
st.sidebar.header("🌐 ¡Comparte Wilfer Trading!")
url_app = "https://wilfer-trading-pro-wswpgyfaccxrhg6uyvq4dv.streamlit.app/"
txt = urllib.parse.quote("¡Mira mi plataforma de Trading Pro!")
st.sidebar.markdown(f"💬 [WhatsApp](https://api.whatsapp.com/send?text={txt}%20{url_app})")
st.sidebar.markdown(f"✈️ [Telegram](https://t.me/share/url?url={url_app}&text={txt})")
st.sidebar.markdown(f"🐦 [Twitter/X](https://twitter.com/intent/tweet?text={txt}&url={url_app})")

# --- NAVEGACIÓN ---
menu = st.sidebar.radio("Ir a:", t["menu"])

# --- CENTRO DE OPERACIONES ---
if menu == t["menu"][0]:
    st.title("🎯 Centro de Operaciones")
    col1, col2, col3 = st.columns(3)
    pl_total = pd.to_numeric(df["P/L"], errors='coerce').fillna(0).sum()
    col1.metric("Capital Actual", f"${10000 + pl_total:,.2f}")
    col2.metric("P/L Neto", f"${pl_total:,.2f}")
    col3.metric("Operaciones", len(df))
    
    with st.form("form"):
        p, a = st.columns(2)
        val_pl = p.number_input("Resultado P/L ($)", value=0.0)
        val_act = a.selectbox("Activo", ["BTC", "EURUSD", "ETH", "NQ", "ES", "GOLD"])
        val_notas = st.text_input("Notas de Psicología")
        if st.form_submit_button("Registrar Operación"):
            nueva = pd.DataFrame({"P/L": [val_pl], "Activo": [val_act], "Estado": ["Ganadora"], "Psicologia/Notas": [val_notas]})
            df = pd.concat([df, nueva], ignore_index=True)
            df.to_csv(FILE_PATH, index=False)
            st.rerun()
    st.dataframe(df, use_container_width=True)

# --- CALCULADORA ---
elif menu == t["menu"][1]:
    st.title("🧮 Calculadora de Riesgo")
    cap = st.number_input("Capital ($)", value=10000.0)
    riesgo = st.number_input("Riesgo (%)", value=1.0)
    st.info(f"Riesgo monetario por trade: ${cap * (riesgo/100):,.2f}")

# --- ANÁLISIS ---
elif menu == t["menu"][2]:
    st.title("📊 Análisis de Rendimiento")
    st.line_chart(pd.to_numeric(df["P/L"], errors='coerce').cumsum())
