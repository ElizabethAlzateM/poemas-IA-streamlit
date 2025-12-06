import os
import pandas as pd
import random
from dotenv import load_dotenv
import streamlit as st
from huggingface_hub import InferenceClient

# Cargamos las variables desde .env
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"

# Cargamos tu dataset limpio
df = pd.read_csv("poems_clean.csv")

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
    ["Verso libre","Soneto","Haiku","Romance","Décima","Oda","Copla","Elegía","Égloga","Lira","Redondilla"]
)

if st.button("Generar poema"):
    if not HF_TOKEN:
        st.error("No se encontró el token HF_TOKEN. Verifica tu archivo .env.")
    else:
        try:
            client = InferenceClient(MODEL_ID, token=HF_TOKEN)

            # Seleccionamos algunos ejemplos aleatorios del dataset
            ejemplos = df['content'].dropna().sample(3).tolist()
            ejemplos_texto = "\n".join([f"- {e.strip()[:200]}" for e in ejemplos])

            # Construimos el prompt con inspiración del dataset
            prompt = f"""
Eres un poeta experto en español.
Escribe un poema sobre el tema: "{tema}".
Estilo: {estilo}.
Inspírate en el estilo (sin copiar) de estos ejemplos:
{ejemplos_texto}
Ahora escribe el poema:
"""

            resp = client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.9
            )

            poem = resp.choices[0].message["content"]
            st.write(poem)

        except Exception as e:
            st.error(f"Error al generar poema: {e}")