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

# Diagnóstico adicional para la carpeta 'main'
try:
    st.write("Archivos en 'main':", os.listdir("main/"))
except FileNotFoundError:
    st.write("La carpeta 'main' no existe.")

HF_TOKEN = os.getenv("HF_TOKEN")
st.write("HF_TOKEN presente:", bool(HF_TOKEN))

# RUTA CORREGIDA: Asumiendo que el archivo está dentro de 'main/'
csv_path = "main/poems_clean.csv" 
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
# Usa Mistral temporalmente para reducir latencia, aunque el bloque estará comentado
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
    # Aumentar el manejo de posibles Timeouts
    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        st.error("Error: La solicitud a Hugging Face ha excedido el tiempo de espera (Timeout).")
        return "ERROR DE TIMEOUT" # Retorna un mensaje de error
    
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
Esta aplicación utiliza un modelo de **IA (Meta-Llama-3-8B-Instruct)** para generar poemas originales en español.  
... (resto de la descripción de la interfaz)
""")

tema = st.text_input("Tema del poema")
estilo = st.selectbox(
    "Estilo",
    ["Verso libre","Soneto","Haiku","Romance","Décima","Oda",
     "Copla","Elegía","Égloga","Lira","Redondilla"]
)

# ----------------------------------------------------
# Bloque de generación de poema (COMENTADO TEMPORALMENTE)
# ----------------------------------------------------
if st.button("Generar poema"):
    st.info("La función de generación está actualmente comentada para propósitos de diagnóstico.")
    st.info("Si la aplicación carga hasta aquí, el problema está en la conexión con Hugging Face (latencia o permisos del modelo).")
    
    # try:
    #     if not HF_TOKEN:
    #         st.error("No se encontró HF_TOKEN en Secrets. Ve a Settings → Secrets y agrégalo con comillas dobles.")
    #     elif df is None:
    #         st.error("No se pudo cargar poems_clean.csv.")
    #     else:
    #         # Lógica para seleccionar ejemplos del CSV
    #         ejemplos = df['content'].dropna().sample(min(3, len(df))).tolist()
    #         ejemplos_texto = "\n".join([f"- {e.strip()[:200]}" for e in ejemplos])

    #         # Construcción del prompt
    #         prompt = f"""
    # Eres un poeta experto en español.
    # Escribe un poema sobre el tema: "{tema}".
    # Estilo: {estilo}.
    # Inspírate en el estilo (sin copiar) de estos ejemplos:
    # {ejemplos_texto}
    # Ahora escribe el poema:
    # """.strip()

    #         # Llamada a la API de Hugging Face
    #         poem = hf_generate(prompt, max_tokens=300, temperature=0.9)
    #         st.subheader("✨ Poema generado:")
    #         st.write(poem)
    # # Manejo de errores específicos y genéricos
    # except requests.HTTPError as e:
    #     st.error(f"Error HTTP de Hugging Face: {e.response.status_code} - {e.response.text}")
    # except Exception as e:
    #     st.error("Error inesperado en la app")
    #     st.code("".join(traceback.format_exception(e)))