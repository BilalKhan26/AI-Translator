import streamlit as st
from transformers import pipeline
from gtts import gTTS
from PIL import Image
import pytesseract
import PyPDF2
import docx
import tempfile
import os

st.set_page_config(page_title="🌍 AI Translator", layout="wide")

st.title("🌐 AI Translator")
st.markdown("### 🔤 Translate text, documents, and images to **Urdu**.")
st.markdown("Upload a file or enter text manually to get started.")

# Define translation pipeline
@st.cache_resource
def get_translator():
    return pipeline("translation", model="Helsinki-NLP/opus-mt-en-ur")

translator = get_translator()

# Translate function
def translate_text(text):
    result = translator(text)
    return result[0]['translation_text']

# Text input
input_text = st.text_area("✍️ Enter text in English", height=150)

# Upload options
uploaded_file = st.file_uploader("📎 Upload a DOCX, PDF, TXT or Image file", type=["docx", "pdf", "txt", "png", "jpg", "jpeg"])

# Extract text from file
def extract_text_from_file(file):
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    elif file.type.startswith("image/"):
        img = Image.open(file)
        return pytesseract.image_to_string(img)
    elif file.type == "text/plain":
        return str(file.read(), "utf-8")
    return ""

if uploaded_file:
    extracted_text = extract_text_from_file(uploaded_file)
    st.text_area("📝 Extracted Text", extracted_text, height=200)
    input_text = extracted_text  # auto fill input

if st.button("🌐 Translate to Urdu"):
    if input_text.strip():
        translated = translate_text(input_text)
        st.success("✅ Translated Text:")
        st.text_area("📄 Urdu Translation", translated, height=150)

        # TTS
        tts = gTTS(translated, lang='ur')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.save(tmp.name)
            st.audio(tmp.name, format="audio/mp3")
            with open(tmp.name, "rb") as audio_file:
                st.download_button("⬇️ Download Urdu Audio", audio_file, file_name="translation.mp3")
    else:
        st.warning("❗ Please enter or upload some text first.")
