import { useState, useRef } from 'react';
import { Send, Image, X } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (content: string, imageFile?: File) => void;
  disabled?: boolean;
  supportsImages?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage,
  disabled = false,
  supportsImages = false,
}) => {
  const [message, setMessage] = useState('');
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() && !imageFile) return;

    onSendMessage(message, imageFile || undefined);
    setMessage('');
    setImageFile(null);
    setImagePreview(null);
  };

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImageFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const removeImage = () => {
    setImageFile(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="border-t border-gray-700 bg-gray-800 p-4">
      {imagePreview && (
        <div className="mb-2 relative inline-block">
          <img
            src={imagePreview}
            alt="Preview"
            className="max-h-32 rounded-lg border border-gray-600"
          />
          <button
            onClick={removeImage}
            className="absolute -top-2 -right-2 bg-red-600 rounded-full p-1 hover:bg-red-700"
          >
            <X size={16} />
          </button>
        </div>
      )}

      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message..."
          disabled={disabled}
          className="flex-1 bg-gray-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
        />

        {supportsImages && (
          <>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleImageSelect}
              className="hidden"
            />
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              disabled={disabled}
              className="bg-gray-700 hover:bg-gray-600 text-white rounded-lg px-4 py-3 transition-colors disabled:opacity-50"
              title="Upload image"
            >
              <Image size={20} />
            </button>
          </>
        )}

        <button
          type="submit"
          disabled={disabled || (!message.trim() && !imageFile)}
          className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-6 py-3 font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Send size={20} />
        </button>
      </form>
    </div>
  );
};