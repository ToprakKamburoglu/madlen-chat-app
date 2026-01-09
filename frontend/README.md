# Madlen AI Chat - Frontend

Modern React-based frontend for the Madlen AI Chat application, featuring TypeScript, TailwindCSS, and a professional user interface.

## Features

- Modern React 18 with TypeScript
- Responsive design with TailwindCSS
- Real-time chat interface
- Multi-modal support (image uploads)
- Session management
- Model selection with visual indicators
- Error handling and loading states
- Professional UI/UX

## Technology Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Fast build tool
- **TailwindCSS 3** - Utility-first CSS
- **Axios** - HTTP client
- **Lucide React** - Icon library

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatInput.tsx       # Message input with image upload
│   │   ├── ChatMessage.tsx     # Message display component
│   │   ├── ErrorMessage.tsx    # Error display component
│   │   ├── LoadingSpinner.tsx  # Loading indicator
│   │   ├── ModelSelector.tsx   # AI model selection
│   │   └── Sidebar.tsx         # Session list sidebar
│   ├── services/
│   │   └── api.ts              # Backend API client
│   ├── types/
│   │   └── index.ts            # TypeScript interfaces
│   ├── App.tsx                 # Main application component
│   ├── main.tsx                # Application entry point
│   └── index.css               # Global styles
├── public/
│   └── logo.jpg                # Application logo
├── package.json                # Dependencies
├── tsconfig.json               # TypeScript configuration
├── vite.config.ts              # Vite configuration
├── tailwind.config.js          # TailwindCSS configuration
├── .env                        # Environment variables
└── README.md                   # This file
```

## Installation

### Prerequisites

- Node.js 18 or higher
- npm or yarn

### Setup

1. **Install Dependencies**

```bash
npm install
```

2. **Configure Environment**

Create `.env` file:

```env
VITE_API_BASE_URL=http://localhost:8000
```

3. **Run Development Server**

```bash
npm run dev
```

The frontend will start at `http://localhost:5173`

## Available Scripts

```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## Components

### App.tsx

Main application component managing:
- Application state
- Model loading
- Session management
- Chat functionality
- Image upload handling

### ChatMessage.tsx

Displays individual messages with:
- User/Assistant differentiation
- Image display for multi-modal messages
- Model name for AI responses
- Timestamp

```tsx
<ChatMessage 
  message={message}
  modelName="Qwen 2 VL 7B Instruct"
/>
```

### ChatInput.tsx

Message input component with:
- Text input field
- Image upload button
- Image preview
- Send button
- Disabled state handling

```tsx
<ChatInput
  onSendMessage={handleSendMessage}
  disabled={isLoading}
  supportsImages={currentModelSupportsImages}
/>
```

### ModelSelector.tsx

Model selection dropdown with:
- Model list with context length
- Visual indicators for vision support
- Model details display
- Disabled state

```tsx
<ModelSelector
  models={models}
  selectedModel={selectedModel}
  onSelectModel={setSelectedModel}
  disabled={isLoading}
/>
```

### Sidebar.tsx

Session management sidebar with:
- Session list
- New chat button
- Current session highlighting
- Delete session functionality

```tsx
<Sidebar
  sessions={sessions}
  currentSessionId={currentSession?.id}
  onSelectSession={handleSelectSession}
  onNewChat={handleNewChat}
  onDeleteSession={handleDeleteSession}
/>
```

### ErrorMessage.tsx

Error display component with:
- Error message
- Close button
- Fade-in animation

```tsx
<ErrorMessage
  message="Failed to send message"
  onClose={() => setError(null)}
/>
```

### LoadingSpinner.tsx

Loading indicator with:
- Animated spinner
- Optional message
- Center alignment

```tsx
<LoadingSpinner message="AI is thinking..." />
```

## API Service

### api.ts

Centralized API client with:
- Axios configuration
- Type-safe methods
- Snake_case to camelCase transformation
- Error handling

```typescript
// Get models
const models = await apiService.getModels();

// Send message
const response = await apiService.sendMessage({
  model: selectedModel,
  messages: [...],
  session_id: sessionId
});

