import base64
import hashlib
import json
import os
from copy import deepcopy
from io import BytesIO

import streamlit as st
from gtts import gTTS
from PIL import Image

from demo_case import DEFAULT_WITNESS_INSTRUCTIONS, DEMO_CASE_PAGES, DEMO_CASE_TITLE
from hearing_archive import deserialize_hearing, serialize_hearing
from litis_engine import (
    CHAT_MODEL,
    EMBEDDING_MODEL,
    MAX_PDF_BYTES,
    analyze_hearing,
    build_rag_index,
    create_client,
    extract_pdf_pages,
    retrieve_chunks,
    generate_witness_response,
)

MAX_IMAGE_BYTES = 5 * 1024 * 1024

st.set_page_config(page_title="L.I.T.I.S. — Simulador de audiencia", layout="wide")


def get_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key:
        return key
    try:
        return str(st.secrets.get("GEMINI_API_KEY", "")).strip()
    except Exception:
        return ""


def document_signature(pages: list[dict]) -> str:
    content = "\n".join(f"{page['page']}:{page['text']}" for page in pages)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def reset_to_demo() -> None:
    preserved_archive_digest = st.session_state.get("last_archive_digest", "")
    st.session_state.pages = deepcopy(DEMO_CASE_PAGES)
    st.session_state.case_title = DEMO_CASE_TITLE
    st.session_state.rag_chunks = []
    st.session_state.index_signature = ""
    st.session_state.messages = []
    st.session_state.analysis = ""
    st.session_state.analysis_sources = []
    st.session_state.hearing_started = False
    st.session_state.evidence_attachment = None
    st.session_state.last_error = ""
    st.session_state.last_archive_digest = preserved_archive_digest


def replace_document(pages: list[dict], title: str) -> None:
    st.session_state.pages = pages
    st.session_state.case_title = title
    st.session_state.rag_chunks = []
    st.session_state.index_signature = ""
    st.session_state.messages = []
    st.session_state.analysis = ""
    st.session_state.analysis_sources = []
    st.session_state.hearing_started = False
    st.session_state.last_error = ""


def normalize_image(uploaded_file) -> dict:
    raw = uploaded_file.getvalue()
    if len(raw) > MAX_IMAGE_BYTES:
        raise ValueError("La imagen supera el límite de 5 MB.")
    try:
        with Image.open(BytesIO(raw)) as image:
            image.load()
            normalized = image.convert("RGB")
            output = BytesIO()
            normalized.save(output, format="JPEG", quality=88, optimize=True)
    except Exception as error:
        raise ValueError(
            "No se pudo leer la imagen. Usá un archivo JPEG, PNG o WebP."
        ) from error
    return {
        "name": uploaded_file.name[:200],
        "mime_type": "image/jpeg",
        "data_base64": base64.b64encode(output.getvalue()).decode("ascii"),
    }


def restore_archive(data: dict) -> None:
    st.session_state.pages = data["pages"]
    st.session_state.case_title = data["case_title"]
    st.session_state.rag_chunks = data["rag_chunks"]
    st.session_state.index_signature = (
        document_signature(data["pages"])
        if data["rag_chunks"] and data["embedding_model"] == EMBEDDING_MODEL
        else ""
    )
    if not st.session_state.index_signature:
        st.session_state.rag_chunks = []
    st.session_state.messages = data["messages"]
    st.session_state.analysis = data["analysis"]
    st.session_state.analysis_sources = []
    st.session_state.evidence_attachment = data["evidence_attachment"]
    st.session_state.instructions = (
        data["settings"]["instructions"] or DEFAULT_WITNESS_INSTRUCTIONS
    )
    st.session_state.locuacidad = data["settings"]["locuacidad"]
    st.session_state.hearing_started = data["settings"]["hearing_started"] and bool(
        st.session_state.rag_chunks
    )
    st.session_state.last_error = ""


