"use client";

import { ChatMessage as ChatMessageType } from "@/types/chat";
import { parseThinkingContent, hasThinkingTags } from "@/utils/thinking";
import ThinkingDisplay from "./ThinkingDisplay";
import { User, Bot } from "lucide-react";

interface ChatMessageProps {
  message: ChatMessageType;
  isStreaming?: boolean;
}

export default function ChatMessage({
  message,
  isStreaming = false,
}: ChatMessageProps) {
  const isUser = message.role === "user";
  const thinkingContent = hasThinkingTags(message.content)
    ? parseThinkingContent(message.content)
    : null;
  const displayContent = thinkingContent
    ? thinkingContent.response
    : message.content;

  return (
    <div
      className={`flex gap-3 ${isUser ? "flex-row-reverse" : "flex-row"} mb-6`}
    >
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser
            ? "bg-blue-500 text-white"
            : "bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-300"
        }`}
      >
        {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
      </div>

      <div
        className={`flex-1 max-w-[80%] ${isUser ? "text-right" : "text-left"}`}
      >
        <div
          className={`inline-block px-4 py-2 rounded-lg ${
            isUser
              ? "bg-blue-500 text-white"
              : "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100"
          }`}
        >
          {/* Show thinking content if present */}
          {thinkingContent && (
            <ThinkingDisplay
              thinking={thinkingContent.thinking}
              isStreaming={isStreaming && !thinkingContent.response}
            />
          )}

          {/* Show main content */}
          <div className="whitespace-pre-wrap">
            {displayContent}
            {isStreaming && !thinkingContent && (
              <span className="inline-block w-2 h-5 bg-current animate-pulse ml-1" />
            )}
          </div>
        </div>

        {message.timestamp && (
          <div
            className={`text-xs text-gray-500 dark:text-gray-400 mt-1 ${
              isUser ? "text-right" : "text-left"
            }`}
          >
            {new Date(message.timestamp).toLocaleTimeString()}
          </div>
        )}
      </div>
    </div>
  );
}
