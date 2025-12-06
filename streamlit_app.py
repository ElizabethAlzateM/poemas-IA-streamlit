import os
import random
import streamlit as st
import traceback

# NOTA: Comentamos las importaciones de pandas y requests
# import pandas as pd 
# import requests 

# =========================
# Diagnóstico inicial
# =========================
st.header("Diagnóstico rápido (Prueba de Aislamiento)")
st.write("Python version:", os.sys.version)
st.write("Working dir:", os.getcwd())
st.write("Archivos en raíz:", os.listdir("."))

# Diagnóstico adicional para la carpeta 'main' (para verificar el clon de Git)
try:
    st.write("Archivos en 'main':", os.listdir("main/"))
except FileNotFoundError:
    st.write("La carpeta 'main' no existe.")
except NotADirectoryError:
    st.write("El archivo 'main' no es una carpeta.")

HF_TOKEN = os.getenv("HF_TOKEN")
st.write("HF_TOKEN presente (debe ser True):", bool(HF_TOKEN))

# COMENTAMOS LA LECTURA DEL CSV
# csv_path = "main/poems_clean.csv" 
# st.write("CSV existe (Ignorado para la prueba):", os.path.exists(csv_path))
# df = None # Establecemos df a None para no usarlo

# =========================
# Configuración del modelo (Solo constantes, no se usa la función)
# =========================
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct" 
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

# COMENTAMOS la función de generación ya que no se usa en esta prueba
# def hf_generate(prompt, max_tokens=300, temperature=0.9):
#    pass 

# =========================
# Interfaz Streamlit
# =========================
st.title("📝 IA Generativa de Poemas en Español (Mínimo)")

st.markdown("""
Esta es una **prueba de carga mínima** para descartar problemas de archivos (CSV) 
o de conexión a Hugging Face.
""")

st.subheader("Resultado de la Prueba:")
st.success("Si ves este texto, Streamlit está funcionando en la nube.")

tema = st.text_input("Tema del poema (Ignorado)")
estilo = st.selectbox(
    "Estilo (Ignorado)",
    ["Verso libre","Soneto","Haiku","Romance"]
)

if st.button("Generar poema"):
    st.info("El bloque de generación de poemas está **desactivado** para esta prueba de diagnóstico. Si ves este mensaje, la aplicación se cargó correctamente.")

# ----------------------------------------------------
# Bloque de generación de poema (COMENTADO TEMPORALMENTE)
# ----------------------------------------------------
    
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