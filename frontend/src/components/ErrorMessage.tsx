import { AlertCircle, X } from 'lucide-react';

interface ErrorMessageProps {
  message: string;
  onClose?: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({
  message,
  onClose,
}) => {
  return (
    <div className="bg-red-900 border border-red-700 text-red-100 rounded-lg p-4 flex items-start gap-3 fade-in">
      <AlertCircle size={20} className="flex-shrink-0 mt-0.5" />
      
      <div className="flex-1">
        <p className="text-sm font-medium">Error</p>
        <p className="text-sm mt-1">{message}</p>
      </div>

      {onClose && (
        <button
          onClick={onClose}
          className="flex-shrink-0 hover:bg-red-800 rounded p-1 transition-colors"
        >
          <X size={18} />
        </button>
      )}
    </div>
  );
};