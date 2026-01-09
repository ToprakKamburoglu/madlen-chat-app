# Madlen AI Chat

![Madlen AI Chat](./frontend/public/logo/logo.jpg)

A modern, production-ready AI chat application with OpenRouter integration, featuring multiple free AI models, multi-modal support, and comprehensive monitoring with OpenTelemetry and Jaeger.

## Project Overview

This web-based chat interface allows users to interact with various AI models through OpenRouter as a gateway. The application supports model selection, chat history management, session persistence, and image uploads for vision-capable models.

## Key Features

**Core Features:**
- Multiple Free AI Models via OpenRouter (10+ models)
- Smart Model Filtering (only free models displayed)
- Multi-modal Support (image uploads for vision models)
- Chat History & Session Management
- Real-time AI Responses
- Professional Modern UI
- Comprehensive Monitoring (OpenTelemetry + Jaeger)

**Enhanced Features:**
- Vision Model Detection with visual indicators
- Model Information Display (context length, capabilities)
- Image Preview for uploads
- Session-based Message Persistence
- Error Handling with user-friendly messages
- Loading States & Visual Feedback
- Responsive Design

## Technology Stack

**Backend:**
- FastAPI - Modern async web framework
- SQLAlchemy - ORM and database management
- SQLite - Lightweight database
- OpenTelemetry - Distributed tracing
- Jaeger - Trace visualization
- HTTPX - Async HTTP client
- Pydantic - Data validation

**Frontend:**
- React 18 - UI library
- TypeScript - Type safety
- Vite - Fast build tool
- TailwindCSS - Utility-first CSS
- Axios - HTTP client
- Lucide React - Icon library

**DevOps:**
- Docker - Containerization
- Docker Compose - Container orchestration

## Project Structure

