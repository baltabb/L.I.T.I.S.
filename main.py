import streamlit as st
import google.generativeai as genai
import PyPDF2
from gtts import gTTS
import os
import base64
from PIL import Image
import tempfile

# 1. Configuración de la página
st.set_page_config(page_title="L.I.T.I.S. - Cristal Zafiro", layout="wide", initial_sidebar_state="expanded")

# --- INYECCIÓN DE DISEÑO CRISTAL ZAFIRO ---
st.markdown("""
<style>
    /* Fondo principal Azul Noche / Gris Plomo */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    /* Tipografías formales y títulos con resplandor */
    h1, h2, h3 {
        color: #58a6ff !important;
        font-family: 'Courier New', Courier, monospace !important;
        text-shadow: 0 0 10px rgba(88,166,255,0.3);
    }
    /* Panel flotante de acceso (vidrio esmerilado) */
    .zafiro-login {
        background: rgba(255, 255, 255, 0.03); /* eco crema casi imperceptible */
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(88, 166, 255, 0.3);
        border-radius: 15px;
        padding: 40px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    /* Botones con bordes iluminados azul eléctrico */
    .stButton>button {
        background-color: #0d1117;
        color: #58a6ff;
        border: 1px solid #58a6ff;
        box-shadow: 0 0 10px rgba(88,166,255,0.2);
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #58a6ff;
        color: #0d1117;
        box-shadow: 0 0 20px rgba(88,166,255,0.6);
    }
    /* Cajas de diálogo de la IA */
    .ia-msg {
        background: rgba(88, 166, 255, 0.05);
        border-left: 4px solid #58a6ff;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 15px;
        font-family: 'Courier New', Courier, monospace;
    }
    /* Caja de Dictamen Rojo Socrático */
    .tinta-roja {
        background: rgba(255, 88, 88, 0.1);
        border-left: 4px solid #ff5858;
        padding: 15px;
        color: #ffb3b3;
        font-family: 'Courier New', Courier, monospace;
        border-radius: 0 8px 8px 0;
    }
</style>
""", unsafe_allow_html=True)
# ------------------------------------------

# 2. Conexión con Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Falta tu GEMINI_API_KEY en los Secrets de Streamlit.")

# 3. Memoria del Sistema
if "acceso" not in st.session_state: st.session_state.acceso = False
if "chat" not in st.session_state: st.session_state.chat = None
if "mensajes" not in st.session_state: st.session_state.mensajes = []
if "expediente_texto" not in st.session_state: st.session_state.expediente_texto = ""

# 4. Motor de Voz (TTS)
def reproducir_voz(texto):
    tts = gTTS(text=texto, lang='es', tld='com.ar')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        with open(fp.name, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio autoplay><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)

# 5. PANTALLA DE ACCESO
if not st.session_state.acceso:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div class='zafiro-login'>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>L.I.T.I.S.</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #8b949e;'>Simulador Jurídico de Élite - Acceso Restringido</p><hr style='border-color: #58a6ff; opacity: 0.3;'>", unsafe_allow_html=True)
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("AUTENTICAR", use_container_width=True):
            if u == "Baltazar" and p == "Litis2026":
                st.session_state.acceso = True
                st.rerun()
            else:
                st.error("Acceso denegado. Credenciales inválidas.")
        st.markdown("</div>", unsafe_allow_html=True)

# 6. LIENZO MULTIMODAL PRINCIPAL
else:
    st.sidebar.markdown("<h2>1. Base de Conocimiento</h2>", unsafe_allow_html=True)
    archivo_pdf = st.sidebar.file_uploader("Subir Expediente (PDF)", type="pdf")
    
    if archivo_pdf and not st.session_state.expediente_texto:
        lector = PyPDF2.PdfReader(archivo_pdf)
        st.session_state.expediente_texto = "".join([pagina.extract_text() for pagina in lector.pages])
        st.sidebar.success("✅ RAG Activo: Expediente en memoria.")

    st.sidebar.markdown("<h2>2. Parámetros Cognitivos</h2>", unsafe_allow_html=True)
    locuacidad = st.sidebar.slider("Locuacidad", 1, 100, 80)
    hostilidad = st.sidebar.slider("Hostilidad", 1, 100, 10)
    prompt = st.sidebar.text_area("System Prompt", "Eres Emilia Martínez y el Juez Virtual. Responde basándote estrictamente en el expediente. Si el fiscal hace una pregunta sugestiva, interrumpe y grita ¡OBJECIÓN!.")
    
    if st.sidebar.button("INICIAR AUDIENCIA ORAL", use_container_width=True):
        instruccion = f"{prompt}\n\nLocuacidad: {locuacidad}%\nHostilidad: {hostilidad}%\n\nEXPEDIENTE:\n{st.session_state.expediente_texto}"
        modelo = genai.GenerativeModel("gemini-1.5-pro", system_instruction=instruccion)
        st.session_state.chat = modelo.start_chat(history=[])
        msg_inicio = "EL JUEZ: Se abre la sesión. Tiene la palabra la fiscalía, usuario Baltazar. Puede comenzar a interrogar a la testigo Emilia Martínez."
        st.session_state.mensajes = [{"role": "model", "content": msg_inicio}]
        reproducir_voz(msg_inicio)

    st.sidebar.markdown("<h2>3. Prueba Gráfica (Visión)</h2>", unsafe_allow_html=True)
    imagen_prueba = st.sidebar.file_uploader("Exhibir documento al estrado", type=["png", "jpg", "jpeg"])

    st.markdown("<h1>Acta de Audiencia - L.I.T.I.S.</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: #58a6ff; opacity: 0.3;'>", unsafe_allow_html=True)
    
    for m in st.session_state.mensajes:
        if m["role"] == "user":
            st.markdown(f"**Baltazar (Fiscal):** {m['content']}")
        else:
            st.markdown(f"<div class='ia-msg'><b>Testigo / Juez:</b><br>{m['content']}</div>", unsafe_allow_html=True)

    pregunta = st.chat_input("Escribe o dicta tu interrogatorio aquí...")
    
    if pregunta and st.session_state.chat:
        st.session_state.mensajes.append({"role": "user", "content": pregunta})
        
        if imagen_prueba:
            img = Image.open(imagen_prueba)
            st.image(img, width=300, caption="[Prueba Documental Exhibida en Sala]")
            respuesta = st.session_state.chat.send_message([pregunta, img])
        else:
            respuesta = st.session_state.chat.send_message(pregunta)
            
        st.session_state.mensajes.append({"role": "model", "content": respuesta.text})
        st.rerun()

    if st.session_state.mensajes and st.session_state.mensajes[-1]["role"] == "model" and len(st.session_state.mensajes) > 1:
        reproducir_voz(st.session_state.mensajes[-1]["content"])

    st.markdown("<br><hr style='border-color: #58a6ff; opacity: 0.3;'>", unsafe_allow_html=True)
    if st.button("🔴 FINALIZAR: GENERAR DICTAMEN SOCRÁTICO"):
        if st.session_state.chat:
            st.markdown("<h2 style='color:#ff5858 !important;'>[ DICTAMEN EN TINTA ROJA ]</h2>", unsafe_allow_html=True)
            auditoria = st.session_state.chat.send_message("LA SIMULACIÓN HA TERMINADO. Actúa como Auditor Evaluador estricto. Genera un dictamen socrático en 3 puntos evaluando exclusivamente mis tácticas de interrogatorio y mi reacción a las objeciones.")
            st.markdown(f"<div class='tinta-roja'>{auditoria.text}</div>", unsafe_allow_html=True)
