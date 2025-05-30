import streamlit as st
from transformers import MarianMTModel, MarianTokenizer
from gtts import gTTS
import os
import tempfile

# Set page config
st.set_page_config(page_title="AI Translator 🌍", layout="centered")

# Language mapping
LANGUAGE_CODES = {
    "English": "en",
    "Urdu": "ur",
    "Hindi": "hi",
    "Arabic": "ar",
    "French": "fr",
    "Spanish": "es",
}

# Load model and tokenizer
@st.cache_resource
def load_model_and_tokenizer(src_lang, tgt_lang):
    model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

# Translate text
def translate_text(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

# Text-to-speech using gTTS
def speak(text, lang_code):
    tts = gTTS(text=text, lang=lang_code)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

# App layout
st.title("🌐 AI Translator with Voice Output")

src_lang = st.selectbox("From Language", list(LANGUAGE_CODES.keys()), index=0)
tgt_lang = st.selectbox("To Language", list(LANGUAGE_CODES.keys()), index=1)

input_text = st.text_area("Enter text to translate", height=150)

if st.button("Translate"):
    if input_text.strip() == "":
        st.warning("⚠️ Please enter some text.")
    elif src_lang == tgt_lang:
        st.info("✅ Same language selected. No translation needed.")
        st.write(input_text)
    else:
        src_code = LANGUAGE_CODES[src_lang]
        tgt_code = LANGUAGE_CODES[tgt_lang]
        tokenizer, model = load_model_and_tokenizer(src_code, tgt_code)

        with st.spinner("Translating..."):
            output_text = translate_text(input_text, tokenizer, model)
            st.success("Translation Complete!")
            st.text_area("Translated Text", output_text, height=150)

            # TTS output
            try:
                audio_file = speak(output_text, tgt_code)
                st.audio(audio_file)
            except Exception as e:
                st.warning(f"TTS not available for '{tgt_lang}'. Error: {e}")
