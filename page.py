import streamlit as st
import requests
import json
import pandas as pd
from streamlit_option_menu import option_menu
import time


st.set_page_config(
    page_title="Plant ID",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://plantnet.org/en/#contact',
        'Report a bug': "https://plantnet.org/en/#contact",
        'About': "# This is a header. This is an *extremely* cool app!",
    }
)


st.markdown("""
    <h1 style='text-align: center; color: #4CAF50; text-shadow: 2px 2px 4px #45a040;'>
        Plant ID <p>   
        <em>based on API Plantnet.org</em></p>
    </h1>
    """, unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options=["🌿", "🌼", "🍒", "🌴"],
    icons=["camera", "camera", "camera", "camera"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

lang_options = {
    "Português-BR": "pt-br",
    "Inglês": "en",
    "Francês": "fr",
    "Espanhol": "es"
}

col1, col2 = st.columns([1, 2])

with col1:
    selected_lang = st.selectbox("Escolha o idioma:", list(lang_options.keys()))
    lang_code = lang_options[selected_lang]

with col2:
    uploaded_file = st.file_uploader("File load", type=["jpg"], label_visibility="hidden")

def stream_data(text_page):
    for word in text_page.split(" "):
        yield word + " "
        time.sleep(0.05)

if selected == "Leaf":
    text_page = f"Na dança do vento, a 🌿 sussurra segredos, vestida de verde esperança, testemunha do tempo que passa."
    st.write_stream(stream_data(text_page))

if selected == "Flower":
    text_page = f"Em cada 🌼 que desabrocha, o universo se pinta de cores, revelando que a beleza é a alma da vida."
    st.write_stream(stream_data(text_page))

if selected == "Fruit":
    text_page = f"Em cada 🍒 maduro, a terra guarda a essência dos sonhos, como promessas que brotam do amor das raízes."
    st.write_stream(stream_data(text_page))

if selected == "Bark":
    text_page = f"Tronco firme e sábio, guardião de histórias antigas, abraça o céu com seus braços de folhas, enquanto os pássaros cantam a melodia do tempo."
    st.write_stream(stream_data(text_page))

API_KEY = st.secrets["auth_key"]
PROJECT = "all"
api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?lang={lang_code}&api-key={API_KEY}"


if uploaded_file is not None:
    st.image(uploaded_file, use_container_width=False, width=800)
    data = {'organs': [selected.lower()]}
    files = [('images', (uploaded_file.name, uploaded_file.getvalue()))]
    request = requests.Request('POST', url=api_endpoint, files=files, data=data)
    prepared = request.prepare()
    session = requests.Session()
    response = session.send(prepared)
    
    if response.status_code == 200:
        json_result = json.loads(response.text)
        st.write(f"Identification based on {selected}:")
        data_results = json_result['results']
        df = pd.json_normalize(data_results)
        st.write(df)
    else:
        st.error(f"Response Error: {response.status_code} - {response.text}")
