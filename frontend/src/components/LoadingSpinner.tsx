import { Loader2 } from 'lucide-react';

interface LoadingSpinnerProps {
  message?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  message = 'Loading...',
}) => {
  return (
    <div className="flex flex-col items-center justify-center gap-3 p-8">
      <Loader2 size={32} className="animate-spin text-blue-500" />
      <p className="text-gray-400 text-sm">{message}</p>
    </div>
  );
};