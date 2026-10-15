import streamlit as st

# 1. Configuración inicial de la página
st.set_page_config(page_title="L.I.T.I.S. - Acceso", layout="centered")

# 2. Inyección del diseño Cristal Zafiro
st.markdown("""
<style>
    /* Fondo Azul Noche / Gris Plomo */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    /* Tipografía formal y destello azul eléctrico */
    h1 {
        color: #58a6ff !important;
        font-family: 'Courier New', Courier, monospace !important;
        text-align: center;
        text-shadow: 0 0 10px rgba(88,166,255,0.3);
        margin-bottom: 5px;
    }
    /* Panel flotante (Vidrio esmerilado con eco crema) */
    .zafiro-login {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(88, 166, 255, 0.3);
        border-radius: 15px;
        padding: 40px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        max-width: 400px;
        margin: 0 auto;
        margin-top: 10vh;
    }
    /* Botones con resplandor azul */
    .stButton>button {
        background-color: #0d1117;
        color: #58a6ff;
        border: 1px solid #58a6ff;
        border-radius: 8px;
        width: 100%;
        transition: all 0.3s ease;
        margin-top: 15px;
    }
    .stButton>button:hover {
        background-color: #58a6ff;
        color: #0d1117;
        box-shadow: 0 0 20px rgba(88,166,255,0.6);
    }
</style>
""", unsafe_allow_html=True)

# 3. Control de Estado (Memoria)
if "acceso" not in st.session_state:
    st.session_state.acceso = False

# 4. Pantalla 1: Inicio de Sesión
if not st.session_state.acceso:
    st.markdown("<div class='zafiro-login'>", unsafe_allow_html=True)
    st.markdown("<h1>L.I.T.I.S.</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e; font-size: 14px;'>Simulador Jurídico de Élite</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: #58a6ff; opacity: 0.3;'>", unsafe_allow_html=True)
    
    u = st.text_input("Usuario")
    p = st.text_input("Contraseña", type="password")
    
    if st.button("INGRESAR"):
        if u == "Baltazar" and p == "Litis2026":
            st.session_state.acceso = True
            st.rerun()
        else:
            st.error("Acceso denegado. Credenciales inválidas.")
    st.markdown("</div>", unsafe_allow_html=True)

# 5. Espacio reservado para la Pantalla 2 
else:
    st.success("¡Acceso Zafiro concedido! El motor está listo para integrar la Pantalla 2.")
