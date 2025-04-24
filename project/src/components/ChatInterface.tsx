import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';
import ChatMessage from './ChatMessage';
import VideoPlayer from './VideoPlayer';
import { Message, sendMessage } from '../services/apiService';

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: "Hello! I'm HyperMath. Ask me to explain any mathematical concept, and I'll create a visual explanation to help you understand it better.",
      videoUrl: null,
      codeSnippet: null,
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      videoUrl: null,
      codeSnippet: null,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await sendMessage(input);
      setMessages((prev) => [...prev, response]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          role: 'assistant',
          content: 'Sorry, I encountered an error. Please try again later.',
          videoUrl: null,
          codeSnippet: null,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const latestVideoMessage = [...messages].reverse().find((msg) => msg.videoUrl);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 h-full">
      <div className="flex flex-col h-full overflow-hidden bg-white">
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          {isLoading && (
            <div className="flex items-center space-x-2 p-3 bg-slate-50 rounded-lg max-w-[80%] animate-pulse">
              <Loader2 className="h-5 w-5 text-blue-500 animate-spin" />
              <p className="text-slate-600">Processing your request...</p>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={handleSubmit} className="p-4 border-t border-slate-200">
          <div className="flex items-center space-x-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about any math concept..."
              className="flex-1 px-4 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={isLoading}
            />
            <button
              type="submit"
              className={`p-2 rounded-md ${
                isLoading || !input.trim()
                  ? 'bg-slate-200 text-slate-400 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              }`}
              disabled={isLoading || !input.trim()}
            >
              {isLoading ? <Loader2 className="h-5 w-5 animate-spin" /> : <Send className="h-5 w-5" />}
            </button>
          </div>
        </form>
      </div>

      <div className="hidden lg:block h-full bg-slate-100 border-l border-slate-200">
        {latestVideoMessage ? (
          <VideoPlayer videoUrl={latestVideoMessage.videoUrl} codeSnippet={latestVideoMessage.codeSnippet} />
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-center p-6">
            <div className="bg-white rounded-lg p-8 shadow-sm max-w-md">
              <h3 className="text-xl font-semibold text-slate-800 mb-3">No Visualization Yet</h3>
              <p className="text-slate-600">
                Ask me to explain any mathematical concept, and I'll create a visual explanation to help you understand it better.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatInterface;