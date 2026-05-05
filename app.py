import streamlit as st
import requests
import random

# 🔑 API do Last.fm
API_KEY = "SUA_API_AQUI"
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

# 🎵 Buscar música
def buscar_musica(genero):
    params = {
        "method": "tag.gettoptracks",
        "tag": genero,
        "api_key": API_KEY,
        "format": "json",
        "limit": 20
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    try:
        tracks = data["tracks"]["track"]
        musica = random.choice(tracks)

        return {
            "musica": musica["name"],
            "artista": musica["artist"]["name"],
            "imagem": musica["image"][-1]["#text"]
        }
    except:
        return None

# 🎨 Mapear humor → cores
def mapear_humor(humor):
    if humor == "Feliz":
        return ["#FFD700", "#FF69B4", "#FF8C00"]
    elif humor == "Triste":
        return ["#2F4F4F", "#4682B4", "#708090"]
    elif humor == "Calmo":
        return ["#98FB98", "#AFEEEE", "#E0FFFF"]
    elif humor == "Ansioso":
        return ["#FF4500", "#FFD700", "#8B0000"]
    else:
        return ["#CCCCCC", "#999999", "#666666"]

# 💬 Frases
def gerar_frase(humor):
    frases = {
        "Feliz": [
            "Sua alma vibra como luz dourada em movimento.",
            "Você é ritmo, cor e brilho no agora."
        ],
        "Triste": [
            "Há poesia até nas partes silenciosas de você.",
            "Mesmo em silêncio, você floresce."
        ],
        "Calmo": [
            "O mundo desacelera dentro de você.",
            "Você é um respiro no caos."
        ],
        "Ansioso": [
            "Energia pede direção — você está vivo.",
            "Seu caos também cria movimento."
        ]
    }
    return random.choice(frases.get(humor, ["Siga seu ritmo."]))

# 🌐 Interface
st.title("🎵 Sua Música do Dia")

humor = st.selectbox("Como você está se sentindo?", ["Feliz", "Triste", "Calmo", "Ansioso"])
genero = st.selectbox("Escolha um gênero musical:", ["pop", "rock", "indie", "electronic"])

if st.button("▶️ Gerar Música"):

    resultado = buscar_musica(genero)

    if resultado is None:
        st.error("Nenhuma música encontrada 😢")
    else:
        st.subheader(f"{resultado['musica']}")
        st.write(f"🎤 {resultado['artista']}")

        if resultado["imagem"]:
            st.image(resultado["imagem"], width=250)

        cores = mapear_humor(humor)
        st.write("🎨 Paleta do seu humor:")
        cols = st.columns(len(cores))
        for i, cor in enumerate(cores):
            cols[i].markdown(
                f"<div style='width:60px;height:60px;background:{cor};border-radius:10px;'></div>",
                unsafe_allow_html=True
            )

        frase = gerar_frase(humor)
        st.write("💬 Mensagem:")
        st.success(frase)
