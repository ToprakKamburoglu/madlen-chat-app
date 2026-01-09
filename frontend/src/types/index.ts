// API Models
export interface AIModel {
  id: string;
  name: string;
  description?: string;
  context_length?: number;
  pricing?: {
    prompt: string;
    completion: string;
  };
  top_provider?: {
    max_completion_tokens?: number;
  };
  supports_vision?: boolean; // ✅ Added for multi-modal support detection
}

// Chat Messages
export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  imageUrl?: string; // For multi-modal support
}

// Chat Session
export interface ChatSession {
  id: string;
  title: string;
  modelId: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}

// API Request/Response types
export interface SendMessageRequest {
  model: string;
  messages: {
    role: string;
    content: string | Array<{ type: string; text?: string; image_url?: { url: string } }>;
  }[];
}

export interface SendMessageResponse {
  id: string;
  model: string;
  choices: {
    message: {
      role: string;
      content: string;
    };
    finish_reason: string;
  }[];
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

// App State
export interface AppState {
  currentSession: ChatSession | null;
  sessions: ChatSession[];
  selectedModel: string;
  availableModels: AIModel[];
  isLoading: boolean;
  error: string | null;
}