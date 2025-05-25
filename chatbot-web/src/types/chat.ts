export interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
  timestamp?: string;
}

export interface ChatRequest {
  message: string;
  conversation_history?: ChatMessage[];
  model?: string;
  max_tokens?: number;
  temperature?: number;
  stream?: boolean;
}

export interface ChatResponse {
  message: string;
  role: string;
  model: string;
  conversation_id?: string;
}

export interface StreamChunk {
  content: string;
  is_complete: boolean;
  model: string;
}

export interface ModelsResponse {
  models: string[];
  default_model: string;
}

export interface ThinkingContent {
  thinking: string;
  response: string;
}
