import os
import pandas as pd
import random
import streamlit as st
import requests
import traceback

# =========================
# CONFIGURACIÓN DE LA PÁGINA Y ESTILOS
# =========================
st.set_page_config(
    page_title="Generador de Poemas IA",
    page_icon="✍️",
    layout="wide", # Usa todo el ancho de la pantalla
)

# =========================
# DIAGNÓSTICO Y CARGA INICIAL
# =========================

# RUTA CORREGIDA: El archivo está en la raíz del repositorio
csv_path = "poems_clean.csv" 
df = None

# Intentamos cargar el CSV
try:
    df = pd.read_csv(csv_path)
except Exception:
    st.sidebar.error("Error: No se pudo cargar poems_clean.csv. Verifica que esté en la raíz.")
    df = None
    
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    st.sidebar.warning("⚠️ HF_TOKEN no encontrado. Por favor, configúralo en Secrets.")

# =========================
# CONFIGURACIÓN DEL MODELO Y API
# =========================
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"
# URL CORREGIDA: Usamos router.huggingface.co en lugar de api-inference.huggingface.co
API_URL = f"https://router.huggingface.co/models/{MODEL_ID}" 

def hf_generate(prompt, max_tokens=300, temperature=0.9):
    """Cliente HTTP para Hugging Face API con manejo de errores."""
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": temperature,
        }
    }
    
    # Aumentamos el timeout a 180s para modelos grandes (Llama 3)
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=180) 
    resp.raise_for_status()
    data = resp.json()
    
    # Procesamiento de la respuesta
    if isinstance(data, list) and data and "generated_text" in data[0]:
        return data[0]["generated_text"]
    
    return "Error: Respuesta inesperada de la API."

# =========================
# INTERFAZ STREAMLIT
# =========================

st.title("✍️ IA Generativa de Poemas en Español")

st.markdown("""
Esta aplicación utiliza el modelo **Meta-Llama-3-8B-Instruct** (vía API de Hugging Face)
para generar poemas originales en español. El modelo se inspira en un dataset de poemas
existentes para adaptarse a distintos estilos literarios.
""")

st.subheader("Configuración de la Generación")

# Usamos dos columnas para una mejor disposición visual
col1, col2 = st.columns(2)

with col1:
    tema = st.text_input("Tema del poema", placeholder="Ej: La melancolía del otoño")

with col2:
    estilo = st.selectbox(
        "Estilo",
        ["Verso libre", "Soneto", "Haiku", "Romance", "Décima", "Oda",
         "Copla", "Elegía", "Égloga", "Lira", "Redondilla"]
    )

if st.button("✨ Generar Poema", type="primary"):
    
    if not tema or len(tema.strip()) < 3:
        st.error("Por favor, ingresa un tema válido para la generación.")
    elif not HF_TOKEN:
        st.error("El token de Hugging Face (HF_TOKEN) es necesario para usar el modelo.")
    elif df is None or df.empty:
        st.error("El dataset de poemas no se cargó correctamente. No se puede generar el prompt.")
    else:
        try:
            # 1. Preparar Ejemplos y Prompt
            ejemplos = df['content'].dropna().sample(min(3, len(df))).tolist()
            ejemplos_texto = "\n".join([f"- {e.strip()[:200]}..." for e in ejemplos])

            prompt = f"""
Eres un poeta experto en español.
Escribe un poema sobre el tema: "{tema}".
Estilo: {estilo}.
Inspírate en el estilo (sin copiar) de estos ejemplos:
{ejemplos_texto}
Ahora escribe el poema:
""".strip()
            
            # 2. Generar el Poema con Feedback Visual (Spinner)
            st.subheader(f"Resultado: Poema '{estilo}' sobre '{tema}'")
            with st.spinner("⏳ La IA está escribiendo... Esto puede tardar varios segundos debido al tamaño del modelo."):
                poem = hf_generate(prompt, max_tokens=300, temperature=0.9)
            
            # Mostrar resultado con formato
            st.success("✅ Generación completada.")
            st.markdown(f"---")
            st.markdown(poem)
            st.markdown(f"---")
    
        except requests.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 503:
                 st.error("💔 **Error 503: Servicio no disponible.** El modelo está cargando (Cold Start). Por favor, espera un minuto e inténtalo de nuevo.")
            else:
                 st.error(f"🚨 Error HTTP de Hugging Face: {status_code} - {e.response.text}")
        except requests.exceptions.Timeout:
            st.error("⏰ **Error de tiempo de espera (Timeout).** El modelo tardó demasiado en responder. Intenta de nuevo.")
        except Exception as e:
            st.error("🚨 Error inesperado durante la generación.")
            st.code("".join(traceback.format_exception(e)))

st.markdown("""
---
### Estilos Disponibles:
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