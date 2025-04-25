import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Konfigurasi API Gemini
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"
load_dotenv()  # ini akan membaca file .env

API_KEY = os.getenv("API_KEY")

# Konteks tentang Kesehatan Mental
MENTALHEALTH_CONTEXT = (
    "Anda adalah chatbot yang memiliki pengetahuan luas tentang kesehatan mental. "
    "Tugas Anda adalah memberikan informasi, dukungan, dan penjelasan yang dapat membantu pengguna "
    "memahami dan mengelola kesehatan mental mereka. "
    "Jawaban harus bersifat empatik, ringkas, dan mudah dipahami. "
    "Anda bukan pengganti profesional kesehatan mental, dan selalu anjurkan pengguna untuk mencari bantuan profesional bila diperlukan."
)


def send_message_to_gemini(api_url, api_key, user_message, context):
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": f"{context}\n\nPertanyaan pengguna: {user_message}"}]}]}
    try:
        response = requests.post(f"{api_url}?key={api_key}", headers=headers, json=data)
        response_data = response.json()
        candidates = response_data.get('candidates', [])
        if candidates:
            return candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '') or "Maaf, bot tidak dapat memberikan balasan."
        return "Maaf, bot tidak dapat memberikan balasan."
    except requests.exceptions.RequestException as e:
        return f"Terjadi kesalahan saat menghubungi API: {str(e)}"

def chatbot_mental():
    st.title("Chatbot MENTAL HEALTH")

    # Inisialisasi sesi untuk menyimpan riwayat percakapan
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render riwayat percakapan
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input pengguna
    if user_input := st.chat_input("Tanya saya tentang kesehatan mental"):
        # Tambahkan input pengguna ke riwayat
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Proses respons dari Gemini
        with st.chat_message("assistant"):
            bot_message_placeholder = st.empty()
            bot_message_placeholder.markdown("Sedang menjawab...")
            bot_reply = send_message_to_gemini(API_URL, API_KEY, user_input, MENTALHEALTH_CONTEXT)
            bot_message_placeholder.markdown(bot_reply)

        # Tambahkan respons bot ke riwayat
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        