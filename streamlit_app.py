import os
import pandas as pd
import random
import streamlit as st
import requests
import traceback

# =========================
# Diagnóstico inicial
# =========================
st.header("Diagnóstico rápido")
st.write("Python version:", os.sys.version)
st.write("Working dir:", os.getcwd())
st.write("Archivos en raíz:", os.listdir("."))

HF_TOKEN = os.getenv("HF_TOKEN")
st.write("HF_TOKEN presente:", bool(HF_TOKEN))

csv_path = "poems_clean.csv"
st.write("CSV existe:", os.path.exists(csv_path))
try:
    df = pd.read_csv(csv_path)
    st.write("CSV cargado: filas =", len(df))
except Exception as e:
    st.error(f"Error leyendo CSV: {e}")
    df = None

# =========================
# Configuración del modelo
# =========================
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

def hf_generate(prompt, max_tokens=300, temperature=0.9):
    """Cliente HTTP para Hugging Face API"""
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
    # Manejo flexible de la respuesta
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
Esta aplicación utiliza un modelo de **IA (Meta-Llama-3-8B-Instruct)** 
para generar poemas originales en español.  
El modelo fue entrenado con un dataset de poemas de *poemas-del-alma.com* 
y puede adaptarse a distintos estilos literarios.

### Estilos disponibles:
- **Verso libre**: Poema sin rima ni métrica fija.
- **Soneto**: 14 versos endecasílabos con rima organizada.
- **Haiku**: Tres versos breves inspirados en la naturaleza.
- **Romance**: Versos octosílabos con rima asonante en pares.
- **Décima**: 10 versos octosílabos con rima ABBAACCDDC.
- **Oda**: Poema solemne y reflexivo.
- **Copla**: Estrofa de 4 versos octosílabos con rima en pares.
- **Elegía**: Poema melancólico sobre la pérdida.
- **Égloga**: Diálogo bucólico entre pastores.
- **Lira**: Estrofa de 5 versos con métrica 7-11-7-7-11.
- **Redondilla**: Estrofa de 4 versos octosílabos con rima ABBA.
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
        elif df is None:
            st.error("No se pudo cargar poems_clean.csv.")
        else:
            ejemplos = df['content'].dropna().sample(min(3, len(df))).tolist()
            ejemplos_texto = "\n".join([f"- {e.strip()[:200]}" for e in ejemplos])

            prompt = f"""
Eres un poeta experto en español.
Escribe un poema sobre el tema: "{tema}".
Estilo: {estilo}.
Inspírate en el estilo (sin copiar) de estos ejemplos:
{ejemplos_texto}
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