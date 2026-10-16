import streamlit as st

# 1. Configuración de página obligatoria al inicio
st.set_page_config(page_title="L.I.T.I.S.", layout="centered")

# 2. CSS Súper Limpio y Estable
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    
    .titulo-litis { 
        text-align: center; color: #58a6ff; font-family: 'Courier New', Courier, monospace; 
        font-size: 55px; font-weight: bold; text-shadow: 0 0 15px rgba(88,166,255,0.6); 
        margin-top: 20px; margin-bottom: 0px; 
    }
    
    .subtitulo { 
        text-align: center; color: #8b949e; letter-spacing: 4px; font-size: 14px; 
        margin-bottom: 40px; 
    }
    
    /* Forzar fondo oscuro en los recuadros de texto */
    div[data-testid="stTextInput"] > div > div > input {
        background-color: #161b22 !important; color: #58a6ff !important; 
        border: 1px solid #30363d !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Memoria Segura
if "acceso_permitido" not in st.session_state:
    st.session_state.acceso_permitido = False

# 4. Pantalla 1: Formulario de Acceso Blindado
if not st.session_state.acceso_permitido:
    st.markdown("<p class='titulo-litis'>L.I.T.I.S.</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitulo'>SIMULADOR JUDICIAL DE ÉLITE</p>", unsafe_allow_html=True)
    
    # El formulario evita que Streamlit se congele al escribir
    with st.form("formulario_acceso", clear_on_submit=False):
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")
        
        # Botón nativo de submit
        ingresar = st.form_submit_button("INICIAR SESIÓN")
        
        if ingresar:
            if usuario == "Baltazar" and clave == "Litis2026":
                st.session_state.acceso_permitido = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas. Verifique su usuario y contraseña.")

# 5. Transición Segura
else:
    st.success("¡Acceso concedido! El motor funciona perfectamente. Listo para Pantalla 2.")
