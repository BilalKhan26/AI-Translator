# 🌐 AI Translator App

A production-ready AI Translator built with Streamlit, featuring real-time translation and text-to-speech capabilities.

## ✨ Features

- 🔤 **Multi-language Translation**: Support for 10+ languages including English, Urdu, Hindi, Arabic, French, Spanish, German, Italian, Portuguese, and Russian
- 🎵 **Text-to-Speech**: Voice output for translated text using Google TTS
- 🚀 **Real-time Translation**: Powered by HuggingFace Transformers
- 📱 **Responsive UI**: Clean, modern interface with emoji indicators
- 🔧 **Production Ready**: Optimized for deployment with error handling and logging
- 🐳 **Docker Support**: Containerized deployment ready
- ⚡ **Performance Optimized**: Model caching and memory management

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd AI-Translator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

### Using Docker

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Or build manually**
   ```bash
   docker build -t ai-translator .
   docker run -p 8501:8501 ai-translator
   ```

## 🌐 Deployment Options

### 1. Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Set `app.py` as the main file
5. Deploy!

### 2. Heroku

1. **Install Heroku CLI** and login
   ```bash
   heroku login
   ```

2. **Create a new Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

### 3. Railway

1. Connect your GitHub repository to [Railway](https://railway.app)
2. Railway will automatically detect the Python app
3. Set the start command: `streamlit run app.py --server.port=$PORT`

### 4. Google Cloud Run

1. **Build and push to Google Container Registry**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT-ID/ai-translator
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy --image gcr.io/PROJECT-ID/ai-translator --platform managed
   ```

### 5. AWS ECS/Fargate

1. **Push to Amazon ECR**
   ```bash
   aws ecr get-login-password --region region | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com
   docker build -t ai-translator .
   docker tag ai-translator:latest aws_account_id.dkr.ecr.region.amazonaws.com/ai-translator:latest
   docker push aws_account_id.dkr.ecr.region.amazonaws.com/ai-translator:latest
   ```

2. **Create ECS service** using the AWS Console or CLI

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key configuration options:
- `STREAMLIT_SERVER_PORT`: Server port (default: 8501)
- `MAX_TEXT_LENGTH`: Maximum input text length (default: 1000)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, ERROR)

### Streamlit Configuration

The app includes a `.streamlit/config.toml` file with optimized settings for production deployment.

## 📋 Supported Translation Pairs

The app supports the following translation directions:
- **From English**: → Urdu, Hindi, Arabic, French, Spanish, German, Italian, Portuguese, Russian
- **To English**: French, Spanish, German, Italian, Portuguese, Russian, Arabic → English

## 🛠️ Development

### Project Structure

```
AI-Translator/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version for deployment
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── .env.example          # Environment variables template
├── .dockerignore         # Docker ignore file
└── README.md             # This file
```

### Adding New Languages

1. Check if Helsinki-NLP has a model for your language pair at [HuggingFace](https://huggingface.co/Helsinki-NLP)
2. Add the language to `LANGUAGE_CODES` in `app.py`
3. Add the translation pair to `AVAILABLE_PAIRS`
4. Test the translation functionality

### Performance Optimization

- Models are cached using `@st.cache_resource`
- Text length is limited to prevent memory issues
- Temporary audio files are cleaned up automatically
- Docker image uses multi-stage builds for smaller size

## 🐛 Troubleshooting

### Common Issues

1. **Model Loading Errors**
   - Ensure internet connection for first-time model downloads
   - Check if the translation pair is supported
   - Verify sufficient disk space for model caching

2. **TTS Not Working**
   - Some languages may not be supported by Google TTS
   - Check internet connection for TTS service

3. **Memory Issues**
   - Reduce `MAX_TEXT_LENGTH` in environment variables
   - Consider using smaller models for resource-constrained environments

### Logs

Check application logs for debugging:
```bash
# Docker
docker logs <container-id>

# Local
tail -f app.log
```

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🙏 Acknowledgments

- [HuggingFace Transformers](https://huggingface.co/transformers/) for translation models
- [Google Text-to-Speech](https://gtts.readthedocs.io/) for voice synthesis
- [Streamlit](https://streamlit.io/) for the web framework
- [Helsinki-NLP](https://huggingface.co/Helsinki-NLP) for the translation models

---

**Built with ❤️ using HuggingFace Transformers and Streamlit**