```
madlen-chat-app/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── routes/       # API endpoints
│   │   ├── services/     # Business logic
│   │   ├── telemetry/    # OpenTelemetry setup
│   │   ├── models.py     # Database models
│   │   ├── database.py   # Database configuration
│   │   └── main.py       # Application entry point
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── README.md
│
├── frontend/             # React application
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── services/     # API services
│   │   ├── types/        # TypeScript types
│   │   └── App.tsx       # Main component
│   ├── package.json
│   └── README.md
│
├── screenshots/          # Project screenshots
└── README.md            # This file
```

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker Desktop (for Jaeger)
- OpenRouter API Key ([Get one here](https://openrouter.ai))

### Installation

**1. Clone the Repository**

```bash
git clone <repository-url>
cd madlen-chat-app
```

**2. Backend Setup**

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Create .env file and add:
OPENROUTER_API_KEY=your_api_key_here
ENABLE_TRACING=True

# Start Jaeger
docker-compose up -d

# Run backend
python -m uvicorn app.main:app --reload
```

Backend will run at `http://localhost:8000`

**3. Frontend Setup**

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Run frontend
npm run dev
```

Frontend will run at `http://localhost:5173`

### Accessing the Application

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Jaeger UI:** http://localhost:16686

## Configuration

### Backend Environment Variables

Create `backend/.env`:

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

### Frontend Environment Variables

Create `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## API Documentation

### Health Check
- `GET /` - Basic health check
- `GET /health` - Detailed health information

### Models
- `GET /models/` - List all free AI models with vision support flags

### Sessions
- `GET /sessions/` - Get all chat sessions
- `GET /sessions/{id}` - Get specific session
- `POST /sessions/` - Create new session
- `PATCH /sessions/{id}` - Update session title
- `DELETE /sessions/{id}` - Delete session

### Chat
- `POST /chat/` - Send message and get AI response

**Interactive API Documentation:** Visit `http://localhost:8000/docs` for Swagger UI

## Monitoring with Jaeger

### Starting Jaeger

```bash
cd backend
docker-compose up -d
```

### Accessing Jaeger UI

Open `http://localhost:16686` in your browser

### Viewing Traces

1. Select `madlen-chat-backend` from the Service dropdown
2. Click "Find Traces"
3. Click on any trace to see detailed spans

### Available Traces

- `GET /models/` - Model fetching from OpenRouter
- `POST /chat/` - Complete chat flow
- `openrouter.chat_completion` - OpenRouter API calls
- `session.create` - Session creation
- `session.add_message` - Message persistence

## Technical Decisions

### Why FastAPI?

- Native async/await support for high performance
- Automatic API documentation (Swagger/OpenAPI)
- Type safety with Pydantic
- Modern Python features
- Excellent for microservices

### Why React + TypeScript?

- Component-based architecture
- Type safety prevents runtime errors
- Large ecosystem and community
- Excellent developer experience
- Production-ready

### Why SQLite?

- Zero configuration required
- Single file database (portable)
- Sufficient performance for local use
- Easy migration path to PostgreSQL
- Perfect for development and demos

### Why OpenTelemetry?

- Industry standard for observability
- Vendor-neutral (works with any backend)
- Production-grade monitoring
- Essential for debugging distributed systems
- Rich ecosystem and tooling

## Smart Features Implementation

### 1. Free Model Filtering

Backend automatically filters only free models:

```python
free_models = [
    model for model in all_models
    if model.get("pricing", {}).get("prompt", "1") == "0"
]
```

### 2. Vision Support Detection

Models are automatically checked for image support:

```python
supports_vision = "image" in model.get("architecture", {}).get("input_modalities", [])
if supports_vision:
    model["name"] = f"📷 {model['name']}"
```

### 3. Session Persistence

All messages saved to SQLite database with cascade delete:

```python
@relationship("Message", back_populates="session", cascade="all, delete-orphan")
```

### 4. Error Handling

Comprehensive try-catch blocks with user-friendly error messages throughout the application.

### 5. Type Safety

Full TypeScript coverage and Pydantic models ensure type safety across the stack.

## Screenshots

### Main Interface
![Main Screen](./screenshots/main-ui.png)
*Chat interface with sidebar, messages, and model information*

### Model Selection
![Model Selection](./screenshots/model-selector.png)
*Model dropdown with vision indicators and context length display*

### Image Upload
![Image Upload](./screenshots/image-upload.png)
*Multi-modal chat with image upload capability*

### Docker Deployment

**Docker Desktop - Containers**
![Docker Containers](./screenshots/docker-containers.png)
*Jaeger container running in Docker Desktop*

**Docker Desktop - Images**
![Docker Images](./screenshots/docker-images.png)
*Jaeger all-in-one image pulled and ready*

**Docker Desktop - Container Logs**
![Docker Logs](./screenshots/docker-logs.png)
*Real-time Jaeger container logs showing trace ingestion*

### Jaeger Monitoring

**Jaeger Traces**
![Jaeger UI](./screenshots/jaeger-traces.png)
*Jaeger UI showing trace list from madlen-chat-backend service*

**Trace Details**
![Trace Details](./screenshots/trace-details.png)
*Detailed view of a chat completion trace with spans*

## Development

### Backend Development

```bash
cd backend
python -m uvicorn app.main:app --reload --log-level debug
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### Code Quality

**Backend:**
- Type hints throughout
- Async/await patterns
- Error handling with spans
- Clean separation of concerns

**Frontend:**
- TypeScript strict mode
- Component composition
- Custom hooks
- Proper error boundaries

## Troubleshooting

### Backend won't start

```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Verify virtual environment
python --version  # Should show venv Python
```

### Frontend won't start

```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

### Jaeger connection errors

```bash
# Check if Docker is running
docker ps

# Restart Jaeger
docker-compose restart
```

### OpenRouter API errors

- Verify API key in `.env`
- Check rate limits (wait a few seconds)
- Ensure internet connection

## Deployment

### Backend (Railway / Render)

```bash
# Procfile
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Frontend (Vercel / Netlify)

```bash
npm run build
# Deploy the dist/ directory
```

### Production Database

Replace SQLite with PostgreSQL:

```python
DATABASE_URL=postgresql://user:pass@host:5432/db
```

## Contributing

This is a case study project. Contributions are welcome for educational purposes.

## License

MIT License - See LICENSE file for details

## Contact

For questions or feedback about this case study:

- GitHub: [Your GitHub Profile]
- LinkedIn: [Your LinkedIn]
- Email: [Your Email]

---

## Project Evaluation & Design Decisions

This section addresses the evaluation criteria for the Madlen case study project.

### 1. Developer Experience

**Easy Setup & Cross-Platform Support:**

- **Single Command Setup:** Both frontend and backend can be started with minimal commands
- **Virtual Environment:** Python venv ensures consistent dependencies across systems
- **Package Manager:** npm for frontend ensures reproducible builds
- **Environment Variables:** Clear `.env` templates prevent configuration errors
- **Docker Compose:** One-command Jaeger setup (`docker-compose up -d`)
- **Comprehensive Documentation:** Step-by-step guides in all README files

**Cross-Platform Compatibility:**

- **Windows, Mac, Linux:** Tested on all major platforms
- **Path Handling:** OS-agnostic paths throughout
- **Port Configuration:** Configurable via environment variables
- **Docker:** Ensures Jaeger works identically everywhere

**Developer Tools:**

- **Hot Reload:** Both frontend (Vite HMR) and backend (`--reload`) support instant updates
- **API Documentation:** Auto-generated Swagger UI at `/docs`
- **Type Safety:** TypeScript + Pydantic catch errors before runtime
- **Linting:** ESLint for code quality

### 2. User Experience & Interface Quality

**Intuitive & Professional UI:**

- **Clean Design:** Modern dark theme with consistent color scheme
- **Responsive Layout:** Works on desktop, tablet, and mobile
- **Visual Hierarchy:** Clear separation of sidebar, header, and chat area
- **Icon Usage:** Lucide icons for intuitive actions (send, upload, delete)

**Real-Time Feedback:**

- **Loading States:** 
  - "Loading models..." in dropdown
  - "AI is thinking..." during responses
  - Spinner animations for visual feedback
  
- **Error Messages:**
  - User-friendly error display component
  - Dismissible error notifications
  - Specific error messages (not generic "error occurred")

- **Success Indicators:**
  - Smooth message animations
  - Auto-scroll to latest message
  - Session highlighting in sidebar

**Professional Polish:**

- **Smooth Transitions:** Fade-in animations for messages
- **Consistent Spacing:** Proper padding and margins throughout
- **Accessible Colors:** High contrast for readability
- **Button States:** Disabled states prevent double-clicks

### 3. Robustness & Error Handling

**API Error Handling:**

```python
# Backend - Comprehensive error handling
try:
    response = await openrouter_service.chat_completion(...)
except Exception as e:
    span.record_exception(e)  # Log to Jaeger
    raise HTTPException(status_code=500, detail=f"Chat completion failed: {str(e)}")
```

```typescript
// Frontend - User-friendly error display
catch (err: any) {
  setError(
    err.response?.data?.detail ||
    'Failed to send message. Please try again.'
  );
}
```

**Defensive Programming:**

- **Input Validation:** Pydantic models validate all API inputs
- **Null Checks:** Optional chaining (`?.`) throughout frontend
- **Default Values:** Fallback models if API fails
- **Database Constraints:** Foreign key constraints prevent orphaned data
- **Rate Limiting Awareness:** Error messages guide users on retry

**Graceful Degradation:**

- **Tracing Optional:** App works even if Jaeger is down
- **Image Upload Optional:** Text-only messages always work
- **Session Optional:** Can chat without creating session
- **Model Fallback:** Default free models if API call fails

### 4. Technical Decisions & Justifications

**FastAPI (Backend Framework)**

**Why:** Modern async Python framework with automatic API documentation
- Native async/await for high performance
- Pydantic integration for type safety
- Auto-generated Swagger docs
- Large community and excellent documentation
- Production-ready with Uvicorn ASGI server

**React + TypeScript (Frontend)**

**Why:** Industry-standard combination for type-safe UIs
- Component-based architecture promotes reusability
- TypeScript prevents runtime errors
- Huge ecosystem of libraries
- Excellent developer experience with Vite
- Battle-tested in production environments

**SQLite (Database)**

**Why:** Perfect for local development and demos
- Zero configuration required
- Single-file portability
- Sufficient performance for single-user
- Easy migration path to PostgreSQL for production
- Built into Python standard library

**TailwindCSS (Styling)**

**Why:** Utility-first CSS for rapid development
- No CSS naming conventions needed
- Consistent design system
- Tiny production bundle with purging
- Responsive design utilities built-in
- Easy customization

**OpenTelemetry + Jaeger (Monitoring)**

**Why:** Industry standard for observability
- Vendor-neutral (works with any backend)
- Rich context propagation
- Essential for debugging distributed systems
- Production-grade monitoring
- Free and open source

**Axios (HTTP Client)**

**Why:** More features than fetch API
- Automatic JSON transformation
- Interceptors for global error handling
- Request/response transformation
- TypeScript support
- Wide adoption

### 5. Additional Features Beyond Requirements

**Enhanced Model Management:**

- **Smart Filtering:** Automatically filters only free models (prevents accidental paid usage)
- **Vision Detection:** Automatic detection of image-capable models
- **Visual Indicators:** 📷 emoji for vision models in dropdown
- **Context Length Display:** Shows token limits for each model (e.g., "131K tokens")
- **Model Details:** Description and capabilities shown below selector

**Improved User Experience:**

- **Model Information:** Displays which AI model generated each response
- **Image Persistence:** Uploaded images saved to database and visible in history
- **Smart Session Handling:** Auto-creates session if user sends message without one
- **Optimistic Updates:** Messages appear instantly (before API confirms)
- **Auto-scroll:** Automatically scrolls to latest message

**Developer Experience:**

- **Type Transformations:** Automatic snake_case to camelCase conversion
- **Error Boundaries:** Comprehensive error handling at every level
- **Hot Module Replacement:** Instant feedback during development
- **API Documentation:** Interactive Swagger UI
- **Code Organization:** Clean separation of concerns

**Production Readiness:**

- **Environment Configuration:** All secrets in environment variables
- **CORS Setup:** Proper cross-origin configuration
- **Database Migrations:** Easy schema updates with SQLAlchemy
- **Docker Support:** Containerized Jaeger for consistent monitoring
- **Logging:** Structured logging with trace correlation

### 6. Code Quality & Organization

**Backend Architecture:**

```
Clear separation of concerns:
- routes/     : API endpoint definitions
- services/   : Business logic
- models.py   : Data models
- database.py : Database setup
- config.py   : Configuration management
```

**Frontend Architecture:**

```
Component-based structure:
- components/ : Reusable UI components
- services/   : API client
- types/      : TypeScript definitions
- App.tsx     : Main application logic
```

**Code Quality Standards:**

- **Type Safety:** 100% TypeScript coverage in frontend, type hints in backend
- **Async/Await:** Proper async patterns throughout
- **Error Handling:** Try-catch blocks with meaningful messages
- **Comments:** Clear documentation for complex logic
- **Naming:** Descriptive variable and function names
- **DRY Principle:** No code duplication

### 7. Testing Considerations

While not implemented due to time constraints, the codebase is structured for easy testing:

**Backend:**
- Unit tests with pytest
- Mock OpenRouter API
- Database fixtures
- Integration tests for endpoints

**Frontend:**
- Component tests with React Testing Library
- Mock API responses
- E2E tests with Playwright

### 8. Scalability & Future Enhancements

**Current Architecture Supports:**

- **Database Migration:** Easy switch from SQLite to PostgreSQL
- **Authentication:** JWT ready (FastAPI security utils)
- **Caching:** Redis integration for model lists
- **Rate Limiting:** Can add rate limiting middleware
- **File Upload:** S3 integration for images
- **Websockets:** Real-time chat with Server-Sent Events

**Potential Enhancements:**

- User authentication and authorization
- Multi-user chat rooms
- Message reactions and editing
- Export chat history
- Custom model parameters (temperature, top_p)
- Streaming responses
- Voice input/output
- Dark/Light theme toggle

---

## Acknowledgments

- OpenRouter for AI model gateway
- FastAPI for the excellent framework
- React team for the UI library
- Jaeger for distributed tracing

---

**Developed as a case study project demonstrating modern full-stack development practices, AI integration, and production-ready monitoring.**
