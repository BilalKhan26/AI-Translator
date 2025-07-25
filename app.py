import streamlit as st
from transformers import MarianMTModel, MarianTokenizer
from gtts import gTTS
import os
import tempfile
import logging
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page config
st.set_page_config(
    page_title="AI Translator 🌍",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit style
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Language mapping with model availability
LANGUAGE_CODES = {
    "English": "en",
    "Urdu": "ur",
    "Hindi": "hi",
    "Arabic": "ar",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru"
}

# Available translation pairs (Helsinki-NLP models)
AVAILABLE_PAIRS = {
    ("en", "ur"), ("en", "hi"), ("en", "ar"), ("en", "fr"),
    ("en", "es"), ("en", "de"), ("en", "it"), ("en", "pt"), ("en", "ru"),
    ("fr", "en"), ("es", "en"), ("de", "en"), ("it", "en"),
    ("pt", "en"), ("ru", "en"), ("ar", "en")
}

# Load model and tokenizer with error handling
@st.cache_resource
def load_model_and_tokenizer(src_lang, tgt_lang):
    try:
        model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
        logger.info(f"Loading model: {model_name}")
        
        with st.spinner(f"Loading translation model ({src_lang} → {tgt_lang})..."):
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            model = MarianMTModel.from_pretrained(model_name)
            
        logger.info(f"Successfully loaded model: {model_name}")
        return tokenizer, model
        
    except Exception as e:
        logger.error(f"Failed to load model {model_name}: {str(e)}")
        st.error(f"❌ Translation model not available for {src_lang} → {tgt_lang}")
        return None, None

def is_translation_available(src_lang, tgt_lang):
    """Check if translation pair is available"""
    return (src_lang, tgt_lang) in AVAILABLE_PAIRS

# Translate text with error handling
def translate_text(text, tokenizer, model):
    try:
        # Limit input length to prevent memory issues
        if len(text) > 1000:
            text = text[:1000]
            st.warning("⚠️ Text truncated to 1000 characters for processing.")
        
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        
        # Generate translation with parameters for better quality
        with torch.no_grad():
            translated = model.generate(
                **inputs,
                max_length=512,
                num_beams=4,
                early_stopping=True,
                do_sample=False
            )
        
        result = tokenizer.decode(translated[0], skip_special_tokens=True)
        logger.info("Translation completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Translation failed: {str(e)}")
        st.error(f"❌ Translation failed: {str(e)}")
        return None

# Text-to-speech using gTTS with error handling
def speak(text, lang_code):
    try:
        # Limit text length for TTS
        if len(text) > 500:
            text = text[:500]
            st.info("🔊 Audio truncated to 500 characters.")
        
        tts = gTTS(text=text, lang=lang_code, slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            logger.info(f"TTS audio generated for language: {lang_code}")
            return fp.name
            
    except Exception as e:
        logger.error(f"TTS failed for {lang_code}: {str(e)}")
        raise e

# App layout
st.title("🌐 AI Translator with Voice Output")
st.markdown("---")

# Create columns for better layout
col1, col2 = st.columns(2)

with col1:
    src_lang = st.selectbox("🔤 From Language", list(LANGUAGE_CODES.keys()), index=0)

with col2:
    tgt_lang = st.selectbox("🎯 To Language", list(LANGUAGE_CODES.keys()), index=1)

# Input text area
input_text = st.text_area(
    "📝 Enter text to translate",
    height=150,
    placeholder="Type your text here...",
    help="Maximum 1000 characters"
)

# Character counter
if input_text:
    char_count = len(input_text)
    if char_count > 1000:
        st.error(f"❌ Text too long: {char_count}/1000 characters")
    else:
        st.info(f"📊 Characters: {char_count}/1000")

# Translation button
if st.button("🚀 Translate", type="primary"):
    if input_text.strip() == "":
        st.warning("⚠️ Please enter some text to translate.")
    elif src_lang == tgt_lang:
        st.info("✅ Same language selected. No translation needed.")
        st.text_area("📄 Original Text", input_text, height=150)
    else:
        src_code = LANGUAGE_CODES[src_lang]
        tgt_code = LANGUAGE_CODES[tgt_lang]
        
        # Check if translation pair is available
        if not is_translation_available(src_code, tgt_code):
            st.error(f"❌ Translation from {src_lang} to {tgt_lang} is not available.")
            st.info("💡 Try translating through English as an intermediate language.")
        else:
            # Load model and translate
            tokenizer, model = load_model_and_tokenizer(src_code, tgt_code)
            
            if tokenizer and model:
                output_text = translate_text(input_text, tokenizer, model)
                
                if output_text:
                    st.success("✅ Translation Complete!")
                    st.text_area("🎯 Translated Text", output_text, height=150)
                    
                    # Add copy button functionality
                    st.code(output_text, language=None)
                    
                    # TTS output
                    st.markdown("### 🔊 Audio Output")
                    try:
                        with st.spinner("Generating audio..."):
                            audio_file = speak(output_text, tgt_code)
                            st.audio(audio_file)
                            
                        # Clean up temp file
                        if os.path.exists(audio_file):
                            os.unlink(audio_file)
                            
                    except Exception as e:
                        st.warning(f"🔇 Text-to-speech not available for '{tgt_lang}'. Error: {str(e)}")

# Add footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🤖 Powered by HuggingFace Transformers | 🎵 Voice by Google TTS</p>
    </div>
    """,
    unsafe_allow_html=True
)
