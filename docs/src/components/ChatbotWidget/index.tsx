/**
 * ChatKit Widget Component
 * Modern chat interface using OpenAI ChatKit React.
 */

import React from 'react';
import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { getBackendURL } from '../../utils/env';

export default function ChatbotWidget() {
  console.log('ChatbotWidget rendering...');
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
    console.log('ChatbotWidget mounted');
  }, []);

  const { control } = useChatKit({
    api: {
      async getClientSecret(existing) {
        console.log('getClientSecret called, existing:', existing);

        if (existing) {
          // Token refresh - for now, create a new session
          console.log('Refreshing token...');
        }

        // Fetch client_secret from custom backend
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
        console.log('Session created successfully:', data);
        return data.client_secret;
      },
    },
    theme: 'dark',
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

  console.log('Rendering with control:', control, 'mounted:', mounted);

  return (
    <>
      {/* Debug indicator - always visible */}
      <div
        style={{
          position: 'fixed',
          bottom: '640px',
          right: '20px',
          padding: '10px',
          backgroundColor: '#25c2a0',
          color: 'white',
          borderRadius: '4px',
          zIndex: 9999,
          fontSize: '12px',
        }}
      >
        Widget Loaded ✓
      </div>

      {/* ChatKit container */}
      <div
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          width: '350px',
          height: '600px',
          zIndex: 9999,
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)',
          borderRadius: '8px',
          overflow: 'hidden',
          backgroundColor: 'white',
          border: '2px solid #25c2a0',
        }}
      >
        {control ? (
          <>
            <div style={{ padding: '10px', backgroundColor: '#f0f0f0', borderBottom: '1px solid #ccc' }}>
              <small>ChatKit Control Ready ✓</small>
            </div>
            <div style={{ height: 'calc(100% - 41px)' }}>
              <ChatKit control={control} style={{ width: '100%', height: '100%' }} />
            </div>
          </>
        ) : (
          <div style={{ padding: '20px', color: '#333' }}>
            <h3>Loading ChatKit...</h3>
            <p>Initializing chat interface</p>
          </div>
        )}
      </div>
    </>
  );
}
