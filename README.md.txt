IA Generativa de Poemas en Español

Esta aplicación utiliza el modelo **Meta-Llama-3-8B-Instruct** y se inspira en un dataset de poemas en español para generar nuevas composiciones en distintos estilos poéticos.  
El proyecto está desarrollado con **Streamlit** y se conecta a la API de Hugging Face para la generación de texto.

---

Estructura del proyecto:
.env
.gitignore
poems_clean.csv
requirements.txt
streamlit_app.py
README.md

Instalación:
Clona el repositorio y entra en la carpeta:

bash
git clone https://github.com/TU_USUARIO/poemas-IA-streamlit.git
cd poemas-IA-streamlit

Instala las dependencias:
pip install -r requirements.txt

Ejecución en local:
Ejecuta la aplicación con: streamlit run streamlit_app.py

Dataset
El archivo poems_clean.csv contiene poemas en español limpios y listos para usarse como inspiración en la generación.
El dataset fue obtenido de Kaggle y procesado para eliminar duplicados, caracteres extraños y espacios innecesarios.

Configuración
Crea un archivo .env en la raíz del proyecto con tu token de Hugging Face:
HF_TOKEN=tu_token_aqui

Estilos poéticos disponibles
- Verso libre: Poema sin rima ni métrica fija.
- Soneto: 14 versos endecasílabos con rima organizada.
- Haiku: Tres versos breves inspirados en la naturaleza.
- Romance: Versos octosílabos con rima asonante en pares.
- Décima: 10 versos octosílabos con rima ABBAACCDDC.
- Oda: Poema solemne y reflexivo.
- Copla: Estrofa de 4 versos octosílabos con rima en pares.
- Elegía: Poema melancólico sobre la pérdida.
- Égloga: Diálogo bucólico entre pastores.
- Lira: Estrofa de 5 versos con métrica 7-11-7-7-11.
- Redondilla: Estrofa de 4 versos octosílabos con rima ABBA.


Despliegue en Streamlit:
1. 	Conecta tu repositorio de GitHub en Streamlit Cloud.
2. 	Selecciona el archivo  como punto de entrada.
3. 	Configura el secreto  en la sección de Secrets.
4. 	Tu aplicación estará disponible en una URL pública.

Créditos
• 	Dataset: Spanish Poetry Dataset en Kaggle
• 	Modelo: Meta-Llama-3-8B-Instruct en Hugging Face
• 	Desarrollo: Proyecto personal de Elizabeth Alzate Murillo para explorar IA generativa aplicada a la poesía en español.
