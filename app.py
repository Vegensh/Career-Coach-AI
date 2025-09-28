import streamlit as st
import subprocess
import requests

from chatbot import CareerCoachBot
from ai_integration import AIAssistant
from career_data import get_all_sectors, get_sub_fields

def ollama_response(prompt, model="deepseek-r1:1.5b"):
    try:
        url = "http://localhost:11434/api/generate"
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "Ollama gave no text.")
        else:
            return f"Ollama error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Exception calling Ollama: {e}"

st.set_page_config(page_title="AI Career Coach", page_icon="🎯")
with st.sidebar:
    st.header("AI Career Coach")
    st.markdown("Chat about your career options by selecting a sector and job.")
    model_name = st.text_input("🧠 Ollama Model Name:", "deepseek-r1:1.5b")
    # ... (Optional: Ollama install/model loader as before) ...

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

coach = CareerCoachBot()
ai = AIAssistant()

st.title("Career Coach Chatbot 🤖")

sector = st.selectbox("Sector", [""] + get_all_sectors())
job = ""
if sector:
    jobs = [""] + get_sub_fields(sector)
    job = st.selectbox("Job/Career", jobs)

with st.form(key="chat_form"):
    user_message = st.text_input("Type your message/question and hit Enter", key="chat_input")
    send_clicked = st.form_submit_button(label="Send")

if send_clicked:
    if not sector or not job or not user_message.strip():
        st.warning("Please select sector, job, and enter a question.")
    else:
        st.session_state.chat_history.append(("You", user_message))
        # --- Try local knowledge base ---
        reply = coach.process_message(user_message, sector, job)
        # --- Check for a fallback/generic/empty answer ---
        fallback_detected = (
            not reply or
            "no data" in reply.lower() or
            "not found" in reply.lower() or
            "trouble" in reply.lower() or
            "sorry" in reply.lower() or
            len(reply.strip()) < 15  # too short to be meaningful
        )

        if fallback_detected:
            # Always send fallback to Ollama
            prompt = f"Career Sector: {sector}\nJob: {job}\nUser Question: {user_message}\nRespond clearly and concisely."
            reply = ollama_response(prompt, model=model_name)
            reply = f"(From Ollama Model)\n{reply}"

        st.session_state.chat_history.append(("Coach", reply))

for speaker, msg in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**AI Career Coach:** {msg}")

if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
