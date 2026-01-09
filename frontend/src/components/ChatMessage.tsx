import { Message } from '../types';
import { User, Bot, Sparkles } from 'lucide-react';

interface ChatMessageProps {
  message: Message;
  modelName?: string; 
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message, modelName }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex gap-4 p-4 ${isUser ? 'bg-gray-800' : 'bg-gray-750'} fade-in`}>
      <div className="flex-shrink-0">
        <div
          className={`w-8 h-8 rounded-full flex items-center justify-center ${
            isUser ? 'bg-blue-600' : 'bg-green-600'
          }`}
        >
          {isUser ? <User size={20} /> : <Bot size={20} />}
        </div>
      </div>

      <div className="flex-1 space-y-2">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="font-semibold text-sm">
            {isUser ? 'You' : 'AI Assistant'}
          </span>
        
          {!isUser && modelName && (
            <span className="text-xs text-gray-400 flex items-center gap-1">
              <Sparkles size={12} />
              {modelName}
            </span>
          )}
          
          <span className="text-xs text-gray-400">
            {new Date(message.timestamp).toLocaleTimeString()}
          </span>
        </div>
        {message.imageUrl && (
          <div className="my-2">
            <img
              src={message.imageUrl}
              alt="Uploaded"
              className="max-w-md max-h-64 rounded-lg border border-gray-600 object-contain"
            />
          </div>
        )}

        <div className="text-gray-100 whitespace-pre-wrap break-words">
          {message.content}
        </div>
      </div>
    </div>
  );
};