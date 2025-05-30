import streamlit as st
from transformers import MarianMTModel, MarianTokenizer
from gtts import gTTS
import torch
import os
import tempfile
from langdetect import detect
from PIL import Image
import pytesseract
import docx
import PyPDF2


# Setup language dictionary
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

st.set_page_config(page_title="🌐 AI Translator", layout="centered")
st.title("🧠 AI Translator with gTTS & File Support")

st.markdown("### 🌍 Choose Languages")
src_lang_name = st.selectbox("Translate from", list(lang_dict.keys()))
tgt_lang_name = st.selectbox("Translate to", list(lang_dict.keys()))
src_lang = lang_dict[src_lang_name]
tgt_lang = lang_dict[tgt_lang_name]

st.markdown("### ✍️ Input Method")
input_method = st.radio("Select Input Method", ["Text", "File Upload", "Image Upload"])

# Load model
@st.cache_resource(show_spinner="🔄 Loading translation model...")
def load_model_and_tokenizer(src, tgt):
    model_name = f"Helsinki-NLP/opus-mt-{src}-{tgt}"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return model, tokenizer

def translate_text(text, src, tgt):
    model, tokenizer = load_model_and_tokenizer(src, tgt)
    tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    output = model.generate(**tokens)
    return tokenizer.decode(output[0], skip_special_tokens=True)

def extract_text_from_file(uploaded_file):
    ext = uploaded_file.name.split('.')[-1]
    if ext == "txt":
        return uploaded_file.read().decode("utf-8")
    elif ext == "docx":
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    elif ext == "pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    else:
        st.error("Unsupported file type.")
        return ""

def extract_text_from_image(image_file):
    img = Image.open(image_file)
    return pytesseract.image_to_string(img)

# Input handling
input_text = ""
if input_method == "Text":
    input_text = st.text_area("Enter text to translate", height=150)
elif input_method == "File Upload":
    file = st.file_uploader("Upload a text, PDF or Word file", type=["txt", "docx", "pdf"])
    if file:
        input_text = extract_text_from_file(file)
        st.text_area("Extracted text", input_text, height=150)
elif input_method == "Image Upload":
    image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if image:
        input_text = extract_text_from_image(image)
        st.text_area("Extracted text", input_text, height=150)

# Translation and TTS
if st.button("🔁 Translate"):
    if not input_text.strip():
        st.warning("⚠️ Please enter or upload some text.")
    elif src_lang == tgt_lang:
        st.warning("⚠️ Source and target languages must differ.")
    else:
        translated = translate_text(input_text, src_lang, tgt_lang)
        st.success("✅ Translation complete!")
        st.text_area("📝 Translated Text", translated, height=150)

        # gTTS Speech
        if st.button("🔊 Listen"):
            tts = gTTS(translated, lang=tgt_lang)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                tts.save(tmpfile.name)
                st.audio(tmpfile.name, format="audio/mp3")
        
        # Download Option
        st.download_button("⬇️ Download Translation", translated, file_name="translation.txt")

# UI footer
st.markdown("---")
st.markdown("✅ Built with 🤗 Transformers and gTTS | 🎨 Enhanced with Streamlit")
