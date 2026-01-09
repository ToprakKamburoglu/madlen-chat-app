import { ChatSession } from '../types';
import { Plus, MessageSquare, Trash2 } from 'lucide-react';

interface SidebarProps {
  sessions: ChatSession[];
  currentSessionId: string | null;
  onSelectSession: (sessionId: string) => void;
  onNewChat: () => void;
  onDeleteSession: (sessionId: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  sessions,
  currentSessionId,
  onSelectSession,
  onNewChat,
  onDeleteSession,
}) => {
  return (
    <div className="w-64 bg-gray-900 border-r border-gray-700 flex flex-col">
     
      <div className="p-4 border-b border-gray-700">
        <button
          onClick={onNewChat}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 font-medium flex items-center justify-center gap-2 transition-colors"
        >
          <Plus size={20} />
          New Chat
        </button>
      </div>

     
      <div className="flex-1 overflow-y-auto">
        {sessions.length === 0 ? (
          <div className="p-4 text-center text-gray-400 text-sm">
            No chat history yet
          </div>
        ) : (
          <div className="p-2 space-y-1">
            {sessions.map((session) => (
              <div
                key={session.id}
                className={`group relative flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-colors ${
                  currentSessionId === session.id
                    ? 'bg-gray-700 text-white'
                    : 'hover:bg-gray-800 text-gray-300'
                }`}
                onClick={() => onSelectSession(session.id)}
              >
                <MessageSquare size={18} className="flex-shrink-0" />
                
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">{session.title}</p>
                  <p className="text-xs text-gray-400 truncate">
                    {session.messages.length} messages
                  </p>
                </div>

                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDeleteSession(session.id);
                  }}
                  className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-600 rounded transition-all"
                  title="Delete chat"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

   
      <div className="p-4 border-t border-gray-700 text-xs text-gray-400">
        <p>Made with for Madlen</p>
        <p className="mt-1">OpenRouter Integration</p>
      </div>
    </div>
  );
};