def initialize_state() -> None:
    defaults = {
        "pages": deepcopy(DEMO_CASE_PAGES),
        "case_title": DEMO_CASE_TITLE,
        "rag_chunks": [],
        "index_signature": "",
        "messages": [],
        "analysis": "",
        "analysis_sources": [],
        "instructions": DEFAULT_WITNESS_INSTRUCTIONS,
        "locuacidad": 65,
        "hearing_started": False,
        "evidence_attachment": None,
        "last_error": "",
        "last_archive_digest": "",
        "active_pdf_digest": "",
        "active_image_digest": "",
        "include_evidence": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = deepcopy(value)


initialize_state()
api_key = get_api_key()
client = create_client(api_key) if api_key else None

st.title("L.I.T.I.S.")
st.subheader("Simulador didáctico de audiencia")
st.caption(
    "Demo con expedientes ficticios. Las preguntas, los fragmentos recuperados y las imágenes "
    "que adjuntes se envían a Gemini para responder."
)
st.info(
    "No uses expedientes reales ni confidenciales en esta versión. "
    "Las audiencias se guardan descargando un archivo JSON y se retoman importándolo."
)

if not api_key:
    st.warning(
        "Falta GEMINI_API_KEY. En Replit, agregala en Secrets; en Streamlit Community Cloud, "
        "cargala en los secretos de la app."
    )

with st.sidebar:
    st.header("Expediente")
    pdf_upload = st.file_uploader(
        "Subir un PDF con texto",
        type=["pdf"],
        help="Límite de demo: 12 MB y 80 páginas. Los PDF escaneados requieren OCR.",
        key="pdf_upload",
    )
    if pdf_upload is not None:
        pdf_bytes = pdf_upload.getvalue()
        pdf_digest = hashlib.sha256(pdf_bytes).hexdigest()
        if pdf_digest != st.session_state.active_pdf_digest:
            st.session_state.active_pdf_digest = pdf_digest
            try:
                extracted_pages = extract_pdf_pages(pdf_bytes)
                replace_document(extracted_pages, pdf_upload.name)
                st.success(f"Leído: {len(extracted_pages)} páginas con texto.")
            except ValueError as error:
                st.error(str(error))

    if st.button("Cargar el caso ficticio de muestra", use_container_width=True):
        reset_to_demo()
        st.rerun()

    st.caption(f"Expediente activo: **{st.session_state.case_title}**")
    st.caption(f"Páginas con texto: {len(st.session_state.pages)}")

    st.divider()
    st.header("Evidencia visual")
    image_upload = st.file_uploader(
        "Adjuntar imagen (JPEG, PNG o WebP)",
        type=["jpg", "jpeg", "png", "webp"],
        key="image_upload",
    )
    if image_upload is not None:
        image_digest = hashlib.sha256(image_upload.getvalue()).hexdigest()
        if image_digest != st.session_state.active_image_digest:
            st.session_state.active_image_digest = image_digest
            try:
                st.session_state.evidence_attachment = normalize_image(image_upload)
            except ValueError as error:
                st.error(str(error))
                st.session_state.evidence_attachment = None

    if st.session_state.evidence_attachment:
        image_bytes = base64.b64decode(
            st.session_state.evidence_attachment["data_base64"], validate=True
        )
        st.image(image_bytes, caption=st.session_state.evidence_attachment["name"])
        st.checkbox(
            "Adjuntar esta imagen a las próximas preguntas",
            key="include_evidence",
        )

    st.divider()
    st.header("Testigo")
    st.slider("Locuacidad", 1, 100, key="locuacidad")
    st.text_area("Instrucciones de actuación", key="instructions", height=150)

    current_signature = document_signature(st.session_state.pages)
    index_ready = (
        bool(st.session_state.rag_chunks)
        and st.session_state.index_signature == current_signature
    )
    if index_ready and st.session_state.hearing_started:
        st.success("RAG listo; audiencia en curso.")
    else:
        if st.button(
            "Preparar RAG e iniciar audiencia",
            type="primary",
            use_container_width=True,
            disabled=client is None or not st.session_state.pages,
        ):
            try:
                with st.spinner("Indexando el expediente con Gemini…"):
                    chunks = build_rag_index(client, st.session_state.pages)
                st.session_state.rag_chunks = chunks
                st.session_state.index_signature = current_signature
                st.session_state.hearing_started = True
                if not st.session_state.messages:
                    st.session_state.messages = [
                        {
                            "role": "assistant",
                            "content": (
                                "Se abre la audiencia ficticia. Tiene la palabra la fiscalía; "
                                "puede comenzar a interrogar."
                            ),
                            "sources": [],
                            "image_name": "",
                        }
                    ]
                st.session_state.last_error = ""
                st.rerun()
            except Exception:
                st.session_state.last_error = (
                    "No se pudo indexar el expediente. Revisá la clave, la conexión y el tamaño "
                    "del documento."
                )

    if st.session_state.last_error:
        st.error(st.session_state.last_error)

    st.divider()
    st.header("Guardar o retomar")
    archive_upload = st.file_uploader(
        "Importar audiencia (.json)",
        type=["json"],
        key="archive_upload",
    )
    if archive_upload is not None:
        archive_bytes = archive_upload.getvalue()
        archive_digest = hashlib.sha256(archive_bytes).hexdigest()
        if archive_digest != st.session_state.last_archive_digest:
            st.session_state.last_archive_digest = archive_digest
            try:
                restore_archive(deserialize_hearing(archive_bytes))
                st.success("Audiencia importada.")
                st.rerun()
            except ValueError as error:
                st.error(str(error))

    if st.session_state.messages:
        try:
            export_bytes = serialize_hearing(
                {
                    "case_title": st.session_state.case_title,
                    "pages": st.session_state.pages,
                    "rag_chunks": st.session_state.rag_chunks,
                    "messages": st.session_state.messages,
                    "analysis": st.session_state.analysis,
                    "settings": {
                        "instructions": st.session_state.instructions,
                        "locuacidad": st.session_state.locuacidad,
                        "hearing_started": st.session_state.hearing_started,
                    },
                    "evidence_attachment": st.session_state.evidence_attachment,
                    "embedding_model": EMBEDDING_MODEL,
                }
            )
            st.download_button(
                "Descargar audiencia",
                data=export_bytes,
                file_name="litis-audiencia.json",
                mime="application/json",
                use_container_width=True,
            )
        except ValueError as error:
            st.warning(str(error))

    if st.button("Nueva audiencia", use_container_width=True):
        reset_to_demo()
        st.rerun()

st.markdown(f"### {st.session_state.case_title}")

if not st.session_state.hearing_started:
    st.info(
        "El caso ficticio de muestra ya está cargado. Prepará el índice RAG desde la barra "
        "lateral para iniciar; también podés reemplazarlo por un PDF con texto."
    )

if st.session_state.last_error:
    st.error(st.session_state.last_error)

for message in st.session_state.messages:
    role = "assistant" if message.get("role") in {"assistant", "model"} else "user"
    with st.chat_message(role):
        st.markdown(message.get("content", ""))
        sources = message.get("sources", [])
        if sources:
            st.caption("Fuentes recuperadas: " + ", ".join(sources))
        if message.get("image_name"):
            st.caption(f"Evidencia visual adjunta: {message['image_name']}")

question = st.chat_input(
    "Escribí una pregunta para la audiencia…",
    disabled=client is None or not st.session_state.hearing_started,
)
if question:
    st.session_state.messages.append(
        {"role": "user", "content": question, "sources": [], "image_name": ""}
    )
    try:
        with st.spinner("Buscando evidencia y preparando la respuesta…"):
            retrieved = retrieve_chunks(
                client, st.session_state.rag_chunks, question, top_k=4
            )
            image_bytes = None
            image_mime_type = None
            image_name = ""
            if (
                st.session_state.include_evidence
                and st.session_state.evidence_attachment
            ):
                attachment = st.session_state.evidence_attachment
                image_bytes = base64.b64decode(attachment["data_base64"], validate=True)
                image_mime_type = attachment["mime_type"]
                image_name = attachment["name"]
            answer = generate_witness_response(
                client=client,
                instructions=st.session_state.instructions,
                messages=st.session_state.messages[:-1],
                question=question,
                evidence_chunks=retrieved,
                temperature=0.15 + (st.session_state.locuacidad / 100) * 0.75,
                image_bytes=image_bytes,
                image_mime_type=image_mime_type,
            )
        sources = list(dict.fromkeys(f"p. {chunk['page']}" for chunk in retrieved))
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources,
                "image_name": image_name,
            }
        )
        st.session_state.analysis = ""
        st.session_state.last_error = ""
    except Exception:
        st.session_state.last_error = (
            "No se pudo completar la respuesta. Revisá el estado de la API de Gemini "
            "y volvé a intentar."
        )
    st.rerun()

