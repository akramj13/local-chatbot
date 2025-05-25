import { ThinkingContent } from "@/types/chat";

export function parseThinkingContent(content: string): ThinkingContent | null {
  // Look for <think> tags in the content
  const thinkingRegex = /<think>([\s\S]*?)<\/think>([\s\S]*)/;
  const match = content.match(thinkingRegex);

  if (match) {
    return {
      thinking: match[1].trim(),
      response: match[2].trim(),
    };
  }

  return null;
}

export function hasThinkingTags(content: string): boolean {
  return /<think>[\s\S]*?<\/think>/.test(content);
}

export function stripThinkingTags(content: string): string {
  return content.replace(/<think>[\s\S]*?<\/think>/g, "").trim();
}

export function extractThinkingOnly(content: string): string {
  const match = content.match(/<think>([\s\S]*?)<\/think>/);
  return match ? match[1].trim() : "";
}

export function isThinkingModel(modelName: string): boolean {
  // Common patterns for thinking models
  const thinkingPatterns = [
    /thinking/i,
    /reason/i,
    /think/i,
    /o1/i, // OpenAI o1 models
    /claude.*thinking/i,
  ];

  return thinkingPatterns.some((pattern) => pattern.test(modelName));
}
