# AI Chatbot with LangGraph & Next.js

A modern, beautiful AI chatbot built with LangGraph, Google Gemini, and Next.js with Tailwind CSS.

## Features

- 🎨 **Beautiful UI**: Modern gradient design with glassmorphism effects
- 💬 **Real-time Chat**: Instant messaging with AI responses
- 🧠 **Powered by LangGraph**: State-of-the-art conversation management
- 🤖 **Google Gemini AI**: Advanced language model for intelligent responses
- 📱 **Responsive Design**: Works perfectly on all devices
- ⚡ **Fast API**: Built with FastAPI for quick responses

## Project Structure

```
chatbot_with_UI/
├── client/                 # Next.js frontend
│   ├── src/
│   │   ├── app/           # Next.js app directory
│   │   ├── components/    # React components
│   │   └── types/         # TypeScript types
│   └── package.json
├── langgraph_backend.py   # LangGraph chatbot logic
├── backend_server.py      # FastAPI server
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

## Setup Instructions

### 1. Backend Setup

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

   Get your Google API key from: https://makersuite.google.com/app/apikey

3. **Start the Backend Server**
   ```bash
   python backend_server.py
   ```

   The backend will run on `http://localhost:8000`

### 2. Frontend Setup

1. **Navigate to Client Directory**
   ```bash
   cd client
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Start the Development Server**
   ```bash
   npm run dev
   ```

   The frontend will run on `http://localhost:3000`

## Usage

1. Make sure both backend and frontend servers are running
2. Open your browser and navigate to `http://localhost:3000`
3. Start chatting with the AI!

## Features in Detail

### Frontend (Next.js + Tailwind CSS)
- **Chat Interface**: Clean, modern chat UI with message bubbles
- **User Experience**: Smooth animations and transitions
- **Responsive**: Works on desktop, tablet, and mobile
- **Theme**: Beautiful dark theme with purple/pink gradients
- **Loading States**: Visual feedback during AI processing

### Backend (FastAPI + LangGraph)
- **LangGraph Integration**: State management for conversations
- **Thread Support**: Maintains conversation context
- **CORS Enabled**: Secure cross-origin requests
- **Error Handling**: Graceful error management
- **Health Check**: API health monitoring

## Technologies Used

### Frontend
- **Next.js 16**: React framework for production
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **React Hooks**: Modern React patterns

### Backend
- **FastAPI**: Modern Python web framework
- **LangGraph**: Conversation state management
- **Google Gemini AI**: Advanced language model
- **Python-dotenv**: Environment variable management

## API Endpoints

### POST /api/chat
Send a message to the chatbot.

**Request Body:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hello, how are you?"
    }
  ],
  "thread_id": "unique-thread-id"
}
```

**Response:**
```json
{
  "role": "assistant",
  "content": "I'm doing well, thank you for asking!"
}
```

### GET /api/health
Check if the API is running.

**Response:**
```json
{
  "status": "healthy"
}
```

## Customization

### Changing the AI Model
Edit `langgraph_backend.py`:
```python
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",  # Change to desired model
    api_key=os.getenv("GOOGLE_API_KEY")
)
```

### Modifying the UI Theme
Edit the gradient colors in `client/src/app/page.tsx` and component files to match your preferred color scheme.

### Adding More Features
The modular structure makes it easy to add:
- Voice input/output
- File upload support
- Conversation history
- User authentication
- Multi-language support

## Troubleshooting

### Backend Connection Issues
- Ensure the backend server is running on port 8000
- Check that your `.env` file contains a valid Google API key
- Verify firewall settings aren't blocking localhost connections

### Frontend Build Errors
- Delete `node_modules` and `package-lock.json`, then run `npm install`
- Ensure you're using Node.js version 18 or higher
- Check that all dependencies are properly installed

### API Errors
- Check the browser console for specific error messages
- Verify the backend server logs for any Python errors
- Ensure CORS is properly configured in `backend_server.py`

## License

This project is open source and available for personal and commercial use.

## Support

For issues or questions, please check the troubleshooting section or create an issue in the repository.