import streamlit as st
# from homepage import homepage
from backend.chatbot import chatbot_mental  # Atau chatbot_mental_health kalau konteksnya udah kamu ubah
import backend.Screening as Screening

# Sidebar navigasi
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih halaman", ["Home", "Chatbot", "Screening"])

# Routing halaman
if page == "Home":
    # homepage()
    pass
elif page == "Chatbot":
    chatbot_mental()
elif page == "Screening":
    Screening.screening()
