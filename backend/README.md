# Madlen AI Chat - Backend

FastAPI-based backend service for the Madlen AI Chat application, featuring OpenRouter integration, OpenTelemetry tracing, and SQLite database.

## Features

- RESTful API with FastAPI
- OpenRouter AI model integration
- SQLite database with SQLAlchemy ORM
- OpenTelemetry distributed tracing
- Jaeger integration for trace visualization
- Async/await throughout for performance
- Comprehensive error handling
- Automatic API documentation

## Technology Stack

- **FastAPI 0.115.0** - Modern async web framework
- **SQLAlchemy 2.0.36** - Database ORM
- **SQLite** - Lightweight database
- **OpenTelemetry** - Distributed tracing
- **Pydantic** - Data validation
- **HTTPX** - Async HTTP client
- **Uvicorn** - ASGI server

## Project Structure

```
backend/
├── app/
│   ├── routes/
│   │   ├── chat.py           # Chat endpoints
│   │   ├── models.py         # Model listing
│   │   └── sessions.py       # Session management
│   ├── services/
│   │   ├── openrouter.py     # OpenRouter API client
│   │   └── session_service.py # Database operations
│   ├── telemetry/
│   │   └── tracer.py         # OpenTelemetry setup
│   ├── config.py             # Configuration management
│   ├── database.py           # Database setup
│   ├── models.py             # SQLAlchemy models
│   └── main.py               # Application entry point
├── docker-compose.yml        # Jaeger container
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
└── README.md                 # This file
```

## Installation

### Prerequisites

- Python 3.10 or higher
- Docker Desktop (for Jaeger)
- OpenRouter API key

### Setup

1. **Create Virtual Environment**

```bash
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure Environment**

Create `.env` file:

```env
# OpenRouter Configuration
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# Application
APP_NAME=Madlen AI Chat
APP_VERSION=1.0.0
DEBUG=True

# Database
DATABASE_URL=sqlite:///./chat.db

# CORS
CORS_ORIGINS=["http://localhost:5173","http://127.0.0.1:5173"]

# OpenTelemetry / Jaeger
JAEGER_ENDPOINT=http://localhost:4317
OTEL_SERVICE_NAME=madlen-chat-backend
ENABLE_TRACING=True
```

4. **Start Jaeger**

```bash
docker-compose up -d
```

5. **Run Backend**

```bash
python -m uvicorn app.main:app --reload
```

The backend will start at `http://localhost:8000`

## API Endpoints

### Health Checks

