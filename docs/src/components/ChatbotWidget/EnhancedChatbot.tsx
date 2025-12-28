/**
 * Custom Chat Widget Component
 * A compact, modern chat widget that works with the Gemini-powered RAG backend.
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { getBackendURL } from '../../utils/env';
import styles from './EnhancedChatbot.module.css';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  isStreaming?: boolean;
}

interface ChatResponse {
  response: string;
  request_id: string;
  session_id: string;
}

const SUGGESTED_PROMPTS = [
  {
    icon: '💡',
    label: 'What is Physical AI?',
    prompt: 'What is Physical AI and how does it relate to robotics?',
  },
  {
    icon: '🤖',
    label: 'Humanoid robots',
    prompt: 'Can you explain what humanoid robots are and their key components?',
  },
  {
    icon: '⚙️',
    label: 'ROS 2 basics',
    prompt: 'What is ROS 2 and why is it important for robotics?',
  },
  {
    icon: '🎮',
    label: 'Isaac Sim',
    prompt: 'What is NVIDIA Isaac Sim and how is it used in robotics?',
  },
];

export default function EnhancedChatbot() {
  const [mounted, setMounted] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    setMounted(true);
    // Generate session ID on mount
    setSessionId(`session-${Date.now()}-${Math.random().toString(36).substring(2, 11)}`);
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen && !isMinimized) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen, isMinimized]);

  const generateMessageId = () => `msg-${Date.now()}-${Math.random().toString(36).substring(2, 11)}`;

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim() || isLoading) return;

    const userMessage: Message = {
      id: generateMessageId(),
      role: 'user',
      content: content.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    // Add placeholder for assistant response
    const assistantMessageId = generateMessageId();
    setMessages(prev => [
      ...prev,
      {
        id: assistantMessageId,
        role: 'assistant',
        content: '',
        timestamp: new Date(),
        isStreaming: true,
      },
    ]);

    try {
      const response = await fetch(`${getBackendURL()}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: content.trim(),
          session_id: sessionId,
        }),
      });

      if (!response.ok) {
        throw new Error(`Request failed: ${response.status} ${response.statusText}`);
      }

      const data: ChatResponse = await response.json();

      // Update assistant message with response
      setMessages(prev =>
        prev.map(msg =>
          msg.id === assistantMessageId
            ? { ...msg, content: data.response, isStreaming: false }
            : msg
        )
      );

      // Update session ID if returned
      if (data.session_id) {
        setSessionId(data.session_id);
      }
    } catch (err) {
      console.error('Chat error:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);

      // Remove the placeholder message on error
      setMessages(prev => prev.filter(msg => msg.id !== assistantMessageId));
    } finally {
      setIsLoading(false);
    }
  }, [isLoading, sessionId]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(inputValue);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(inputValue);
    }
  };

  const handlePromptClick = (prompt: string) => {
    sendMessage(prompt);
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (isMinimized) {
      setIsMinimized(false);
    }
  };

  const minimizeChat = () => {
    setIsMinimized(!isMinimized);
  };

  const closeChat = () => {
    setIsOpen(false);
    setIsMinimized(false);
  };

  const clearChat = () => {
    setMessages([]);
    setError(null);
    setSessionId(`session-${Date.now()}-${Math.random().toString(36).substring(2, 11)}`);
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  if (!mounted) return null;

  return (
    <>
      {/* Floating Action Button */}
      {!isOpen && (
        <button
          className={styles.fab}
          onClick={toggleChat}
          aria-label="Open AI Chat Assistant"
          title="Ask me anything about Physical AI & Robotics!"
        >
          <span className={styles.fabIcon}>🤖</span>
          <span className={styles.fabTooltip}>Ask AI Assistant</span>
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div
          className={`${styles.chatContainer} ${isMinimized ? styles.minimized : ''}`}
          role="dialog"
          aria-label="AI Chat Assistant"
        >
          {/* Chat Header */}
          <div className={styles.chatHeader}>
            <div className={styles.headerLeft}>
              <div className={styles.botAvatar}>
                <span className={styles.botIcon}>🤖</span>
                <span className={styles.statusDot}></span>
              </div>
              <div className={styles.headerInfo}>
                <h3 className={styles.headerTitle}>AI Assistant</h3>
                <p className={styles.headerSubtitle}>
                  {isLoading ? 'Thinking...' : 'Online • Ask about robotics'}
                </p>
              </div>
            </div>
            <div className={styles.headerActions}>
              <button
                className={styles.headerButton}
                onClick={clearChat}
                aria-label="Clear chat"
                title="Clear chat"
              >
                🗑
              </button>
              <button
                className={styles.headerButton}
                onClick={minimizeChat}
                aria-label={isMinimized ? 'Maximize' : 'Minimize'}
                title={isMinimized ? 'Maximize' : 'Minimize'}
              >
                {isMinimized ? '□' : '−'}
              </button>
              <button
                className={styles.headerButton}
                onClick={closeChat}
                aria-label="Close chat"
                title="Close chat"
              >
                ✕
              </button>
            </div>
          </div>

          {/* Chat Body */}
          {!isMinimized && (
            <div className={styles.chatBody}>
              <div className={styles.messagesContainer}>
                {/* Welcome Screen */}
                {messages.length === 0 && (
                  <div className={styles.welcomeScreen}>
                    <div className={styles.welcomeIcon}>🤖</div>
                    <h4 className={styles.welcomeTitle}>
                      Welcome! I'm your AI Assistant
                    </h4>
                    <p className={styles.welcomeText}>
                      Ask me anything about Physical AI and Humanoid Robotics. I can help with ROS 2, sensors, simulation, and more.
                    </p>
                    <div className={styles.suggestedPrompts}>
                      {SUGGESTED_PROMPTS.map((item, index) => (
                        <button
                          key={index}
                          className={styles.promptButton}
                          onClick={() => handlePromptClick(item.prompt)}
                          disabled={isLoading}
                        >
                          <span className={styles.promptIcon}>{item.icon}</span>
                          <span className={styles.promptLabel}>{item.label}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Messages */}
                {messages.map(message => (
                  <div
                    key={message.id}
                    className={`${styles.message} ${
                      message.role === 'user' ? styles.userMessage : styles.assistantMessage
                    }`}
                  >
                    {message.role === 'assistant' && (
                      <div className={styles.messageAvatar}>🤖</div>
                    )}
                    <div className={styles.messageContent}>
                      <div className={styles.messageBubble}>
                        {message.isStreaming ? (
                          <div className={styles.typingIndicator}>
                            <span></span>
                            <span></span>
                            <span></span>
                          </div>
                        ) : (
                          <p className={styles.messageText}>{message.content}</p>
                        )}
                      </div>
                      <span className={styles.messageTime}>
                        {formatTime(message.timestamp)}
                      </span>
                    </div>
                  </div>
                ))}

                {/* Error Message */}
                {error && (
                  <div className={styles.errorMessage}>
                    <span className={styles.errorIcon}>⚠️</span>
                    <span>{error}</span>
                    <button
                      className={styles.retryButtonSmall}
                      onClick={() => setError(null)}
                    >
                      Dismiss
                    </button>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>

              {/* Input Area */}
              <form className={styles.inputArea} onSubmit={handleSubmit}>
                <div className={styles.inputWrapper}>
                  <textarea
                    ref={inputRef}
                    className={styles.textInput}
                    value={inputValue}
                    onChange={e => setInputValue(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask about Physical AI, robotics, ROS 2..."
                    rows={1}
                    disabled={isLoading}
                  />
                  <button
                    type="submit"
                    className={styles.sendButton}
                    disabled={!inputValue.trim() || isLoading}
                    aria-label="Send message"
                  >
                    {isLoading ? (
                      <span className={styles.sendingSpinner}></span>
                    ) : (
                      <span className={styles.sendIcon}>➤</span>
                    )}
                  </button>
                </div>
                <p className={styles.inputHint}>
                  Press Enter to send • Shift+Enter for new line
                </p>
              </form>
            </div>
          )}

          {/* Minimized Footer */}
          {isMinimized && (
            <div className={styles.chatFooter} onClick={() => setIsMinimized(false)}>
              <p className={styles.footerText}>Click to expand chat</p>
            </div>
          )}
        </div>
      )}
    </>
  );
}
