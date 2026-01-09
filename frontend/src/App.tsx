import { useState, useEffect, useRef } from 'react';
import { Sidebar } from './components/Sidebar';
import { ChatMessage } from './components/ChatMessage';
import { ChatInput } from './components/ChatInput';
import { ModelSelector } from './components/ModelSelector';
import { LoadingSpinner } from './components/LoadingSpinner';
import { ErrorMessage } from './components/ErrorMessage';
import { apiService } from './services/api';
import { AIModel, ChatSession, Message } from './types';
import { Bot } from 'lucide-react';

function App() {
  const [models, setModels] = useState<AIModel[]>([]);
  const [selectedModel, setSelectedModel] = useState<string>('');
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [currentSession, setCurrentSession] = useState<ChatSession | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadModels();
    loadSessions();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [currentSession?.messages]);

  const loadModels = async () => {
    try {
      setError(null);
      const modelsData = await apiService.getModels();
      setModels(modelsData);
      if (modelsData.length > 0 && !selectedModel) {
        setSelectedModel(modelsData[0].id);
      }
    } catch (err) {
      setError('Failed to load AI models. Please check your connection.');
      console.error('Error loading models:', err);
    }
  };

  const loadSessions = async () => {
    try {
      const sessionsData = await apiService.getSessions();
      setSessions(sessionsData);
    } catch (err) {
      console.error('Error loading sessions:', err);
    }
  };

  const handleNewChat = async () => {
    if (!selectedModel) {
      setError('Please select a model first');
      return;
    }

    try {
      setError(null);
      const newSession = await apiService.createSession(
        selectedModel,
        `Chat ${sessions.length + 1}`
      );
      setSessions([newSession, ...sessions]);
      setCurrentSession(newSession);
      return newSession; 
    } catch (err) {
      setError('Failed to create new chat session');
      console.error('Error creating session:', err);
      return null;
    }
  };

  const handleSelectSession = async (sessionId: string) => {
    try {
      setError(null);
      const session = await apiService.getSession(sessionId);
      setCurrentSession(session);
      setSelectedModel(session.modelId);
    } catch (err) {
      setError('Failed to load chat session');
      console.error('Error loading session:', err);
    }
  };

  const handleDeleteSession = async (sessionId: string) => {
    if (!confirm('Are you sure you want to delete this chat?')) return;

    try {
      setError(null);
      await apiService.deleteSession(sessionId);
      setSessions(sessions.filter((s) => s.id !== sessionId));
      if (currentSession?.id === sessionId) {
        setCurrentSession(null);
      }
    } catch (err) {
      setError('Failed to delete chat session');
      console.error('Error deleting session:', err);
    }
  };

  const handleSendMessage = async (content: string, imageFile?: File) => {
    
    let session = currentSession;
    if (!session) {
      session = await handleNewChat();
      if (!session) {
        setError('Failed to create chat session');
        return;
      }
    }

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    };

   
    if (imageFile) {
      const base64 = await fileToBase64(imageFile);
      userMessage.imageUrl = base64;
    }

    const updatedSession = {
      ...session,
      messages: [...session.messages, userMessage],
    };
    setCurrentSession(updatedSession);

    setIsLoading(true);
    setError(null);

    try {
     
      let messageContent: any = content;
      
      if (imageFile) {
       
        const base64 = await fileToBase64(imageFile);
        messageContent = [
          { type: 'text', text: content },
          { type: 'image_url', image_url: { url: base64 } },
        ];
      }

      
      const response = await apiService.sendMessage({
        model: selectedModel,
        messages: [
          ...session.messages.map((msg) => ({
            role: msg.role,
            content: msg.content,
          })),
          { role: 'user', content: messageContent },
        ],
        session_id: session.id, 
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.choices[0].message.content,
        timestamp: new Date(),
      };

      const finalSession = {
        ...updatedSession,
        messages: [...updatedSession.messages, assistantMessage],
        updatedAt: new Date(),
      };

      setCurrentSession(finalSession);

      await loadSessions();
      
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          'Failed to send message. Please try again.'
      );
      console.error('Error sending message:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const fileToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result as string);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  };

  const currentModelSupportsImages = models
    .find((m) => m.id === selectedModel)
    ?.supports_vision || false;

  return (
    <div className="flex h-screen bg-gray-900 text-white">
   
      <Sidebar
        sessions={sessions}
        currentSessionId={currentSession?.id || null}
        onSelectSession={handleSelectSession}
        onNewChat={handleNewChat}
        onDeleteSession={handleDeleteSession}
      />

      <div className="flex-1 flex flex-col">
        <div className="bg-gray-800 border-b border-gray-700 p-4">
          <div className="max-w-4xl mx-auto flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Bot size={24} className="text-blue-500" />
              <h1 className="text-xl font-bold">Madlen AI Chat</h1>
            </div>
            <div className="flex-1">
              <ModelSelector
                models={models}
                selectedModel={selectedModel}
                onSelectModel={setSelectedModel}
                disabled={isLoading}
              />
            </div>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto">
          <div className="max-w-4xl mx-auto">
            {error && (
              <div className="p-4">
                <ErrorMessage message={error} onClose={() => setError(null)} />
              </div>
            )}

            {!currentSession ? (
              <div className="flex flex-col items-center justify-center h-full p-8 text-center">
                <Bot size={64} className="text-gray-600 mb-4" />
                <h2 className="text-2xl font-bold mb-2">
                  Welcome to Madlen AI Chat
                </h2>
                <p className="text-gray-400 mb-6">
                  Start a new conversation by clicking "New Chat" or selecting a
                  model and typing below.
                </p>
              </div>
            ) : (
              <>
                {currentSession.messages.map((message) => {
               
                  const messageModel = models.find((m) => m.id === currentSession.modelId);
                  const modelName = messageModel?.name || currentSession.modelId;
                  
                  return (
                    <ChatMessage 
                      key={message.id} 
                      message={message}
                      modelName={message.role === 'assistant' ? modelName : undefined}
                    />
                  );
                })}

                {isLoading && (
                  <div className="p-4">
                    <LoadingSpinner message="AI is thinking..." />
                  </div>
                )}

                <div ref={messagesEndRef} />
              </>
            )}
          </div>
        </div>

        <div className="max-w-4xl mx-auto w-full">
          <ChatInput
            onSendMessage={handleSendMessage}
            disabled={isLoading || !selectedModel}
            supportsImages={currentModelSupportsImages}
          />
        </div>
      </div>
    </div>
  );
}

export default App;