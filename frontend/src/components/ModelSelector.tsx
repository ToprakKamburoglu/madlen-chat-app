import { AIModel } from '../types';
import { ChevronDown } from 'lucide-react';

interface ModelSelectorProps {
  models: AIModel[];
  selectedModel: string;
  onSelectModel: (modelId: string) => void;
  disabled?: boolean;
}

export const ModelSelector: React.FC<ModelSelectorProps> = ({
  models,
  selectedModel,
  onSelectModel,
  disabled = false,
}) => {
  
  const formatContextLength = (length?: number) => {
    if (!length) return '';
    if (length >= 1000000) return `${(length / 1000000).toFixed(1)}M`;
    if (length >= 1000) return `${(length / 1000).toFixed(0)}K`;
    return length.toString();
  };

  return (
    <div className="space-y-2">
      <div className="relative">
        <select
          value={selectedModel}
          onChange={(e) => onSelectModel(e.target.value)}
          disabled={disabled}
          className="w-full bg-gray-700 text-white rounded-lg px-4 py-2 pr-10 appearance-none focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 cursor-pointer"
        >
          {models.length === 0 ? (
            <option>Loading models...</option>
          ) : (
            models.map((model) => (
              <option key={model.id} value={model.id}>
                {model.name}
                {model.context_length && ` • ${formatContextLength(model.context_length)} tokens`}
              </option>
            ))
          )}
        </select>

        <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none">
          <ChevronDown size={20} className="text-gray-400" />
        </div>
      </div>
    </div>
  );
};