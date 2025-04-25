import streamlit as st
# from homepage import homepage
from chatbot import chatbot_mental  # Atau chatbot_mental_health kalau konteksnya udah kamu ubah

# Sidebar navigasi
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih halaman", ["Home", "Chatbot BISINDO"])

# Routing halaman
if page == "Home":
    # homepage()
    pass
elif page == "Chatbot BISINDO":
    chatbot_mental()
