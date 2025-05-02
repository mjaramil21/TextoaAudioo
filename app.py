import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

st.set_page_config(page_title="Texto a Audio", layout="centered")

st.markdown('<style>body {background-color: #800020;} .stApp {background-color: #800020; text-align: center;} h1, .stApp h1 {color: #EFBF04 !important; text-align: center;} h2, h3, .stApp h2 {color: #EFBF04 !important; text-align: center;} .stButton>button {background-color: #EFBF04; color: white; border: none; border-radius: 8px; padding: 0.5em 1em; font-weight: bold; display: block; margin: auto;} .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {color: #ffb3ec !important;} .stTextArea label, .stSelectbox label {color: #EFBF04 !important; text-align: center; display: block; width: 100%;} .custom-text {color:  #FFA800; text-align: center; font-size: 16px;}</style>', unsafe_allow_html=True)

st.title("Conversión de Texto a Audio")

image = Image.open("imagen_2025-05-01_210402173.png")
st.image(image, use_container_width=True)

with st.sidebar:
    st.subheader("Esrcibe y/o pega un texto para poder escucharlo.")

try:
    os.mkdir("temp")
except:
    pass

st.subheader("Traductor de canciones")

st.markdown('<p class="custom-text">Todos amamos escuchar música ¿cierto? y por eso sé que a veces tenemos canciones que nos preguntamos como suenan en inglés o en español, dependiendo de su idioma original, ¡por eso te invito que escribas la letra de tu canción favorita y la traduzcas para que dejes de tener esa duda!</p>', unsafe_allow_html=True)
st.markdown('<p class="custom-text">Escribe la letra de alguna canción</p>', unsafe_allow_html=True)

text = st.text_area("Ingrese el texto a escuchar.")

option_lang = st.selectbox("Selecciona el lenguaje", ("Español", "English"))
lg = "es" if option_lang == "Español" else "en"

def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[0:20].strip().replace(" ", "_")
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

if st.button("Convertir a Audio"):
    result, output_text = text_to_speech(text, lg)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown("## Tu audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    with open(f"temp/{result}.mp3", "rb") as f:
        data = f.read()

    def get_binary_file_downloader_html(bin_file, file_label='File'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Descargar {file_label}</a>'
        return href

    st.markdown(get_binary_file_downloader_html(f"temp/{result}.mp3", file_label="Archivo de Audio"), unsafe_allow_html=True)

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)
