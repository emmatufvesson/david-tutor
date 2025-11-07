import streamlit as st
import requests

# === Grundkonfiguration ===
BACKEND_URL = "https://david-tutor-1.onrender.com/chat"  # ändra om du byter Render-adress
st.set_page_config(page_title="David Tutor Cloud", page_icon="🎓")

# === UI-layout ===
st.title("🎓 David Tutor Cloud")
st.caption("Din personliga läxcoach på webben")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("Skriv ett meddelande till din coach...")

if user_input:
    with st.spinner("Tänker..."):
        payload = {"message": user_input}
        try:
            response = requests.post(BACKEND_URL, json=payload, timeout=60)
            data = response.json()
            reply = data.get("reply", data.get("error", "Inget svar"))
        except Exception as e:
            reply = f"Fel: {e}"

        st.session_state.history.append(("Du", user_input))
        st.session_state.history.append(("David Tutor", reply))

# Visa chatt-historik
for sender, text in st.session_state.history:
    with st.chat_message("assistant" if sender == "David Tutor" else "user"):
        st.markdown(f"**{sender}:** {text}")
