import os
import pandas as pd
import random
import streamlit as st
import requests
import traceback

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = "tiiuae/falcon-7b-instruct"
API_URL = f"https://router.huggingface.co/models/{MODEL_ID}"

def hf_generate(prompt, max_tokens=300, temperature=0.9):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": temperature,
        }
    }
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, list) and data and "generated_text" in data[0]:
        return data[0]["generated_text"]
    if isinstance(data, dict) and "generated_text" in data:
        return data["generated_text"]
    return str(data)

# =========================
# Interfaz Streamlit
# =========================
st.title("📝 IA Generativa de Poemas en Español")

st.markdown("""
Esta aplicación utiliza un modelo de **IA (Falcon-7B-Instruct)**
para generar poemas originales en español.
""")

tema = st.text_input("Tema del poema")
estilo = st.selectbox(
    "Estilo",
    ["Verso libre","Soneto","Haiku","Romance","Décima","Oda",
     "Copla","Elegía","Égloga","Lira","Redondilla"]
)

if st.button("Generar poema"):
    try:
        if not HF_TOKEN:
            st.error("No se encontró HF_TOKEN en Secrets. Ve a Settings → Secrets y agrégalo con comillas dobles.")
        else:
            prompt = f"""
Eres un poeta experto en español.
Escribe un poema sobre el tema: "{tema}".
Estilo: {estilo}.
Ahora escribe el poema:
""".strip()

            poem = hf_generate(prompt, max_tokens=300, temperature=0.9)
            st.subheader("✨ Poema generado:")
            st.write(poem)
    except requests.HTTPError as e:
        st.error(f"Error HTTP de Hugging Face: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        st.error("Error inesperado en la app")
        st.code("".join(traceback.format_exception(e)))