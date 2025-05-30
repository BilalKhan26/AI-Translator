import streamlit as st
from transformers import MarianMTModel, MarianTokenizer
from langdetect import detect
import speech_recognition as sr
import pyttsx3
import base64
import docx2txt
import pytesseract
from PIL import Image
import os

# --- Language dictionary ---
lang_dict = {
    "English": "en",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Russian": "ru",
    "Hindi": "hi",
    "Urdu": "ur"
}

# --- Page Config ---
st.set_page_config(page_title="🌐 AI Translator", layout="centered")

st.markdown("""
    <style>
    .main {background-color: #f9f9f9;}
    h1, h3 {text-align: center; color: #4B8BBE;}
    .css-1q8dd3e {color: #4B8BBE;}
    </style>
""", unsafe_allow_html=True)

st.title("🌐 AI Translator")
st.markdown("### ✨ Translate text, files, and images with speech support")

src_lang_name = st.selectbox("🔤 Translate from", list(lang_dict.keys()))
tgt_lang_name = st.selectbox("🈯 Translate to", list(lang_dict.keys()))

src_code = lang_dict[src_lang_name]
tgt_code = lang_dict[tgt_lang_name]

# --- Input method ---
input_method = st.radio("📝 Select input type", ("Text", "Text File", "Image"))

# --- Input data ---
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Speak now...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        st.success(f"✅ You said: {text}")
        return text
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return ""

def extract_text_from_image(img):
    try:
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        st.error(f"❌ Image reading error: {e}")
        return ""

def extract_text_from_file(file):
    ext = file.name.split('.')[-1]
    try:
        if ext == "txt":
            return file.read().decode()
        elif ext in ["docx"]:
            return docx2txt.process(file)
        else:
            return ""
    except Exception as e:
        st.error(f"❌ File reading error: {e}")
        return ""

if input_method == "Text":
    input_text = st.text_area("Enter text here:")
elif input_method == "Text File":
    uploaded_file = st.file_uploader("📄 Upload .txt or .docx file", type=['txt', 'docx'])
    input_text = extract_text_from_file(uploaded_file) if uploaded_file else ""
elif input_method == "Image":
    uploaded_img = st.file_uploader("🖼️ Upload an image (JPG/PNG)", type=['jpg', 'png', 'jpeg'])
    if uploaded_img:
        img = Image.open(uploaded_img)
        st.image(img, caption="Uploaded Image", use_column_width=True)
        input_text = extract_text_from_image(img)
    else:
        input_text = ""

# --- Load Translation Model ---
@st.cache_resource(show_spinner=False)
def load_model(src, tgt):
    model_name = f"Helsinki-NLP/opus-mt-{src}-{tgt}"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return model, tokenizer

# --- Translate text ---
def translate_text(text, src, tgt):
    model, tokenizer = load_model(src, tgt)
    tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(**tokens)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# --- Text-to-Speech with speaker choice ---
def speak_text(text, voice_id=None):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if voice_id is not None:
        engine.setProperty('voice', voice_id)
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# --- Translation Button ---
if st.button("🔁 Translate"):
    if not input_text.strip():
        st.warning("⚠️ Please provide some input text.")
    elif src_code == tgt_code:
        st.warning("⚠️ Source and target languages must differ.")
    else:
        translated = translate_text(input_text, src_code, tgt_code)
        st.success("✅ Translation:")
        st.text_area("📝 Translated Text", translated, height=150)

        # --- Voice Selection ---
        if st.checkbox("🔊 Listen to the translation"):
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            voice_names = [f"{i}: {v.name}" for i, v in enumerate(voices)]
            selected_voice = st.selectbox("🎤 Choose a voice", voice_names)
            voice_index = int(selected_voice.split(":")[0])
            speak_text(translated, voices[voice_index].id)

        # --- Download Option ---
        if st.download_button("⬇️ Download Translation", translated, file_name="translated.txt"):
            st.success("📥 File downloaded successfully.")
