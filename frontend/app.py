import os
import streamlit as st
import requests

# === Grundkonfiguration ===
# URL till backend (ändra om du kör backend lokalt)
BACKEND_URL = os.getenv("BACKEND_URL", "https://david-tutor-1.onrender.com/chat")
st.set_page_config(page_title="David Tutor Cloud", page_icon="🎓")

# Streamlit rekommenderar att använda secrets.toml (TOML) för hemligheter.
# Vi läser först från st.secrets (t.ex. .streamlit/secrets.toml eller Streamlit Cloud Secrets)
# och faller tillbaka på miljövariabler om de saknas.
secrets = {}
try:
    secrets = st.secrets
except Exception:
    secrets = {}

# Säkerhetsinställningar: kräver ett lösenord för att använda klienten (DAVID_PASSWORD)
# och skickar en server-till-server API-nyckel i headern (APP_API_KEY) så bara backend accepterar.
APP_API_KEY = secrets.get("APP_API_KEY") or os.getenv("APP_API_KEY")
DAVID_PASSWORD = secrets.get("DAVID_PASSWORD") or os.getenv("DAVID_PASSWORD")

# === UI-layout ===
st.title("🎓 David Tutor Cloud")
st.caption("Din personliga läxcoach på webben")

if "history" not in st.session_state:
    st.session_state.history = []

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Om ett lösenord är satt i miljön, kräver vi att användaren loggar in.
if DAVID_PASSWORD:
    if not st.session_state.authenticated:
        pwd = st.text_input("Lösenord (endast David)", type="password")
        if pwd:
            if pwd == DAVID_PASSWORD:
                st.session_state.authenticated = True
                st.success("Inloggad")
            else:
                st.error("Fel lösenord")
        st.stop()

user_input = st.chat_input("Skriv ett meddelande till din coach...")

if user_input:
    with st.spinner("Tänker..."):
        payload = {"message": user_input}
        try:
            headers = {"Content-Type": "application/json"}
            if APP_API_KEY:
                headers["X-API-KEY"] = APP_API_KEY
            response = requests.post(BACKEND_URL, json=payload, headers=headers, timeout=60)
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
