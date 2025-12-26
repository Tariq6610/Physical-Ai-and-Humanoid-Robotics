import React, { useState } from 'react';
import { getBackendURL } from '../utils/env';

const ChatbotWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const toggleChat = () => setIsOpen(!isOpen);

  const handleSendMessage = async () => {
    if (!userInput.trim()) return;

    const newMessages = [...messages, { sender: 'user', text: userInput }];
    setMessages(newMessages);
    setUserInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${getBackendURL()}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userInput }),
      });
      const data = await response.json();
      setMessages([...newMessages, { sender: 'bot', text: data.response }]);
    } catch (error) {
      console.error("Error fetching chatbot response:", error);
      setMessages([...newMessages, { sender: 'bot', text: "Sorry, I'm having trouble connecting." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      zIndex: 9999,
    }}>
      <button
        onClick={toggleChat}
        style={{
          padding: '15px 25px',
          backgroundColor: '#25c2a0',
          color: 'white',
          border: 'none',
          borderRadius: '25px',
          cursor: 'pointer',
          fontSize: '16px',
          fontWeight: 'bold',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)',
        }}
      >
        {isOpen ? '✕ Close' : '💬 Chat'}
      </button>
      {isOpen && (
        <div style={{
          position: 'absolute',
          bottom: '60px',
          right: '0',
          width: '350px',
          height: '500px',
          backgroundColor: 'white',
          borderRadius: '10px',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
        }}>
          <div style={{
            padding: '15px',
            backgroundColor: '#25c2a0',
            color: 'white',
            fontWeight: 'bold',
            fontSize: '18px',
          }}>
            Robotics Assistant
          </div>
          <div style={{
            flex: 1,
            overflowY: 'auto',
            padding: '15px',
            display: 'flex',
            flexDirection: 'column',
            gap: '10px',
          }}>
            {messages.map((msg, index) => (
              <div
                key={index}
                style={{
                  padding: '10px 15px',
                  borderRadius: '10px',
                  maxWidth: '80%',
                  alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start',
                  backgroundColor: msg.sender === 'user' ? '#25c2a0' : '#f0f0f0',
                  color: msg.sender === 'user' ? 'white' : '#333',
                }}
              >
                {msg.text}
              </div>
            ))}
            {isLoading && (
              <div style={{
                padding: '10px 15px',
                borderRadius: '10px',
                maxWidth: '80%',
                alignSelf: 'flex-start',
                backgroundColor: '#f0f0f0',
                color: '#333',
              }}>
                Thinking...
              </div>
            )}
          </div>
          <div style={{
            padding: '15px',
            borderTop: '1px solid #eee',
            display: 'flex',
            gap: '10px',
          }}>
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Ask about robotics..."
              style={{
                flex: 1,
                padding: '10px',
                border: '1px solid #ddd',
                borderRadius: '5px',
                fontSize: '14px',
              }}
            />
            <button
              onClick={handleSendMessage}
              disabled={isLoading}
              style={{
                padding: '10px 20px',
                backgroundColor: '#25c2a0',
                color: 'white',
                border: 'none',
                borderRadius: '5px',
                cursor: isLoading ? 'not-allowed' : 'pointer',
                fontWeight: 'bold',
                opacity: isLoading ? 0.6 : 1,
              }}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatbotWidget;
