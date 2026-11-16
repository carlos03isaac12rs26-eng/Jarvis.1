import streamlit as st
from openai import OpenAI

# Configuración de la página móvil
st.set_page_config(
    page_title="JARVIS Mobile",
    page_icon="🤖",
    layout="centered"
)

# Estilo visual futurista
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #00ffcc;
    }
    </style>
""", unsafe_allow_html=True)

st.title("J.A.R.V.I.S. v1.0")
st.write("Sistemas en línea. A su servicio, Señor.")

# Configurar API Key en la barra lateral
api_key = st.sidebar.text_input("API Key de Google Gemini", type="password")

if not api_key:
    st.warning("Por favor, ingrese su API Key de Gemini en la barra lateral para iniciar los sistemas.")
else:
    # Conexión compatible con el endpoint gratuito de Gemini
    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    # Inicializar el historial de conversación
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "Eres JARVIS (Just A Rather Very Intelligent System), "
                    "el asistente de inteligencia artificial de Tony Stark. Eres formal, "
                    "eficiente, altamente inteligente y ligeramente ingenioso. "
                    "Te diriges al usuario siempre como 'Señor' y respondes de manera "
                    "concisa y directa, ideal para lectura en dispositivos móviles."
                ),
            }
        ]

    # Mostrar mensajes previos
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Caja de entrada para hablar con el asistente
    if prompt := st.chat_input("Escriba su orden, Señor..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="gemini-2.5-flash",
                    messages=st.session_state.messages
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error de sistema: {e}")
        
