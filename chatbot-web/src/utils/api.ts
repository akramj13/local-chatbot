import { ChatRequest, ModelsResponse, StreamChunk } from "@/types/chat";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

export async function fetchModels(): Promise<ModelsResponse> {
  const response = await fetch(`${API_BASE_URL}/models`);

  if (!response.ok) {
    throw new ApiError(
      response.status,
      `Failed to fetch models: ${response.statusText}`
    );
  }

  return response.json();
}

export async function* streamChat(
  request: ChatRequest
): AsyncGenerator<StreamChunk, void, unknown> {
  const response = await fetch(`${API_BASE_URL}/chat/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new ApiError(
      response.status,
      `Failed to start chat stream: ${response.statusText}`
    );
  }

  const reader = response.body?.getReader();
  if (!reader) {
    throw new Error("No response body reader available");
  }

  const decoder = new TextDecoder();
  let buffer = "";

  try {
    while (true) {
      const { done, value } = await reader.read();

      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      // Process complete lines
      const lines = buffer.split("\n");
      buffer = lines.pop() || ""; // Keep incomplete line in buffer

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const data = line.slice(6).trim();

          if (data === "[DONE]") {
            return;
          }

          try {
            const chunk: StreamChunk = JSON.parse(data);
            yield chunk;

            if (chunk.is_complete) {
              return;
            }
          } catch (error) {
            console.warn("Failed to parse chunk:", data, error);
          }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}

export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
}
