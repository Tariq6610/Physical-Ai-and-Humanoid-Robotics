---
sidebar_position: 2
title: Building and Embedding the Chatbot
---

## Introduction

With the RAG architecture in place, this chapter provides a step-by-step guide to building, training, and embedding the RAG chatbot into our Docusaurus-based digital book. We will cover the frontend implementation of the chatbot widget and the final integration steps to bring our interactive companion to life.

## Lesson 14.1: Implementing the Chatbot Frontend Widget

Our chatbot needs a user interface. Since our book is a Docusaurus site (which is built on React), we'll create a React component for our chatbot.

This component will be responsible for:
- Rendering a chat window.
- Handling user input.
- Sending user messages to our FastAPI backend.
- Displaying the conversation history.

Create a new file at `docs/src/components/ChatbotWidget.tsx`:

```tsx
import React, { useState, useEffect } from 'react';
import styles from './ChatbotWidget.module.css';

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
      const response = await fetch('/api/chat', { // Assuming the backend is on the same host
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userInput }),
      });
      const data = await response.json();
      setMessages([...newMessages, { sender: 'bot', text: data.answer }]);
    } catch (error) {
      console.error("Error fetching chatbot response:", error);
      setMessages([...newMessages, { sender: 'bot', text: "Sorry, I'm having trouble connecting." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      <button className={styles.chatToggleButton} onClick={toggleChat}>
        {isOpen ? 'Close' : 'Chat'}
      </button>
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>Robotics Assistant</div>
          <div className={styles.chatMessages}>
            {messages.map((msg, index) => (
              <div key={index} className={`${styles.message} ${styles[msg.sender]}`}>
                {msg.text}
              </div>
            ))}
            {isLoading && <div className={`${styles.message} ${styles.bot}`}>...</div>}
          </div>
          <div className={styles.chatInput}>
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Ask a question..."
            />
            <button onClick={handleSendMessage}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatbotWidget;
```

You'll also need to create a corresponding CSS module file at `docs/src/components/ChatbotWidget.module.css` to style the component.

## Lesson 14.2: Integrating the Chatbot with Docusaurus

To make our `ChatbotWidget` appear on every page of our site, we need to add it to a layout component that wraps all pages. Docusaurus provides a powerful feature called **"swizzling"** that allows us to override default theme components.

We will swizzle the `Root` component, which is the perfect place to add our widget.

1.  **Run the Swizzle Command**: From within the `docs` directory, run:
    ```bash
    npm run swizzle @docusaurus/theme-classic Root -- --danger
    ```
    This command ejects the `Root.tsx` component from the default theme into your `docs/src/theme` directory, allowing you to edit it.

2.  **Modify the Swizzled Component**: Open the newly created file `docs/src/theme/Root.tsx` and import and add the `ChatbotWidget`.

    ```tsx
    import React from 'react';
    import ChatbotWidget from '../components/ChatbotWidget'; // Import our widget

    // Default implementation:
    export default function Root({children}) {
      return (
        <>
          {children}
          <ChatbotWidget /> {/* Add our widget here */}
        </>
      );
    }
    ```

Now, when you run your Docusaurus site, the `ChatbotWidget` will be rendered on every page.

## Lesson 5.6: Training and Ingesting Book Content

Our RAG system is useless without the book's content in the Qdrant vector database. The `scripts/ingest.py` script is responsible for this "training" process.

The script will:
1.  Scan the `docs/docs` directory for all Markdown (`.md`) files.
2.  Load the content of each file.
3.  Split the content into smaller, semantically meaningful chunks.
4.  Use a sentence-transformer model to convert each chunk into a vector embedding.
5.  Upload the vector and the original text chunk to our Qdrant collection.

To run the ingestion script:

1.  **Set up Environment Variables**: Ensure your `.env` file in the `backend` directory has your `QDRANT_URL` and `QDRANT_API_KEY`.
2.  **Run the script**: From the root of the project, run:
    ```bash
    python scripts/ingest.py
    ```

You should run this script whenever the book's content is significantly updated to keep the chatbot's knowledge base current.

## Lesson 5.7: Testing and Deployment

To test our full end-to-end system locally, we need to run both the backend and the frontend simultaneously.

1.  **Start the Backend**: In a terminal, navigate to the `backend` directory and start the FastAPI server:
    ```bash
    uvicorn src.main:app --reload
    ```
    This will typically start the backend server on `http://127.0.0.1:8000`.

2.  **Start the Frontend**: In another terminal, navigate to the `docs` directory and start the Docusaurus development server:
    ```bash
    npm run start
    ```
    This will start the frontend on `http://localhost:3000`.

3.  **Testing**: Open your browser to `http://localhost:3000`. You should see your Docusaurus site with the chatbot widget. Open the widget and ask a question related to the content you've ingested. The frontend will send the request to the FastAPI backend, which will then execute the RAG pipeline and return an answer.

### Deployment

For a production deployment, you would:
-   Deploy the Docusaurus site as a static website (e.g., on Vercel, Netlify, or GitHub Pages).
-   Deploy the FastAPI backend as a persistent service (e.g., on a service like Render, Heroku, or a cloud provider).
-   Configure the frontend to point to the production backend URL.

## Summary

In this chapter, we brought our chatbot to life. We built the frontend React component, integrated it into our Docusaurus site using swizzling, and learned how to populate our vector database with the `ingest.py` script. Finally, we walked through the process of testing the full end-to-end system. Our book is now equipped with an interactive AI companion, ready to help readers on their learning journey.

## Key Takeaways

*   React components can be seamlessly integrated into Docusaurus sites.
*   Docusaurus swizzling is a powerful feature for customizing the site layout.
*   A content ingestion pipeline is crucial for keeping the RAG system's knowledge up-to-date.
*   Local testing requires running both the frontend and backend servers concurrently.