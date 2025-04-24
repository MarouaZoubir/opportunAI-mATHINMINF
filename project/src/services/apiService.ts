import axios from 'axios';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  videoUrl: string | null;
  codeSnippet: string | null;
}

const API_URL = 'http://localhost:5000';

export const sendMessage = async (content: string): Promise<Message> => {
  try {
    const response = await axios.post(`${API_URL}/api/chat`, { prompt: content });
    return {
      id: Date.now().toString(),
      role: 'assistant',
      content: response.data.explanation,
      videoUrl: response.data.video_url,
      codeSnippet: response.data.manim_code,
    };
  } catch (error) {
    console.error('API error:', error);
    throw error;
  }
};