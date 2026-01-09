import axios from 'axios';
import { AIModel, SendMessageRequest, SendMessageResponse, ChatSession } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

const transformMessage = (msg: any) => ({
  id: msg.id,
  role: msg.role,
  content: msg.content,
  timestamp: new Date(msg.timestamp),
  imageUrl: msg.image_url, 
});

const transformSession = (session: any): ChatSession => ({
  id: session.id,
  title: session.title,
  modelId: session.model_id, 
  messages: session.messages ? session.messages.map(transformMessage) : [],
  createdAt: new Date(session.created_at),
  updatedAt: new Date(session.updated_at),
});

export const apiService = {

  getModels: async (): Promise<AIModel[]> => {
    const response = await api.get<AIModel[]>('/models/');
    return response.data;
  },


  sendMessage: async (request: SendMessageRequest & { session_id?: string }): Promise<SendMessageResponse> => {
    const response = await api.post<SendMessageResponse>('/chat/', request);
    return response.data;
  },

 
  getSessions: async (): Promise<ChatSession[]> => {
    const response = await api.get<any[]>('/sessions/');
   
    return response.data.map(transformSession);
  },


  getSession: async (sessionId: string): Promise<ChatSession> => {
    const response = await api.get<any>(`/sessions/${sessionId}`);
   
    return transformSession(response.data);
  },

 
  createSession: async (modelId: string, title?: string): Promise<ChatSession> => {
    const response = await api.post<any>('/sessions/', {
      model_id: modelId,
      title: title || 'New Chat',
    });
 
    return transformSession(response.data);
  },


  deleteSession: async (sessionId: string): Promise<void> => {
    await api.delete(`/sessions/${sessionId}`);
  },

 
  updateSessionTitle: async (sessionId: string, title: string): Promise<ChatSession> => {
    const response = await api.patch<any>(`/sessions/${sessionId}`, { title });
 
    return transformSession(response.data);
  },
};

export default api;