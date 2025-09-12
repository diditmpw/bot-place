import React, { useState } from 'react';
import { searchPlace } from '../../services/places.service';
import './ChatWindow.css';

interface Message {
  content: string;
  sender: 'user' | 'bot';
  location?: {
    lat: number;
    lng: number;
  };
}

interface ChatWindowProps {
  onLocationSelect: (lat: number, lng: number) => void;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ onLocationSelect }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (query: string) => {
    try {
      // Immediately show user message
      setMessages(prev => [...prev, { content: query, sender: 'user' }]);
      setIsLoading(true);

      const response = await searchPlace(query);
      
      // Add bot response
      if (response.type === 'place') {
        setMessages(prev => [...prev, {
          content: response.response,
          sender: 'bot',
          location: response.location
        }]);
        onLocationSelect(response.location.lat, response.location.lng);
      } else {
        setMessages(prev => [...prev, {
          content: response.response,
          sender: 'bot'
        }]);
      }
    } catch (error) {
      setMessages(prev => [...prev, 
        { content: 'Sorry, I encountered an error. Please try again.', sender: 'bot' }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-window">
      <div className="messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            {message.content}
          </div>
        ))}
        {isLoading && <div className="message bot">Thinking...</div>}
      </div>
      <div className="input-area">
        <input
          type="text"
          placeholder="Ask me anything..."
          onKeyPress={(e) => {
            if (e.key === 'Enter' && e.currentTarget.value.trim()) {
              handleSearch(e.currentTarget.value.trim());
              e.currentTarget.value = '';
            }
          }}
        />
      </div>
    </div>
  );
};

export default ChatWindow;