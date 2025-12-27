/**
 * Enhanced ChatKit Widget Component
 * Beautiful, modern chat interface with animations and better UX
 */

import React, { useState, useEffect } from 'react';
import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { getBackendURL } from '../../utils/env';
import styles from './EnhancedChatbot.module.css';

export default function EnhancedChatbot() {
  const [mounted, setMounted] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [hasNewMessage, setHasNewMessage] = useState(false);

  useEffect(() => {
    setMounted(true);
    console.log('EnhancedChatbot mounted');
  }, []);

  const { control } = useChatKit({
    api: {
      async getClientSecret(existing) {
        console.log('getClientSecret called');

        const sessionUrl = `${getBackendURL()}/api/chatkit/session`;
        console.log('Fetching session from:', sessionUrl);

        const res = await fetch(sessionUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
        });

        if (!res.ok) {
          const errorMsg = `Failed to create ChatKit session: ${res.status} ${res.statusText}`;
          console.error(errorMsg);
          throw new Error(errorMsg);
        }

        const data = await res.json();
        console.log('Session created successfully');
        return data.client_secret;
      },
    },
    theme: {
      colorScheme: 'dark',
      radius: 'round',
      color: {
        accent: { primary: '#4d90e1', level: 2 },
      },
    },
    header: {
      enabled: true,
      title: 'AI Assistant',
      subtitle: 'Physical AI & Robotics Expert',
    },
    history: {
      enabled: true,
      showDelete: true,
      showRename: false,
    },
    startScreen: {
      greeting: 'Welcome! Ask me anything about Physical AI and Humanoid Robotics.',
      prompts: [
        {
          label: 'What is Physical AI?',
          prompt: 'What is Physical AI and how does it relate to robotics?',
          icon: 'lightbulb',
        },
        {
          label: 'Explain humanoid robots',
          prompt: 'Can you explain what humanoid robots are and their key components?',
          icon: 'robot',
        },
        {
          label: 'Tell me about ROS 2',
          prompt: 'What is ROS 2 and why is it important for robotics?',
          icon: 'settings',
        },
        {
          label: 'NVIDIA Isaac Sim',
          prompt: 'What is NVIDIA Isaac Sim and how is it used in robotics?',
          icon: 'desktop',
        },
      ],
    },
    composer: {
      placeholder: 'Ask about Physical AI, robotics, ROS 2, sensors...',
    },
    threadItemActions: {
      feedback: true,
      retry: true,
    },
    locale: 'en',
    onError: ({ error }) => {
      console.error('ChatKit error:', error);
    },
    onReady: () => {
      console.log('ChatKit is ready');
    },
    onThreadChange: ({ threadId }) => {
      console.log('Thread changed:', threadId);
      if (threadId) {
        sessionStorage.setItem('chatkit_thread_id', threadId);
      }
    },
  });

  const toggleChat = () => {
    setIsOpen(!isOpen);
    setHasNewMessage(false);
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

  if (!mounted) return null;

  return (
    <>
      {/* Floating Action Button */}
      {!isOpen && (
        <button
          className={`${styles.fab} ${hasNewMessage ? styles.fabPulse : ''}`}
          onClick={toggleChat}
          aria-label="Open AI Chat Assistant"
          title="Ask me anything about Physical AI & Robotics!"
        >
          <span className={styles.fabIcon}>🤖</span>
          {hasNewMessage && <span className={styles.fabBadge}>!</span>}
          <span className={styles.fabTooltip}>
            Ask AI Assistant
          </span>
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
                  {control ? 'Online • Ready to help' : 'Connecting...'}
                </p>
              </div>
            </div>
            <div className={styles.headerActions}>
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
              {control ? (
                <div className={styles.chatkitWrapper}>
                  <ChatKit
                    control={control}
                    className={styles.chatkit}
                  />
                </div>
              ) : (
                <div className={styles.loadingContainer}>
                  <div className={styles.loadingSpinner}></div>
                  <p className={styles.loadingText}>Initializing AI Assistant...</p>
                  <p className={styles.loadingSubtext}>Setting up secure connection</p>
                </div>
              )}
            </div>
          )}

          {/* Chat Footer - Only show when minimized */}
          {isMinimized && (
            <div className={styles.chatFooter}>
              <p className={styles.footerText}>Click to expand chat</p>
            </div>
          )}
        </div>
      )}
    </>
  );
}
