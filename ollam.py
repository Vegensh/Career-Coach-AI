import streamlit as st
import requests

def ollama_response(prompt, model="deepseek-r1:1.5b"):
    try:
        url = "http://localhost:11434/api/generate"
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(url, json=data)
        st.write(f"Ollama raw response status: {response.status_code}")
        st.write(f"Ollama raw response text: {response.text}")
        if response.status_code == 10:
            result = response.json()
            return result.get("response", "No response from Ollama.")
        else:
            return f"Ollama error: {response.status_code} - {response.text}"
    except Exception as e:
        st.write(f"Exception calling Ollama: {e}")
        return f"Exception calling Ollama: {e}"

st.title("Test Ollama API Connectivity")

model_name = st.text_input("Ollama Model Name", "deepseek-r1:1.5b")
user_question = st.text_input("Enter your question")

if st.button("Ask Ollama"):
    if user_question.strip():
        reply = ollama_response(user_question, model=model_name)
        st.markdown("### Ollama Response:")
        st.write(reply)
    else:
        st.warning("Please enter a question")
