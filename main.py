import streamlit as st

# Configuración de página
st.set_page_config(page_title="L.I.T.I.S.", layout="centered")

# CSS Simplificado y Funcional (Diseño Cristal Zafiro puro)
st.markdown("""
<style>
    /* Fondo radial azul noche */
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
        padding: 40px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        text-align: center;
        max-width: 400px;
        margin: 5vh auto;
    }

    /* Títulos */
    .title-litis {
        color: #8ab4f8;
        font-size: 46px;
        font-weight: 300;
        letter-spacing: 6px;
        margin-bottom: 5px;
        text-shadow: 0 0 15px rgba(138, 180, 248, 0.5);
    }

    .subtitle-litis {
        color: #9aa0a6;
        font-size: 11px;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 30px;
    }

    /* Botón Zafiro */
    .stButton > button {
        background-color: transparent !important;
        color: #8ab4f8 !important;
        border: 1px solid rgba(138, 180, 248, 0.5) !important;
        border-radius: 6px !important;
        width: 100% !important;
        padding: 10px !important;
        transition: all 0.3s ease !important;
        margin-top: 10px;
    }

    .stButton > button:hover {
        background-color: rgba(138, 180, 248, 0.1) !important;
        box-shadow: 0 0 15px rgba(138, 180, 248, 0.4) !important;
        border-color: #8ab4f8 !important;
    }
</style>
""", unsafe_allow_html=True)

# Control de sesión
if "acceso" not in st.session_state:
    st.session_state.acceso = False

# Pantalla 1: Acceso
if not st.session_state.acceso:
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='title-litis'>L.I.T.I.S.</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle-litis'>SIMULADOR LEGAL</div>", unsafe_allow_html=True)
    
    # Inputs nativos 100% funcionales
    u = st.text_input("Usuario")
    p = st.text_input("Contraseña", type="password")
    
    if st.button("INICIAR SESIÓN"):
        if u == "Baltazar" and p == "Litis2026":
            st.session_state.acceso = True
            st.rerun()
        else:
            st.error("Credenciales incorrectas")
            
    st.markdown("</div>", unsafe_allow_html=True)

# Pantalla 2: El Estrado (Borrador temporal)
else:
    st.success("¡Acceso validado! (Aquí insertaremos el código de la Pantalla 2)")
