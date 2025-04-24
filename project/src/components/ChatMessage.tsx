import React from 'react';
import { User, Bot } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { Message } from '../services/apiService';

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div
      className={`flex items-start space-x-3 ${
        isUser ? 'justify-end' : 'justify-start'
      }`}
    >
      {!isUser && (
        <div className="flex-shrink-0 bg-blue-100 p-2 rounded-full">
          <Bot className="h-5 w-5 text-blue-700" />
        </div>
      )}
      
      <div
        className={`p-3 rounded-lg max-w-[80%] ${
          isUser
            ? 'bg-blue-600 text-white'
            : 'bg-slate-100 text-slate-800'
        }`}
      >
        <ReactMarkdown
          className={`prose ${
            isUser ? 'prose-invert' : ''
          } max-w-none text-sm`}
        >
          {message.content}
        </ReactMarkdown>
        
        {message.videoUrl && !isUser && (
          <div className="mt-2 lg:hidden">
            <video 
              src={message.videoUrl} 
              controls 
              className="w-full h-auto rounded-md"
            >
              Your browser does not support the video tag.
            </video>
          </div>
        )}
      </div>
      
      {isUser && (
        <div className="flex-shrink-0 bg-blue-600 p-2 rounded-full">
          <User className="h-5 w-5 text-white" />
        </div>
      )}
    </div>
  );
};

export default ChatMessage;