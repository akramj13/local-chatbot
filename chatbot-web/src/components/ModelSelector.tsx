"use client";

import { useState, useEffect, useCallback } from "react";
import { ChevronDown, Bot, Zap } from "lucide-react";
import { ModelsResponse } from "@/types/chat";
import { fetchModels } from "@/utils/api";
import { isThinkingModel } from "@/utils/thinking";

interface ModelSelectorProps {
  selectedModel: string;
  onModelChange: (model: string) => void;
}

export default function ModelSelector({
  selectedModel,
  onModelChange,
}: ModelSelectorProps) {
  const [models, setModels] = useState<string[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadModels = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response: ModelsResponse = await fetchModels();
      setModels(response.models);

      // Set default model if none selected
      if (!selectedModel && response.default_model) {
        onModelChange(response.default_model);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load models");
    } finally {
      setLoading(false);
    }
  }, [selectedModel, onModelChange]);

  useEffect(() => {
    loadModels();
  }, [loadModels]);

  if (loading) {
    return (
      <div className="flex items-center gap-2 px-3 py-2 bg-gray-100 dark:bg-gray-800 rounded-lg">
        <Bot className="w-4 h-4 animate-spin" />
        <span className="text-sm text-gray-600 dark:text-gray-400">
          Loading models...
        </span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center gap-2 px-3 py-2 bg-red-100 dark:bg-red-900 rounded-lg">
        <Bot className="w-4 h-4 text-red-600 dark:text-red-400" />
        <span className="text-sm text-red-600 dark:text-red-400">
          Error: {error}
        </span>
      </div>
    );
  }

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors min-w-[200px]"
      >
        <Bot className="w-4 h-4 text-gray-600 dark:text-gray-400" />
        <div className="flex-1 text-left">
          <div className="text-sm font-medium text-gray-900 dark:text-gray-100">
            {selectedModel || "Select Model"}
          </div>
        </div>
        {isThinkingModel(selectedModel) && (
          <div title="Thinking Model">
            <Zap className="w-3 h-3 text-blue-500" />
          </div>
        )}
        <ChevronDown
          className={`w-4 h-4 text-gray-400 transition-transform ${
            isOpen ? "rotate-180" : ""
          }`}
        />
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg shadow-lg z-10 max-h-60 overflow-y-auto">
          {models.map((modelName) => (
            <button
              key={modelName}
              onClick={() => {
                onModelChange(modelName);
                setIsOpen(false);
              }}
              className={`w-full flex items-center gap-2 px-3 py-2 text-left hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors ${
                selectedModel === modelName ? "bg-blue-50 dark:bg-blue-900" : ""
              }`}
            >
              <Bot className="w-4 h-4 text-gray-600 dark:text-gray-400" />
              <div className="flex-1">
                <div className="text-sm font-medium text-gray-900 dark:text-gray-100">
                  {modelName}
                </div>
              </div>
              {isThinkingModel(modelName) && (
                <div title="Thinking Model">
                  <Zap className="w-3 h-3 text-blue-500" />
                </div>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
