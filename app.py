import streamlit as st
from transformers import MarianMTModel, MarianTokenizer
from langdetect import detect
import pytesseract
from PIL import Image
import pdfplumber
import pyttsx3
import base64
import os

# UI Setup
st.set_page_config(page_title="🌐 AI Translator App", layout="centered")
st.markdown("## 🌍 AI Translator with Speech, Files, and Images")
st.markdown("Translate between languages including **Urdu** with voice support, file upload, and image OCR.")
st.markdown("---")

# Language options
lang_dict = {
    "English": "en", "French": "fr", "German": "de",
    "Spanish": "es", "Italian": "it", "Russian": "ru",
    "Hindi": "hi", "Urdu": "ur"
}
langs = list(lang_dict.keys())

src_lang = st.selectbox("🔤 Translate from", langs)
tgt_lang = st.selectbox("🔠 Translate to", langs)
src_code, tgt_code = lang_dict[src_lang], lang_dict[tgt_lang]

@st.cache_resource(show_spinner=False)
def load_model(src, tgt):
    model_name = f"Helsinki-NLP/opus-mt-{src}-{tgt}"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return model, tokenizer

def translate_text(text, src, tgt):
    model, tokenizer = load_model(src, tgt)
    tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(**tokens)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def text_to_speech(text, voice_id=None):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if voice_id is not None:
        engine.setProperty('voice', voices[voice_id].id)
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# Input Methods
option = st.radio("📥 Input Method", ["Type", "Upload File", "Upload Image"])

input_text = ""
if option == "Type":
    input_text = st.text_area("✍️ Enter text to translate", height=150)
elif option == "Upload File":
    uploaded_file = st.file_uploader("📄 Upload a .txt or .pdf file", type=["txt", "pdf"])
    if uploaded_file:
        if uploaded_file.type == "text/plain":
            input_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                input_text = "".join(page.extract_text() for page in pdf.pages)
elif option == "Upload Image":
    image_file = st.file_uploader("🖼️ Upload an image", type=["png", "jpg", "jpeg"])
    if image_file:
        img = Image.open(image_file)
        input_text = pytesseract.image_to_string(img)

if st.button("🚀 Translate"):
    if input_text.strip() == "":
        st.warning("⚠️ Please provide input text.")
    elif src_code == tgt_code:
        st.warning("⚠️ Source and target languages must differ.")
    else:
        translated = translate_text(input_text, src_code, tgt_code)
        st.success("✅ Translation:")
        st.text_area("📝 Translated Text", translated, height=150)

        if st.button("🔊 Speak"):
            voice_choice = st.selectbox("🎙️ Choose Voice", ["Voice 1", "Voice 2", "Voice 3"])
            text_to_speech(translated, voice_id=langs.index(tgt_lang) % 3)

        # Download
        b64 = base64.b64encode(translated.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="translated.txt">📥 Download Translation</a>'
        st.markdown(href, unsafe_allow_html=True)