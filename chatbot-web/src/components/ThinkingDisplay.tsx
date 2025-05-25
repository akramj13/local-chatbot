"use client";

import { useState } from "react";
import { ChevronDown, ChevronRight, Brain } from "lucide-react";

interface ThinkingDisplayProps {
  thinking: string;
  isStreaming?: boolean;
}

export default function ThinkingDisplay({
  thinking,
  isStreaming = false,
}: ThinkingDisplayProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!thinking.trim()) return null;

  return (
    <div className="mb-4 border border-blue-200 rounded-lg bg-blue-50 dark:bg-blue-950 dark:border-blue-800">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center gap-2 p-3 text-left hover:bg-blue-100 dark:hover:bg-blue-900 transition-colors rounded-lg"
      >
        <Brain className="w-4 h-4 text-blue-600 dark:text-blue-400" />
        <span className="text-sm font-medium text-blue-800 dark:text-blue-200">
          {isStreaming ? "Thinking..." : "Model Thinking"}
        </span>
        {isStreaming && (
          <div className="flex gap-1 ml-2">
            <div className="w-1 h-1 bg-blue-600 rounded-full animate-pulse"></div>
            <div
              className="w-1 h-1 bg-blue-600 rounded-full animate-pulse"
              style={{ animationDelay: "0.2s" }}
            ></div>
            <div
              className="w-1 h-1 bg-blue-600 rounded-full animate-pulse"
              style={{ animationDelay: "0.4s" }}
            ></div>
          </div>
        )}
        <div className="ml-auto">
          {isExpanded ? (
            <ChevronDown className="w-4 h-4 text-blue-600 dark:text-blue-400" />
          ) : (
            <ChevronRight className="w-4 h-4 text-blue-600 dark:text-blue-400" />
          )}
        </div>
      </button>

      {isExpanded && (
        <div className="px-3 pb-3">
          <div className="bg-white dark:bg-gray-900 rounded border p-3 text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap font-mono">
            {thinking}
          </div>
        </div>
      )}
    </div>
  );
}
