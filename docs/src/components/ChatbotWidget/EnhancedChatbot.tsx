/**
 * Enhanced ChatKit Widget Component
 * Uses vanilla @openai/chatkit web component loaded from CDN
 */

import React, { useState, useEffect, useRef } from 'react';
import { getBackendURL } from '../../utils/env';
import styles from './EnhancedChatbot.module.css';

// Declare the global chatkit element type
declare global {
  interface HTMLElementTagNameMap {
    'openai-chatkit': HTMLElement & {
      setOptions: (options: any) => void;
    };
  }
}

// Load ChatKit script from CDN
const loadChatKitScript = (): Promise<void> => {
  return new Promise((resolve, reject) => {
    // Check if already loaded
    if (document.querySelector('script[src*="chatkit.js"]')) {
      // Wait for custom element to be defined
      if (customElements.get('openai-chatkit')) {
        resolve();
        return;
      }
      // Wait for it to be defined
      customElements.whenDefined('openai-chatkit').then(() => resolve());
      return;
    }

    const script = document.createElement('script');
    script.src = 'https://cdn.platform.openai.com/deployments/chatkit/chatkit.js';
    script.async = true;

    script.onload = () => {
      // Wait for custom element to be registered
      customElements.whenDefined('openai-chatkit').then(() => resolve());
    };

    script.onerror = () => reject(new Error('Failed to load ChatKit script'));

    document.head.appendChild(script);
  });
};

export default function EnhancedChatbot() {
  const [mounted, setMounted] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [hasNewMessage, setHasNewMessage] = useState(false);
  const [isReady, setIsReady] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const chatkitRef = useRef<HTMLElement | null>(null);
  const initializingRef = useRef(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Initialize ChatKit when the chat opens
  useEffect(() => {
    if (!isOpen || !mounted || chatkitRef.current || initializingRef.current) return;

    const initChatKit = async () => {
      initializingRef.current = true;
      setIsLoading(true);
      setError(null);

      try {
        // Load the ChatKit script from CDN
        await loadChatKitScript();

        const container = chatContainerRef.current;
        if (!container) {
          initializingRef.current = false;
          return;
        }

        // Create the openai-chatkit element
        const chatkit = document.createElement('openai-chatkit');

        // Set explicit dimensions
        chatkit.style.width = '100%';
        chatkit.style.height = '100%';
        chatkit.style.display = 'block';
        chatkit.style.minHeight = '400px';

        // Configure options
        (chatkit as any).setOptions({
          api: {
            async getClientSecret(existing: string | null) {
              console.log('getClientSecret called, existing:', !!existing);

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
            enabled: false,
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
                icon: 'agent',
              },
              {
                label: 'Tell me about ROS 2',
                prompt: 'What is ROS 2 and why is it important for robotics?',
                icon: 'settings-slider',
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
        });

        // Add event listeners
        chatkit.addEventListener('chatkit.ready', () => {
          console.log('ChatKit is ready');
          setIsReady(true);
          setIsLoading(false);
          setError(null);
        });

        chatkit.addEventListener('chatkit.error', ((event: CustomEvent) => {
          console.error('ChatKit error:', event.detail?.error);
          setError(event.detail?.error?.message || 'An error occurred');
          setIsLoading(false);
        }) as EventListener);

        chatkit.addEventListener('chatkit.thread.change', ((event: CustomEvent) => {
          const threadId = event.detail?.threadId;
          console.log('Thread changed:', threadId);
          if (threadId) {
            sessionStorage.setItem('chatkit_thread_id', threadId);
          }
        }) as EventListener);

        // Append chatkit to container (don't clear - React manages children)
        container.appendChild(chatkit);
        chatkitRef.current = chatkit;

      } catch (err) {
        console.error('Failed to initialize ChatKit:', err);
        setError(err instanceof Error ? err.message : 'Failed to initialize chat');
        setIsLoading(false);
        initializingRef.current = false;
      }
    };

    initChatKit();

    // Cleanup function
    return () => {
      if (chatkitRef.current) {
        try {
          // Remove the chatkit element directly instead of clearing innerHTML
          chatkitRef.current.remove();
        } catch (e) {
          // Ignore cleanup errors
        }
      }
      chatkitRef.current = null;
      initializingRef.current = false;
      setIsReady(false);
    };
  }, [isOpen, mounted]);

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
    // Clean up chatkit instance
    if (chatkitRef.current) {
      try {
        chatkitRef.current.remove();
      } catch (e) {
        // Ignore cleanup errors
      }
      chatkitRef.current = null;
      initializingRef.current = false;
      setIsReady(false);
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    setError(null);
    setIsLoading(false);
    if (chatkitRef.current) {
      try {
        chatkitRef.current.remove();
      } catch (e) {
        // Ignore cleanup errors
      }
    }
    chatkitRef.current = null;
    initializingRef.current = false;
    setIsReady(false);
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
                  {isReady ? 'Online • Ready to help' : isLoading ? 'Connecting...' : 'Offline'}
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
              {error ? (
                <div className={styles.errorContainer}>
                  <div className={styles.errorIcon}>⚠️</div>
                  <p className={styles.errorText}>{error}</p>
                  <button
                    className={styles.retryButton}
                    onClick={handleRetry}
                  >
                    Retry
                  </button>
                </div>
              ) : (
                <div
                  ref={chatContainerRef}
                  className={styles.chatkitContainer}
                >
                  {(isLoading && !isReady) && (
                    <div className={styles.loadingContainer}>
                      <div className={styles.loadingSpinner}></div>
                      <p className={styles.loadingText}>Initializing AI Assistant...</p>
                      <p className={styles.loadingSubtext}>Setting up secure connection</p>
                    </div>
                  )}
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