if st.session_state.analysis:
    st.subheader("Dictamen socrático")
    st.markdown(st.session_state.analysis)
    if st.session_state.analysis_sources:
        st.caption(
            "Fuentes consideradas: " + ", ".join(st.session_state.analysis_sources)
        )

has_exchange = any(
    message.get("role") == "user" for message in st.session_state.messages
)
if has_exchange and st.session_state.hearing_started:
    if st.button("Generar análisis de la audiencia", type="primary"):
        try:
            with st.spinner("Analizando el interrogatorio y las fuentes…"):
                analysis_evidence = retrieve_chunks(
                    client,
                    st.session_state.rag_chunks,
                    "inconsistencias, cronología y respaldo documental de la audiencia",
                    top_k=8,
                )
                st.session_state.analysis = analyze_hearing(
                    client, st.session_state.messages, analysis_evidence
                )
                st.session_state.analysis_sources = list(
                    dict.fromkeys(f"p. {chunk['page']}" for chunk in analysis_evidence)
                )
                st.session_state.last_error = ""
            st.rerun()
        except Exception:
            st.session_state.last_error = "No se pudo generar el análisis. Revisá la conexión con Gemini y volvé a intentar."
            st.rerun()

latest_assistant = next(
    (
        message
        for message in reversed(st.session_state.messages)
        if message.get("role") in {"assistant", "model"}
    ),
    None,
)
if latest_assistant and client is not None:
    if st.button("Escuchar la última intervención"):
        try:
            audio_buffer = BytesIO()
            gTTS(text=latest_assistant["content"], lang="es", tld="com.ar").write_to_fp(
                audio_buffer
            )
            st.audio(audio_buffer.getvalue(), format="audio/mp3")
        except Exception:
            st.warning(
                "No se pudo generar el audio. El resto de la audiencia sigue disponible."
            )
