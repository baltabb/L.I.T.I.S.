import streamlit as st
import time

# Configuración de página
st.set_page_config(page_title="L.I.T.I.S.", layout="centered")

# Inyección de CSS (Clon exacto de la foto Cristal Zafiro)
st.markdown("""
<style>
    /* Fondo radial azul noche exacto al de la foto */
    .stApp {
        background: radial-gradient(circle at center, #1e293b 0%, #0a0f18 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Ocultar elementos por defecto de Streamlit para mayor limpieza */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Contenedor principal de cristal esmerilado */
    .glass-panel {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(138, 180, 248, 0.2);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 12px;
        padding: 50px 40px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        text-align: center;
        max-width: 380px;
        margin: 5vh auto;
    }

    /* Tipografía del título L.I.T.I.S. */
    .title-litis {
        color: #8ab4f8;
        font-size: 46px;
        font-weight: 300;
        letter-spacing: 6px;
        margin-bottom: 5px;
        text-shadow: 0 0 15px rgba(138, 180, 248, 0.5);
    }

    /* Subtítulo SIMULADOR LEGAL */
    .subtitle-litis {
        color: #9aa0a6;
        font-size: 11px;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 35px;
    }

    /* Animación del aro central luminoso */
    .loader-ring {
        width: 70px;
        height: 70px;
        border: 3px solid rgba(138, 180, 248, 0.1);
        border-top: 3px solid #8ab4f8;
        border-radius: 50%;
        animation: spin 1.2s linear infinite;
        margin: 0 auto 35px auto;
        box-shadow: 0 0 20px rgba(138, 180, 248, 0.15);
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Cajas de texto (Usuario / Contraseña) */
    div[data-testid="stTextInput"] input {
        background-color: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: #e8eaed !important;
        border-radius: 6px !important;
        padding: 12px 15px !important;
        font-size: 14px !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #8ab4f8 !important;
        box-shadow: 0 0 8px rgba(138, 180, 248, 0.3) !important;
    }

    /* Botón de Iniciar Sesión */
    div[data-testid="stButton"] button {
        background-color: transparent !important;
        color: #8ab4f8 !important;
        border: 1px solid rgba(138, 180, 248, 0.5) !important;
        border-radius: 6px !important;
        width: 100% !important;
        font-weight: 400 !important;
        letter-spacing: 1px !important;
        margin-top: 15px !important;
        padding: 10px !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stButton"] button:hover {
        background-color: rgba(138, 180, 248, 0.1) !important;
        box-shadow: 0 0 15px rgba(138, 180, 248, 0.4) !important;
        border-color: #8ab4f8 !important;
    }
</style>
""", unsafe_allow_html=True)

# Lógica y Memoria de la sesión
if "acceso" not in st.session_state:
    st.session_state.acceso = False
if "cargando" not in st.session_state:
    st.session_state.cargando = False

# Pantalla 1: Acceso (Clon de la foto)
if not st.session_state.acceso:
    # Contenedor visual
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    st.markdown("<div class='title-litis'>L.I.T.I.S.</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle-litis'>SIMULADOR LEGAL</div>", unsafe_allow_html=True)
    st.markdown("<div class='loader-ring'></div>", unsafe_allow_html=True)

    if st.session_state.cargando:
        st.markdown("<p style='color:#8ab4f8; font-size:12px; margin-top:10px; letter-spacing:1px;'>Autenticando...</p>", unsafe_allow_html=True)
        time.sleep(1.5)
        st.session_state.cargando = False
        st.session_state.acceso = True
        st.rerun()
    else:
        u = st.text_input("Usuario", placeholder="Usuario", label_visibility="collapsed")
        p = st.text_input("Contraseña", type="password", placeholder="Contraseña", label_visibility="collapsed")
        
        if st.button("INICIAR SESIÓN"):
            if u == "Baltazar" and p == "Litis2026":
                st.session_state.cargando = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
    
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Aquí insertaremos la Pantalla 2
    st.success("¡Acceso validado! (Espacio reservado para la Pantalla 2)")
