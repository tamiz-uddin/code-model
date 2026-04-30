# 💻 Code Model Chat UI

A beautiful web-based chat interface to interact with code generation models.

## 🚀 Quick Start

### 1. Start the Chat Server

```bash
python chat_ui.py
```

### 2. Open in Browser

Open your browser and go to:
```
http://localhost:5000
```

### 3. Start Chatting!

- Select a model from the left sidebar
- Type your code prompt
- Press Enter or click Send
- Get generated code instantly

## 🎨 Features

✅ **Beautiful UI**
- Modern gradient design
- Smooth animations
- Responsive layout
- Dark/Light messages

✅ **Model Selection**
- Foundation (JavaScript, Python)
- Frontend (+ HTML, CSS)
- Full-Stack (+ React, Express, Django, Flask, SQL)
- Universal (All languages)

✅ **Chat Features**
- Real-time code generation
- Message history
- Clear chat button
- Status indicator
- Loading animation

✅ **Responsive Design**
- Works on desktop
- Works on tablet
- Works on mobile

## 📝 Examples

### JavaScript
```
Prompt: function fibonacci
```

### Python
```
Prompt: def merge_sort
```

### SQL
```
Prompt: SELECT * FROM users
```

### TypeScript
```
Prompt: interface User
```

### Java
```
Prompt: public class
```

### Go
```
Prompt: func main
```

### Rust
```
Prompt: fn main
```

### C#
```
Prompt: public class
```

### HTML
```
Prompt: <div class='container'>
```

### React
```
Prompt: function Counter
```

## 🔧 API Endpoints

### GET /api/models
Get list of available models

**Response:**
```json
[
  {
    "name": "foundation",
    "file": "foundation-model-v1.pt",
    "description": "JavaScript, Python"
  },
  ...
]
```

### POST /api/generate
Generate code from prompt

**Request:**
```json
{
  "prompt": "function add",
  "model": "universal-model-v1.pt",
  "max_length": 100
}
```

**Response:**
```json
{
  "success": true,
  "prompt": "function add",
  "generated": "function add(a, b) { return a + b; }",
  "model": "universal-model-v1.pt",
  "device": "cpu"
}
```

### GET /api/health
Health check

**Response:**
```json
{
  "status": "ok",
  "device": "cpu",
  "model_loaded": true
}
```

## 🎯 Usage Tips

1. **Select Model First**
   - Choose the appropriate model for your task
   - Foundation for basic code
   - Frontend for HTML/CSS
   - Full-Stack for frameworks
   - Universal for all languages

2. **Write Clear Prompts**
   - Be specific about what you want
   - Include language hints
   - Provide context if needed

3. **Examples of Good Prompts**
   - "function fibonacci(n)"
   - "def merge_sort(arr)"
   - "SELECT * FROM users WHERE age > 18"
   - "interface User { name: string; age: number; }"

4. **Examples of Bad Prompts**
   - "code"
   - "function"
   - "something"

## 🌐 Deployment

### Local Development
```bash
python chat_ui.py
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 chat_ui:app
```

### Docker
```bash
docker build -t code-model-chat .
docker run -p 5000:5000 code-model-chat
```

### Cloud Deployment
- Heroku
- AWS Lambda
- Google Cloud Run
- Azure App Service

## 📊 Performance

- **Response Time**: ~2 seconds
- **Model Size**: 168.6 MB
- **Memory Usage**: ~2 GB
- **GPU Support**: Optional (CPU fallback)

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use different port
python chat_ui.py --port 5001
```

### Model Not Found
```bash
# Check models exist
ls -la outputs/models/
```

### Slow Generation
- Use Foundation model for faster generation
- Reduce max_length parameter
- Use GPU if available

### Connection Refused
- Make sure server is running
- Check firewall settings
- Try http://localhost:5000

## 📚 Documentation

- **SETUP_GUIDE.md** - Installation & setup
- **QUICK_START.md** - Quick start guide
- **USAGE_GUIDE.md** - Complete documentation
- **generate.py** - Command-line interface
- **api_server.py** - REST API server

## 🚀 Next Steps

1. **Customize UI**
   - Modify templates/chat.html
   - Change colors and styling
   - Add new features

2. **Add Features**
   - Code syntax highlighting
   - Export chat history
   - Save favorite prompts
   - Model comparison

3. **Deploy**
   - Docker containerization
   - Cloud deployment
   - Load balancing
   - Monitoring

4. **Integrate**
   - IDE plugins
   - Slack bot
   - Discord bot
   - Web app

## 📞 Support

For issues or questions:
1. Check the documentation
2. Review the examples
3. Check the logs
4. Open an issue on GitHub

## 📄 License

MIT License - Feel free to use and modify!

---

**Happy coding! 🎉**

Start the chat UI now:
```bash
python chat_ui.py
```

Then open http://localhost:5000 in your browser!