**GET /**
```json
{
  "message": "Madlen AI Chat Backend",
  "version": "1.0.0",
  "status": "running"
}
```

**GET /health**
```json
{
  "status": "healthy",
  "service": "Madlen AI Chat",
  "version": "1.0.0",
  "tracing_enabled": true
}
```

### Models

**GET /models/**

List all available free AI models with vision support detection.

Response:
```json
[
  {
    "id": "qwen/qwen-2-vl-7b-instruct:free",
    "name": "📷 Qwen 2 VL 7B Instruct (free)",
    "description": "Vision-language model...",
    "context_length": 32768,
    "supports_vision": true,
    "pricing": {
      "prompt": "0",
      "completion": "0"
    }
  }
]
```

### Sessions

**GET /sessions/**

Get all chat sessions.

**GET /sessions/{session_id}**

Get specific session with messages.

**POST /sessions/**

Create new session.

Request:
```json
{
  "model_id": "meta-llama/llama-3.2-3b-instruct:free",
  "title": "My Chat"
}
```

**PATCH /sessions/{session_id}**

Update session title.

**DELETE /sessions/{session_id}**

Delete session.

### Chat

**POST /chat/**

Send message and get AI response.

Request:
```json
{
  "model": "meta-llama/llama-3.2-3b-instruct:free",
  "messages": [
    {
      "role": "user",
      "content": "Hello!"
    }
  ],
  "session_id": "optional-session-id",
  "max_tokens": 1000,
  "temperature": 0.7
}
```

Multi-modal request (with image):
```json
{
  "model": "qwen/qwen-2-vl-7b-instruct:free",
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "What's in this image?"},
        {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,..."}}
      ]
    }
  ],
  "session_id": "optional-session-id"
}
```

## Database Schema

### ChatSession

```python
class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    model_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
```

### Message

```python
class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True)
    session_id = Column(String, ForeignKey("chat_sessions.id", ondelete="CASCADE"))
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    extra_metadata = Column(JSON, nullable=True)
    
    session = relationship("ChatSession", back_populates="messages")
```

## OpenTelemetry Integration

### Instrumentation

The application is fully instrumented with OpenTelemetry:

- **FastAPI** - Automatic request/response tracing
- **HTTPX** - HTTP client request tracing
- **Custom Spans** - Business logic tracing

### Trace Examples

```python
with tracer.start_as_current_span("openrouter.chat_completion") as span:
    span.set_attribute("model", model)
    span.set_attribute("message_count", len(messages))
    # ... operation
```

### Viewing Traces

1. Start Jaeger: `docker-compose up -d`
2. Open Jaeger UI: `http://localhost:16686`
3. Select service: `madlen-chat-backend`
4. Click "Find Traces"

## Smart Features

### Free Model Filtering

Only free models are returned:

```python
free_models = [
    model for model in all_models
    if model.get("pricing", {}).get("prompt", "1") == "0"
    and model.get("pricing", {}).get("completion", "1") == "0"
]
```

### Vision Support Detection

Automatically detects image-capable models:

```python
def _check_vision_support(self, model: Dict[str, Any]) -> bool:
    arch = model.get("architecture", {})
    input_modalities = arch.get("input_modalities", [])
    return "image" in input_modalities
```

### Session Persistence

Messages are automatically saved when `session_id` is provided in chat requests.

## Configuration

### Settings Management

All configuration through Pydantic settings:

```python
from app.config import settings

settings.OPENROUTER_API_KEY
settings.ENABLE_TRACING
settings.DATABASE_URL
```

### Environment Variables

- `OPENROUTER_API_KEY` - Required for OpenRouter API
- `ENABLE_TRACING` - Enable/disable OpenTelemetry (default: True)
- `DEBUG` - Debug mode (default: False)
- `DATABASE_URL` - Database connection string
- `CORS_ORIGINS` - Allowed frontend origins
- `JAEGER_ENDPOINT` - Jaeger collector endpoint

## Development

### Running with Debug Mode

```bash
python -m uvicorn app.main:app --reload --log-level debug
```

### Testing API

Visit `http://localhost:8000/docs` for interactive Swagger documentation.

### Database Management

Database file: `./chat.db`

To reset:
```bash
rm chat.db
# Restart app - tables auto-created
```

## Error Handling

All endpoints include comprehensive error handling:

```python
try:
    # operation
except Exception as e:
    span.record_exception(e)
    raise HTTPException(status_code=500, detail=str(e))
```

## Performance

- **Async Operations** - All I/O operations are async
- **Connection Pooling** - Database connection reuse
- **Batch Span Processing** - Efficient trace export
- **Lazy Loading** - Models loaded on demand

## Security

- API keys stored in environment variables
- CORS configuration for frontend access
- SQL injection prevention via SQLAlchemy
- Input validation with Pydantic

## Deployment

### Production Checklist

1. Set `DEBUG=False`
2. Use production database (PostgreSQL)
3. Configure proper CORS origins
4. Set up SSL/TLS
5. Use production ASGI server (Gunicorn + Uvicorn)
6. Configure Jaeger backend (not Docker)

### Example Deployment

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

### Database Locked

```bash
# Stop all instances
# Delete chat.db
# Restart
```

### Jaeger Connection Failed

```bash
# Check Docker
docker ps

# Restart Jaeger
docker-compose restart
```

### OpenRouter API Errors

- Verify API key is correct
- Check rate limits
- Ensure internet connection

## API Documentation

Interactive Swagger UI: `http://localhost:8000/docs`

ReDoc documentation: `http://localhost:8000/redoc`

## Dependencies

See `requirements.txt` for complete list.

Key dependencies:
- fastapi==0.115.0
- sqlalchemy==2.0.36
- opentelemetry-instrumentation-fastapi==0.49b2
- httpx==0.27.2
- pydantic-settings==2.6.1
