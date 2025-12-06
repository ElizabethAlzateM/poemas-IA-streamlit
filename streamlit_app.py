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
    page_title="Generador de Poemas con IA",
    page_icon="✍️",
    layout="wide",
)

# =========================
# DIAGNÓSTICO Y CARGA INICIAL
# =========================

# RUTA CORRECTA: El archivo está en la raíz del repositorio
csv_path = "poems_clean.csv" 
df = None
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
# Mantenemos el modelo original de tu proyecto
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct" 
# Usamos la URL correcta del router, sabiendo que fallará con 404 en la capa gratuita.
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
    
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=180) 
    resp.raise_for_status()
    data = resp.json()
    
    if isinstance(data, list) and data and "generated_text" in data[0]:
        return data[0]["generated_text"]
    
    return "Error: Respuesta inesperada de la API."

# =========================
# INTERFAZ STREAMLIT
# =========================

st.title("✍️ IA Generativa de Poemas en Español")

st.markdown(f"""
Esta aplicación utiliza el modelo **{MODEL_ID}** (vía API de Hugging Face).
""")

st.subheader("Configuración de la Generación")

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
        st.error("El token de Hugging Face (HF_TOKEN) es necesario.")
    elif df is None or df.empty:
        st.error("El dataset de poemas no se cargó correctamente.")
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
            with st.spinner("⏳ La IA está escribiendo... Esto puede tardar varios segundos."):
                poem = hf_generate(prompt, max_tokens=300, temperature=0.9)
            
            st.success("✅ Generación completada.")
            st.markdown(f"---")
            st.markdown(poem)
            st.markdown(f"---")
    
        except requests.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 404:
                 st.error("❌ **Error 404: Modelo No Encontrado.** El modelo Llama 3 no está disponible en la API pública gratuita. Se requiere un **Endpoint de Infererencia dedicado (pago)** para usar este modelo.")
            elif status_code == 410:
                 st.error("🚨 **Error 410: URL Obsoleta.** La URL de la API fue actualizada. Verifica que estés usando 'router.huggingface.co'.")
            elif status_code == 503:
                 st.error("💔 **Error 503: Servicio no disponible.** El modelo está cargando (Cold Start).")
            else:
                 st.error(f"🚨 Error HTTP de Hugging Face: {status_code} - {e.response.text}")
        except requests.exceptions.Timeout:
            st.error("⏰ **Error de tiempo de espera (Timeout).** El modelo tardó demasiado en responder.")
        except Exception as e:
            st.error("🚨 Error inesperado durante la generación.")
            st.code("".join(traceback.format_exception(e)))

st.markdown("""
---
### Estilos Disponibles:
* **Verso libre**: Poema sin rima ni métrica fija.
* **Soneto**: 14 versos endecasílabos con rima organizada.
* **Haiku**: Tres versos breves inspirados en la naturaleza.
* **Romance**: Versos octosílabos con rima asonante en pares.
* **Décima**: 10 versos octosílabos con rima ABBAACCDDC.
* **Oda**: Poema solemne y reflexivo.
* **Copla**: Estrofa de 4 versos octosílabos con rima en pares.
* **Elegía**: Poema melancólico sobre la pérdida.
* **Égloga**: Diálogo bucólico entre pastores.
* **Lira**: Estrofa de 5 versos con métrica 7-11-7-7-11.
* **Redondilla**: Estrofa de 4 versos octosílabos con rima ABBA.
""")