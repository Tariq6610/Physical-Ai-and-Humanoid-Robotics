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
          const ReadingProgress = require('../components/ReadingProgress').default;
          const ScrollToTop = require('../components/ScrollToTop').default;
          return (
            <>
              <ReadingProgress />
              <ScrollToTop />
              <ChatbotWidget />
            </>
          );
        }}
      </BrowserOnly>
    </>
  );
};

export default Root;