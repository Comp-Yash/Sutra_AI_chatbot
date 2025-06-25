# 💬 AI Mentor & Friend Chatbot

A multilingual AI chatbot powered by Sutra AI that serves as your personal mentor and friend. Built with Streamlit, featuring memory capabilities, web search, and support for multiple Indian languages.

## 🌟 Features

- **Multilingual Support**: Chat in English, Hindi, Marathi, Gujarati, Tamil, Telugu, Kannada, Punjabi, and Bihari
- **Persistent Memory**: Remembers your conversations using Mem0 for personalized interactions
- **Web Search**: Can search the internet for real-time information using DuckDuckGo
- **Empathetic AI**: Sutra responds with human-like empathy and understanding
- **Fallback System**: Multiple layers of API fallback for reliable service
- **Clean UI**: Modern Streamlit interface with real-time chat

## 🏗️ Architecture

The application uses a modular architecture with multiple components:

- **Frontend**: Streamlit web interface
- **AI Model**: Sutra-v2 via Two.ai API
- **Memory**: Mem0 for conversation persistence
- **Agent Framework**: Agno for advanced AI agent capabilities
- **Translation**: Google Translate for multilingual support
- **Search**: DuckDuckGo for web search functionality

## 📋 Prerequisites

- Python 3.8 or higher
- API keys for Sutra AI and Mem0
- Internet connection for API calls and web search

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai-mentor-chatbot
   ```

2. **Install required packages**
   ```bash
   pip install streamlit requests mem0 agno openai googletrans==4.0.0rc1
   ```

3. **Set up API keys**
   
   The application requires two API keys that are currently hardcoded in the script:
   - **Sutra API Key**: For the AI model
   - **Mem0 API Key**: For memory functionality
   
   > ⚠️ **Security Note**: In production, move these keys to environment variables or a secure configuration file.

## 🔧 Configuration

### API Keys Setup

Replace the hardcoded API keys in the script with your own:

```python
SUTRA_API_KEY = "your_sutra_api_key_here"
MEM0_API_KEY = "your_mem0_api_key_here"
```

### Environment Variables (Recommended)

For better security, use environment variables:

```python
SUTRA_API_KEY = os.getenv("SUTRA_API_KEY", "your_default_key")
MEM0_API_KEY = os.getenv("MEM0_API_KEY", "your_default_key")
```

Then set them in your environment:
```bash
export SUTRA_API_KEY="your_sutra_api_key"
export MEM0_API_KEY="your_mem0_api_key"
```

## 🏃‍♂️ Running the Application

1. **Start the Streamlit app**
   ```bash
   streamlit run your_script_name.py
   ```

2. **Open your browser**
   
   The app will automatically open at `http://localhost:8501`

3. **Start chatting**
   - Select your preferred language
   - Type your message in the chat input
   - Enjoy conversations with Sutra!

## 🛠️ Dependencies

### Required Packages
- `streamlit` - Web interface
- `requests` - HTTP requests for API calls

### Optional Packages (with graceful fallback)
- `mem0` - Memory functionality
- `agno` - AI agent framework
- `openai` - OpenAI API integration
- `googletrans` - Translation services

## 📁 File Structure

```
ai-mentor-chatbot/
│
├── app.py                 # Main application file
├── README.md              # This file
├── requirements.txt       # Python dependencies

```

## 🔧 Component Status

The application displays real-time status of all components:

- ✅ **Available**: Component is loaded and functional
- ❌ **Unavailable**: Component failed to load (fallback will be used)

## 🌐 Supported Languages

| Language | Code |
|----------|------|
| English | english |
| Hindi | hindi |
| Marathi | marathi |
| Gujarati | gujarati |
| Tamil | tamil |
| Telugu | telugu |
| Kannada | kannada |
| Punjabi | punjabi |
| Bihari | bihari |

## 🧠 Memory System

- **User ID**: Simple session-based (`simple_session_2`)
- **Memory Duration**: 30 days
- **Storage**: English translation for consistency
- **Context**: Automatically included in conversations

## 🔍 Web Search

- **Provider**: DuckDuckGo
- **Integration**: Agno agent framework
- **Usage**: Automatic when relevant information is needed

## 🚨 Error Handling

The application includes comprehensive error handling:

- **Graceful Degradation**: Works even if optional components fail
- **Fallback Systems**: Multiple API fallback options
- **User Feedback**: Clear error messages and warnings
- **Timeout Handling**: 30-second timeout for API calls

## 🛡️ Security Considerations

- **API Keys**: Currently hardcoded (move to environment variables)
- **User Data**: Stored in Mem0 with user consent
- **Network**: All API calls use HTTPS
- **Input Validation**: Basic validation on user inputs

## 🚀 Deployment Options

### Local Development
```bash
streamlit run main.py
```

### Streamlit Cloud
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add secrets in Streamlit Cloud dashboard

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "main.py"]
```

## 🔄 Updates and Maintenance

- **Memory Cleanup**: Automatic 30-day memory retention
- **API Monitoring**: Built-in status checking
- **Dependency Updates**: Regular updates recommended
- **Security Patches**: Monitor for security updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter issues:

1. Check the **System Status** in the app
2. Verify your API keys are valid
3. Ensure all dependencies are installed
4. Check the console for error messages

## 🔮 Future Enhancements

- [ ] Voice input/output capabilities
- [ ] File upload and processing
- [ ] Custom personality settings
- [ ] Advanced memory management
- [ ] Integration with more AI models
- [ ] Mobile app version
- [ ] Advanced analytics dashboard

## 📊 Performance Notes

- **Response Time**: 2-5 seconds typical
- **Memory Usage**: ~100MB base + models
- **Concurrent Users**: Supports multiple sessions
- **Rate Limits**: Depends on API provider limits

---

*Made with ❤️ using Streamlit and Sutra AI*

**Version**: 1.0.0  
**Last Updated**: June 2025
