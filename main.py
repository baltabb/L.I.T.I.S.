import streamlit as st
import time

# 1. Configuración inicial
st.set_page_config(page_title="L.I.T.I.S. - Acceso Ejecutivo", layout="centered")

# 2. Inyección de CSS Cristal Zafiro Elegante
st.markdown("""
<style>
    /* Fondo principal nocturno */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Panel de Vidrio Esmerilado (Cristal Zafiro) */
    .zafiro-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(88, 166, 255, 0.25);
        border-radius: 12px;
        padding: 40px 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        max-width: 400px;
        margin: 10vh auto 0 auto;
    }

    /* Animación de Carga Minimalista (Anillo Zafiro) */
    .loader {
        border: 3px solid rgba(88, 166, 255, 0.1);
        border-top: 3px solid #58a6ff;
        border-radius: 50%;
        width: 45px;
        height: 45px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Estilo de los campos de texto */
    input {
        background-color: #0d1117 !important;
        color: #58a6ff !important;
        border: 1px solid rgba(88, 166, 255, 0.3) !important;
        border-radius: 6px !important;
    }

    /* Botón ejecutivo */
    .stButton>button {
        background-color: #0d1117;
        color: #58a6ff;
        border: 1px solid #58a6ff;
        border-radius: 6px;
        font-weight: bold;
        letter-spacing: 1px;
        width: 100%;
        transition: all 0.3s ease;
        margin-top: 15px;
    }
    .stButton>button:hover {
        background-color: #58a6ff;
        color: #0d1117;
        box-shadow: 0 0 15px rgba(88,166,255,0.4);
    }
</style>
""", unsafe_allow_html=True)

# 3. Control de Estado
if "acceso" not in st.session_state: st.session_state.acceso = False
if "cargando" not in st.session_state: st.session_state.cargando = False

# 4. PANTALLA 1: Inicio de Sesión
if not st.session_state.acceso:
    st.markdown("<div class='zafiro-card'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#58a6ff; text-align:center; text-shadow: 0 0 10px rgba(88,166,255,0.3);'>L.I.T.I.S.</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#8b949e; font-size: 13px;'>ENTORNO DE SIMULACIÓN JUDICIAL</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: rgba(88,166,255,0.3);'>", unsafe_allow_html=True)
    
    # Lógica de transición animada
    if st.session_state.cargando:
        st.markdown("<div class='loader'></div>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#58a6ff; font-size: 12px;'>Estableciendo conexión encriptada...</p>", unsafe_allow_html=True)
        time.sleep(2) # Pausa de 2 segundos para mostrar la animación
        st.session_state.cargando = False
        st.session_state.acceso = True
        st.rerun()
    else:
        u = st.text_input("Usuario", placeholder="Ingrese su ID")
        p = st.text_input("Contraseña", type="password", placeholder="••••••••")
        
        if st.button("ACCEDER AL ESTRADO"):
            if u == "Baltazar" and p == "Litis2026":
                st.session_state.cargando = True # Activa la animación
                st.rerun()
            else:
                st.error("Credenciales inválidas. Acceso denegado.")
                
    st.markdown("</div>", unsafe_allow_html=True)

# 5. Espacio de transición a la Siguiente Pantalla
else:
    st.success("¡Transición exitosa! El código de la Pantalla 2 se insertará aquí.")
