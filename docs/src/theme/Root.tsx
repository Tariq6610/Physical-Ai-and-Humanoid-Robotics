import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

// Root component that wraps the entire application
const Root = ({ children }: { children: React.ReactNode }) => {
  return (
    <>
      {children}
      <BrowserOnly fallback={null}>
        {() => {
          const ChatbotWidget = require('../components/ChatbotWidget').default;
          return <ChatbotWidget />;
        }}
      </BrowserOnly>
    </>
  );
};

export default Root;