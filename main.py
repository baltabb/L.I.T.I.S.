import streamlit as st
import google.generativeai as genai
import PyPDF2
from gtts import gTTS
import os
import base64
from PIL import Image
import tempfile

# 1. Configuración de la Interfaz
st.set_page_config(page_title="L.I.T.I.S. - Motor Completo", layout="wide")

# 2. Conexión con Gemini (Requiere tu clave en Secrets como GEMINI_API_KEY)
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("Por favor, agrega GEMINI_API_KEY en los secretos (Secrets) de Streamlit.")

# 3. Memoria del Sistema
if "acceso" not in st.session_state: st.session_state.acceso = False
if "chat" not in st.session_state: st.session_state.chat = None
if "mensajes" not in st.session_state: st.session_state.mensajes = []
if "expediente_texto" not in st.session_state: st.session_state.expediente_texto = ""

# 4. Función de Voz (Text-to-Speech)
def reproducir_voz(texto):
    tts = gTTS(text=texto, lang='es', tld='com.ar')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        with open(fp.name, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio autoplay><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)

# 5. Pantalla de Acceso (Usuario Baltazar)
if not st.session_state.acceso:
    st.markdown("<h1 style='text-align: center; color: #58a6ff; font-family: Courier;'>L.I.T.I.S.</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e;'>Acceso Restringido - Ingrese sus credenciales</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.button("INGRESAR"):
            if u == "Baltazar" and p == "Litis2026":
                st.session_state.acceso = True
                st.rerun()
            else:
                st.error("Credenciales inválidas.")

# 6. El Simulador Principal
else:
    st.sidebar.title("1. Expediente (RAG)")
    archivo_pdf = st.sidebar.file_uploader("Subir PDF", type="pdf")
    
    if archivo_pdf and not st.session_state.expediente_texto:
        lector = PyPDF2.PdfReader(archivo_pdf)
        st.session_state.expediente_texto = "".join([pagina.extract_text() for pagina in lector.pages])
        st.sidebar.success("Expediente indexado en la memoria.")

    st.sidebar.title("2. Configurar Testigo")
    locuacidad = st.sidebar.slider("Locuacidad", 1, 100, 80)
    prompt = st.sidebar.text_area("System Prompt", "Eres Emilia Martínez. Responde basándote estrictamente en el expediente. Si me hacen una pregunta compuesta o sugestiva, actúa como el Juez y grita ¡OBJECIÓN!.")
    
    if st.sidebar.button("INICIAR AUDIENCIA"):
        instruccion = f"{prompt}\n\nLocuacidad: {locuacidad}%\n\nEXPEDIENTE:\n{st.session_state.expediente_texto}"
        modelo = genai.GenerativeModel("gemini-1.5-pro", system_instruction=instruccion)
        st.session_state.chat = modelo.start_chat(history=[])
        msg_inicio = "Se abre la sesión. Tiene la palabra la fiscalía. Puede comenzar a interrogar."
        st.session_state.mensajes = [{"role": "model", "content": msg_inicio}]
        reproducir_voz(msg_inicio)

    st.sidebar.title("3. Subir Pruebas (Visión)")
    imagen_prueba = st.sidebar.file_uploader("Exhibir documento gráfico", type=["png", "jpg", "jpeg"])

    st.title("Acta de Audiencia - Papel Calco")
    
    for m in st.session_state.mensajes:
        if m["role"] == "user":
            st.markdown(f"**Baltazar:** {m['content']}")
        else:
            st.markdown(f"<div style='background-color:#1e1e1e; padding:10px; border-left: 4px solid #d73a49;'><b>Testigo/Juez:</b> {m['content']}</div>", unsafe_allow_html=True)

    pregunta = st.chat_input("Escribe o dicta tu pregunta...")
    
    if pregunta and st.session_state.chat:
        st.session_state.mensajes.append({"role": "user", "content": pregunta})
        
        if imagen_prueba:
            img = Image.open(imagen_prueba)
            st.image(img, width=250, caption="Prueba exhibida en sala")
            respuesta = st.session_state.chat.send_message([pregunta, img])
        else:
            respuesta = st.session_state.chat.send_message(pregunta)
            
        st.session_state.mensajes.append({"role": "model", "content": respuesta.text})
        st.rerun()

    if st.session_state.mensajes and st.session_state.mensajes[-1]["role"] == "model" and len(st.session_state.mensajes) > 1:
        reproducir_voz(st.session_state.mensajes[-1]["content"])

    st.markdown("---")
    if st.button("🔴 GENERAR DICTAMEN SOCRÁTICO"):
        if st.session_state.chat:
            st.markdown("<h3 style='color:#d73a49; font-family: Courier;'>DICTAMEN EN TINTA ROJA</h3>", unsafe_allow_html=True)
            auditoria = st.session_state.chat.send_message("Genera un dictamen socrático en 3 puntos evaluando mis tácticas de interrogatorio y el manejo de las objeciones.")
            st.error(auditoria.text)
