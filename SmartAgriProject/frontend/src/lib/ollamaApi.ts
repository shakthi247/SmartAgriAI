import type { AIModel } from '../types/enums';

const OLLAMA_API_URL = 'http://127.0.0.1:11434/api';

export interface OllamaMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface OllamaRequest {
  model: string;
  messages: OllamaMessage[];
  stream?: boolean;
  options?: {
    temperature?: number;
  };
}

export interface OllamaResponse {
  model: string;
  created_at: string;
  message: {
    role: string;
    content: string;
  };
  done: boolean;
}

export async function chatWithOllama(
  model: AIModel,
  messages: OllamaMessage[],
  temperature: number = 0.7
): Promise<string> {
  try {
    // Add system message for agricultural context
    const systemMessage: OllamaMessage = {
      role: 'system',
      content: 'You are an expert agricultural AI assistant. Provide helpful, accurate advice about farming, crop management, pest control, fertilizers, irrigation, and other agricultural topics. Keep responses concise and practical for farmers.'
    };

    const requestBody: OllamaRequest = {
      model,
      messages: [systemMessage, ...messages],
      stream: false,
      options: {
        temperature
      }
    };

    const response = await fetch(`${OLLAMA_API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      throw new Error(`Ollama API error: ${response.statusText}`);
    }

    const data: OllamaResponse = await response.json();
    return data.message.content;
  } catch (error) {
    console.error('Error calling Ollama API:', error);
    throw new Error(`Failed to get response from Ollama: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

export async function checkOllamaConnection(): Promise<boolean> {
  try {
    const response = await fetch(`${OLLAMA_API_URL}/tags`);
    return response.ok;
  } catch {
    return false;
  }
}

export async function getAvailableModels(): Promise<string[]> {
  try {
    const response = await fetch(`${OLLAMA_API_URL}/tags`);
    if (!response.ok) {
      throw new Error('Failed to fetch models');
    }
    const data = await response.json();
    return data.models?.map((m: any) => m.name) || [];
  } catch (error) {
    console.error('Error fetching models:', error);
    return [];
  }
}