// Create session
const session = await apiService.createSession(modelId, title);
```

## Type Definitions

### types/index.ts

TypeScript interfaces for:
- AIModel
- Message
- ChatSession
- API requests/responses
- App state

```typescript
interface AIModel {
  id: string;
  name: string;
  description?: string;
  context_length?: number;
  supports_vision?: boolean;
  pricing?: {
    prompt: string;
    completion: string;
  };
}

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  imageUrl?: string;
}

interface ChatSession {
  id: string;
  title: string;
  modelId: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}
```

## Styling

### TailwindCSS

Custom configuration:

```javascript
// tailwind.config.js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        gray: {
          750: '#2d3748',
          // ...
        }
      }
    },
  },
  plugins: [],
}
```

### Global Styles

```css
/* index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  @apply bg-gray-900 text-white;
}

.fade-in {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

## Features Implementation

### Image Upload

```typescript
const handleSendMessage = async (content: string, imageFile?: File) => {
  if (imageFile) {
    const base64 = await fileToBase64(imageFile);
    messageContent = [
      { type: 'text', text: content },
      { type: 'image_url', image_url: { url: base64 } }
    ];
  }
  // Send to API
};
```

### Vision Model Detection

```typescript
const currentModelSupportsImages = models
  .find((m) => m.id === selectedModel)
  ?.supports_vision || false;
```

### Session Management

```typescript
const handleSelectSession = async (sessionId: string) => {
  const session = await apiService.getSession(sessionId);
  setCurrentSession(session);
  setSelectedModel(session.modelId);
};
```

### Error Handling

```typescript
try {
  const response = await apiService.sendMessage(request);
  // Handle success
} catch (err: any) {
  setError(
    err.response?.data?.detail ||
    'Failed to send message. Please try again.'
  );
}
```

## State Management

Application state managed with React hooks:

```typescript
const [models, setModels] = useState<AIModel[]>([]);
const [selectedModel, setSelectedModel] = useState<string>('');
const [sessions, setSessions] = useState<ChatSession[]>([]);
const [currentSession, setCurrentSession] = useState<ChatSession | null>(null);
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState<string | null>(null);
```

## Performance Optimizations

- **useEffect** with proper dependencies
- **Auto-scroll** to latest message
- **Debounced** API calls
- **Lazy loading** of images
- **Memoization** where appropriate

## Responsive Design

The application is fully responsive:
- Mobile-first design
- Flexible layouts
- Touch-friendly buttons
- Responsive sidebar

## Build Configuration

### Vite Configuration

```typescript
// vite.config.ts
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true
  }
})
```

### TypeScript Configuration

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

## Development

### Hot Module Replacement

Vite provides instant HMR for fast development:
- Component updates without full reload
- State preservation
- CSS hot reload

### Dev Tools

- React DevTools for component inspection
- TypeScript compiler for type checking
- ESLint for code quality

## Building for Production

```bash
# Build
npm run build

# Preview
npm run preview
```

Build output in `dist/` directory.

## Deployment

### Vercel

```bash
npm run build
# Deploy dist/ directory
```

### Netlify

```bash
npm run build
# Deploy dist/ directory
```

### Environment Variables

Set `VITE_API_BASE_URL` to production backend URL.

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Accessibility

- Semantic HTML
- ARIA labels where needed
- Keyboard navigation
- Screen reader friendly

## Security

- No sensitive data in localStorage
- XSS prevention with React
- CORS handled by backend
- Environment variables for configuration

## Troubleshooting

### Port Already in Use

```bash
# Change port in package.json
vite --port 3000
```

### Build Errors

```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

### TypeScript Errors

```bash
# Check types
npm run type-check
```

## Code Quality

- TypeScript strict mode
- ESLint configuration
- Consistent code formatting
- Component composition
- Custom hooks

## Dependencies

Key dependencies:
- react@18.3.1
- typescript@5.6.2
- vite@6.0.5
- tailwindcss@3.4.17
- axios@1.7.9
- lucide-react@0.468.0

See `package.json` for complete list.

