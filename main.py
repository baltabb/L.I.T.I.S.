import streamlit as st

# Configuración de página
st.set_page_config(page_title="L.I.T.I.S.", layout="centered")

# CSS para eliminar recuadros vacíos y resaltar el título
st.markdown("""
<style>
    /* Eliminar el recuadro superior y ocultar elementos por defecto de Streamlit */
    .block-container {
        padding-top: 2rem !important;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Fondo radial azul noche puro */
    .stApp {
        background: radial-gradient(circle at center, #1e293b 0%, #0a0f18 100%);
        font-family: 'Segoe UI', Tahoma, sans-serif;
    }
    
    /* Contenedor de cristal esmerilado */
    .glass-panel {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(138, 180, 248, 0.2);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 12px;
        padding: 50px 40px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        text-align: center;
        max-width: 400px;
        margin: 0 auto; 
    }

    /* TÍTULO L.I.T.I.S. RESALTADO */
    .title-litis {
        color: #8ab4f8;
        font-size: 58px; /* Tamaño mucho más grande */
        font-weight: 700; /* Letra más gruesa */
        letter-spacing: 8px;
        margin-bottom: 5px;
        text-shadow: 0 0 25px rgba(138, 180, 248, 0.8), 0 0 10px rgba(255,255,255,0.4); /* Resplandor doble */
    }

    .subtitle-litis {
        color: #9aa0a6;
        font-size: 12px;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-bottom: 30px;
    }

    /* Inputs ocultando el label para que no dejen espacios en blanco */
    div[data-testid="stTextInput"] label {
        display: none !important;
    }
    div[data-testid="stTextInput"] input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: #e8eaed !important;
        border-radius: 6px !important;
        padding: 12px 15px !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #8ab4f8 !important;
        box-shadow: 0 0 8px rgba(138, 180, 248, 0.3) !important;
    }

    /* Botón Zafiro */
    .stButton > button {
        background-color: transparent !important;
        color: #8ab4f8 !important;
        border: 1px solid rgba(138, 180, 248, 0.5) !important;
        border-radius: 6px !important;
        width: 100% !important;
        padding: 12px !important;
        font-weight: bold !important;
        letter-spacing: 1.5px !important;
        transition: all 0.3s ease !important;
        margin-top: 15px;
    }
    .stButton > button:hover {
        background-color: rgba(138, 180, 248, 0.1) !important;
        box-shadow: 0 0 15px rgba(138, 180, 248, 0.4) !important;
        border-color: #8ab4f8 !important;
    }
</style>
""", unsafe_allow_html=True)

# Memoria de sesión
if "acceso" not in st.session_state:
    st.session_state.acceso = False

# Pantalla 1: Acceso
if not st.session_state.acceso:
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='title-litis'>L.I.T.I.S.</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle-litis'>SIMULADOR LEGAL</div>", unsafe_allow_html=True)
    
    # Text inputs limpios
    u = st.text_input("Usuario", placeholder="Usuario")
    p = st.text_input("Contraseña", type="password", placeholder="Contraseña")
    
    if st.button("INICIAR SESIÓN"):
        if u == "Baltazar" and p == "Litis2026":
            st.session_state.acceso = True
            st.rerun()
        else:
            st.error("Credenciales incorrectas")
            
    st.markdown("</div>", unsafe_allow_html=True)

# Pantalla 2 (En construcción)
else:
    st.success("¡Acceso validado y diseño limpio! (Aquí insertaremos la Pantalla 2)")
