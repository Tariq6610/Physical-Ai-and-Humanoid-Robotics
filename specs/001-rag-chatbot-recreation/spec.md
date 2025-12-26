# Feature Specification: RAG Chatbot Recreation with Modern Frameworks

**Feature Branch**: `001-rag-chatbot-recreation`
**Created**: 2025-12-26
**Status**: Draft
**Input**: User description: "Recreate RAG chatbot implementation with new frameworks while maintaining existing frontend-backend API connection logic"

---

## 🚨 CRITICAL: Mandatory Context7 MCP Usage

**FOR ALL AGENTS (Planning, Tasks, Implementation)**:

You MUST use Context7 MCP server to retrieve framework documentation before making any design or implementation decisions. Do NOT rely on internal knowledge about these frameworks.

**Required Context7 Queries**:
1. **OpenAI Agents SDK Python**: `/openai/openai-agents-python`
   - Topics: agent patterns, session management, function tools, LiteLLM integration, Gemini configuration
2. **OpenAI ChatKit React**: `/openai/chatkit-js`
   - Topics: widget integration, theming, custom backend connection, event handling, responsive design

**When to Query Context7**:
- Before planning architecture decisions involving these frameworks
- Before generating implementation tasks
- Before writing any code that uses OpenAI Agents SDK or ChatKit
- When troubleshooting integration issues
- When determining best practices or patterns

**Failure to use Context7** may result in outdated patterns, incorrect API usage, or missing features that these frameworks provide natively.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Basic Question-Answer Flow (Priority: P1)

A documentation site visitor asks a question about Physical AI and Humanoid Robotics topics through the chatbot widget and receives accurate, context-aware responses sourced from the project documentation.

**Why this priority**: Core functionality that delivers immediate value. Without this, the chatbot is non-functional. This is the foundation that all other features build upon.

**Independent Test**: Can be fully tested by opening the chatbot widget, typing "What is Physical AI?", and verifying a relevant answer is displayed within 3 seconds with source citations.

**Acceptance Scenarios**:

1. **Given** the chatbot widget is visible on the documentation page, **When** a visitor clicks the chat icon and types a question about robotics fundamentals, **Then** the system retrieves relevant document chunks and generates a comprehensive answer with source references
2. **Given** a user submits a query, **When** the RAG pipeline processes the question, **Then** the system embeds the query, searches the vector database, retrieves top 5 relevant chunks, and passes them to the LLM for response generation
3. **Given** the LLM generates a response, **When** the answer is returned to the frontend, **Then** the response appears in the chat interface with proper formatting and source citations within 3 seconds

---

### User Story 2 - Multi-Turn Conversation Context (Priority: P2)

A user engages in a multi-turn conversation where each new question builds upon previous exchanges, maintaining context throughout the session.

**Why this priority**: Enhances user experience by enabling natural conversations rather than isolated Q&A pairs. Critical for complex technical topics that require follow-up questions.

**Independent Test**: Can be tested by asking "What is a humanoid robot?" followed by "How does it differ from industrial robots?" and verifying the second answer references the first question's context.

**Acceptance Scenarios**:

1. **Given** a user has asked a question and received an answer, **When** they ask a follow-up question using pronouns or implicit references, **Then** the system maintains conversation history and resolves references correctly
2. **Given** a conversation has 5+ exchanges, **When** the context window approaches the limit, **Then** the system intelligently summarizes or truncates older messages while preserving key information
3. **Given** a user starts a new topic, **When** they explicitly signal a context switch, **Then** the system recognizes the shift and doesn't incorrectly blend contexts

---

### User Story 3 - Graceful Error Handling and Fallback (Priority: P1)

When the RAG system encounters errors (API failures, missing documents, network issues), users receive clear, helpful error messages and the system degrades gracefully.

**Why this priority**: Essential for production reliability. Users should never see cryptic errors or hung requests. This builds trust in the system.

**Independent Test**: Can be tested by disconnecting the vector database or simulating an LLM API timeout, then verifying users see meaningful error messages like "Unable to connect to knowledge base. Please try again in a moment."

**Acceptance Scenarios**:

1. **Given** the vector database is unavailable, **When** a user submits a query, **Then** the system displays "Knowledge base temporarily unavailable" and suggests alternative resources
2. **Given** the LLM API times out, **When** the retry mechanism exhausts attempts, **Then** the user sees "Response generation is taking longer than expected. Please try rephrasing your question."
3. **Given** no relevant documents are found for a query, **When** the retrieval score is below the threshold, **Then** the system responds with "I don't have specific information about that topic in the current documentation" rather than hallucinating

---

### User Story 4 - Off-Topic Query Detection (Priority: P2)

Users who ask questions unrelated to Physical AI and Humanoid Robotics receive polite redirection to stay within the chatbot's domain expertise.

**Why this priority**: Prevents misinformation and sets appropriate expectations about the chatbot's capabilities. Important for maintaining credibility but not blocking core functionality.

**Independent Test**: Can be tested by asking "What's the weather today?" and verifying the response states "I'm specialized in Physical AI and Humanoid Robotics topics. I can help with questions about [examples]."

**Acceptance Scenarios**:

1. **Given** a user asks about an unrelated topic, **When** the classifier detects off-topic intent, **Then** the system provides a friendly redirection message with example valid topics
2. **Given** a borderline query that might be tangentially related, **When** the classifier is uncertain, **Then** the system attempts to answer while noting the tangential connection
3. **Given** a user repeatedly asks off-topic questions, **When** the pattern is detected, **Then** the system provides a more detailed explanation of its scope without frustrating the user

---

### User Story 5 - Modern ChatKit UI with Rich Features (Priority: P1)

Users interact with a professional, modern chat interface powered by OpenAI ChatKit that automatically renders markdown, highlights code syntax, displays typing indicators, works responsively on all devices, and provides a polished experience comparable to ChatGPT.

**Why this priority**: The current custom widget is basic (70 lines of React) and lacks modern chat features users expect from AI assistants. ChatKit's prebuilt widget eliminates the need to build these features from scratch and provides a professional, tested UI out of the box. This is critical because even a working RAG backend with poor UI won't drive user adoption.

**Independent Test**: Can be tested by opening the chatbot widget on both desktop (1920x1080) and mobile (375x667), sending messages with markdown formatting and code snippets, and verifying proper rendering, smooth animations, typing indicators, and responsive layout without custom CSS.

**Acceptance Scenarios**:

1. **Given** a user sends a message containing markdown (bold, italic, lists, links) or code blocks, **When** the bot responds with formatted content, **Then** ChatKit automatically renders markdown with proper styling and displays code with syntax highlighting (no custom parsing required)
2. **Given** a user opens the chatbot on a mobile device, **When** they interact with the interface, **Then** ChatKit's responsive design adapts the layout, button sizes, and spacing for touch interaction without custom media queries
3. **Given** a user submits a question, **When** the backend is generating a response, **Then** ChatKit displays an animated typing indicator and streams tokens as they arrive for real-time feedback
4. **Given** a conversation with multiple messages, **When** scrolling through history, **Then** messages display with user/bot avatars, formatted timestamps, proper spacing, and the UI maintains smooth scrolling performance
5. **Given** a useful bot response with code, **When** the user hovers over the message, **Then** ChatKit provides built-in actions (copy message, copy code block) via intuitive hover menus

---

### User Story 6 - Production Deployment Compatibility (Priority: P1)

The chatbot works correctly when deployed to production environments with separate frontend and backend URLs, not just on localhost development setups.

**Why this priority**: Critical blocker fix. The current system only works on localhost due to hardcoded URLs. Without this, the feature cannot be deployed.

**Independent Test**: Can be tested by deploying frontend to `https://example.onrender.com` and backend to `https://api.example.onrender.com`, then verifying the chatbot successfully communicates across domains.

**Acceptance Scenarios**:

1. **Given** the frontend is deployed on a Render static site, **When** the application loads, **Then** it correctly determines the backend API URL from environment configuration
2. **Given** the backend is deployed on a separate Render web service, **When** CORS requests arrive from the frontend domain, **Then** the requests are properly authenticated and processed
3. **Given** different deployment environments (dev, staging, prod), **When** the application initializes, **Then** it automatically connects to the correct backend URL for that environment without code changes

---

### Edge Cases

- **What happens when a user submits an extremely long question (>2000 characters)?** System truncates gracefully and notifies the user of character limits
- **How does the system handle concurrent requests from the same user?** Implements request queuing or debouncing to prevent duplicate processing
- **What happens when the vector database returns zero results?** Falls back to a general LLM response or provides helpful suggestions for rephrasing
- **How does the system handle special characters, code snippets, or markdown in queries?** Properly sanitizes input while preserving user intent and renders formatted responses
- **What happens when API keys expire or are invalid?** Detects authentication failures at startup and provides clear configuration error messages
- **How does the system behave when network latency exceeds 10 seconds?** Shows loading indicators and allows user to cancel in-flight requests
- **What happens when the chatbot widget is opened on a slow mobile connection?** Optimizes payload size and shows progressive loading states

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept natural language questions through a chat interface widget embedded in the documentation site
- **FR-002**: System MUST convert user queries into vector embeddings compatible with the vector database format
- **FR-003**: System MUST retrieve the top 5 most relevant document chunks from the vector database based on semantic similarity
- **FR-004**: System MUST combine retrieved context with the user's question to generate accurate, coherent responses
- **FR-005**: System MUST maintain conversation history for multi-turn dialogues within a single session
- **FR-006**: System MUST detect off-topic queries and politely redirect users to in-scope topics
- **FR-007**: System MUST sanitize user input to prevent XSS, injection attacks, and other security vulnerabilities
- **FR-008**: System MUST implement rate limiting to prevent abuse (minimum 100 requests per hour per user)
- **FR-009**: System MUST return responses within 3 seconds for 95% of queries under normal conditions
- **FR-010**: System MUST provide source citations or references for information retrieved from documentation
- **FR-011**: System MUST handle errors gracefully with user-friendly messages (no stack traces or technical jargon exposed)
- **FR-012**: System MUST support environment-specific configuration for backend API URLs (development, staging, production)
- **FR-013**: System MUST implement retry logic with exponential backoff for transient failures (network timeouts, temporary API unavailability)
- **FR-014**: System MUST persist conversation history in browser session storage to survive page refreshes
- **FR-015**: System MUST allow users to clear conversation history manually via a "New Conversation" button
- **FR-016**: System MUST log all queries and responses for analytics and quality improvement (with PII redaction)
- **FR-017**: Frontend MUST dynamically determine backend URL from environment variables or deployment context
- **FR-018**: Backend MUST validate request payloads against expected schema (reject malformed requests)
- **FR-019**: System MUST support embedding model upgrades without requiring vector database re-indexing if backward compatible
- **FR-020**: System MUST provide a health check endpoint for monitoring service availability
- **FR-021**: Frontend MUST use OpenAI ChatKit's prebuilt widget component for the chat interface (replacing custom ChatbotWidget)
- **FR-022**: ChatKit widget MUST automatically render markdown formatting (bold, italic, lists, links) in bot responses
- **FR-023**: ChatKit widget MUST display code blocks with syntax highlighting for common programming languages
- **FR-024**: ChatKit widget MUST adapt responsively to mobile and desktop screen sizes without custom CSS media queries
- **FR-025**: ChatKit widget MUST display typing indicators and stream response tokens in real-time as they arrive from the backend
- **FR-026**: ChatKit widget MUST provide built-in message actions (copy, share) accessible via hover or long-press on mobile
- **FR-027**: ChatKit theme MUST be customized to match the Docusaurus color scheme (accent color, typography, dark/light mode)
- **FR-028**: Frontend MUST connect ChatKit to the custom FastAPI backend via the `getClientSecret()` callback instead of OpenAI's hosted service

### Key Entities

- **ChatMessage**: Represents a single message in the conversation, containing the message text, timestamp, sender (user or assistant), and optional source references. Messages are ordered chronologically within a conversation session.

- **ConversationSession**: Represents a complete chat interaction, containing a unique session ID, list of ChatMessages, creation timestamp, and last activity timestamp. Sessions are scoped to browser storage and expire after 24 hours of inactivity.

- **DocumentChunk**: Represents a segment of documentation content, containing the text content, metadata (document title, section, URL), embedding vector, and relevance score. Used for retrieval and citation purposes.

- **RAGContext**: Represents the combined information passed to the LLM, containing the user's query, retrieved DocumentChunks, conversation history (last 5 exchanges), and system instructions. This is the assembled context that influences response generation.

- **ErrorResponse**: Represents a structured error message, containing error type (network, timeout, validation, server), user-facing message, technical details (for logging), and suggested actions. Used for consistent error handling across the system.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users receive relevant answers to domain-specific questions within 3 seconds for 95% of queries
- **SC-002**: System successfully handles at least 100 concurrent users without response time degradation beyond 5 seconds
- **SC-003**: 90% of users complete at least 3 exchanges in a conversation session (indicates engagement and satisfaction)
- **SC-004**: Error rate remains below 5% across all queries (excluding user-caused errors like off-topic questions)
- **SC-005**: Source citation accuracy reaches 85% (responses include correct references to documentation sources)
- **SC-006**: Off-topic query detection achieves 80% precision (correctly identifies unrelated questions without false positives)
- **SC-007**: System maintains 99.5% uptime during business hours (excluding scheduled maintenance)
- **SC-008**: Zero security vulnerabilities related to input sanitization in production environment
- **SC-009**: Production deployment works correctly across separate frontend/backend domains without CORS errors
- **SC-010**: User abandonment rate (closing chatbot before receiving response) stays below 10%
- **SC-011**: Average conversation length increases by 50% compared to single-turn Q&A baseline (indicates improved context handling)
- **SC-012**: Response relevance score (human evaluation on sample of 100 queries) exceeds 85% "helpful" rating

## Assumptions *(if applicable)*

1. **Vector Database Pre-population**: Assume the vector database (Qdrant) is already populated with embedded documentation chunks. This feature focuses on the RAG pipeline, not the document ingestion process.

2. **LLM API Availability**: Assume access to Google Gemini's free tier API with appropriate API key configured. The recreation focuses on improving the framework integration using OpenAI Agents SDK with LiteLLM for Gemini access, not building custom LLM hosting.

3. **Modern Browser Support**: Assume users access the documentation site using modern browsers (Chrome, Firefox, Safari, Edge) with JavaScript enabled. No support for IE11 or legacy environments.

4. **Single-Language Documentation**: Assume all documentation is in English. Multi-language support and translation are out of scope for this recreation.

5. **Docusaurus Integration**: Assume the frontend continues using Docusaurus as the documentation framework. The chat widget must integrate seamlessly without breaking existing documentation features.

6. **Session-Based Conversations**: Assume conversation history is session-scoped (browser storage) rather than user-account-scoped. No user authentication required for basic chatbot functionality.

7. **Rate Limiting Per IP**: Assume rate limiting is enforced per IP address rather than per authenticated user, given the anonymous nature of documentation site visitors.

8. **Deployment on Render**: Assume the application deploys to Render platform for both frontend (static site) and backend (web service), requiring environment-specific configuration.

9. **Context7 MCP Availability**: Assume Context7 MCP server is available and operational during planning, task generation, and implementation phases. All agents must have access to query `/openai/openai-agents-python` and `/openai/chatkit-js` library IDs for framework documentation.

## Constraints *(if applicable)*

1. **API Compatibility Preservation**: Must maintain existing API endpoint structure (`POST /chat`, `GET /health`) to avoid breaking any external integrations or monitoring tools that may already depend on these routes.

2. **Frontend Component Interface**: Will replace custom ChatbotWidget with ChatKit's prebuilt widget component. The integration point in `Root.tsx` remains the same, but internal implementation switches to ChatKit's `<ChatKit control={control} />` component.

3. **Environment Variable Schema**: Must maintain key environment variables (`QDRANT_URL`, `QDRANT_API_KEY`, `GEMINI_API_KEY`) while potentially renaming LLM-related variables to reflect the new OpenAI Agents SDK + LiteLLM architecture.

4. **Testing Infrastructure**: Must maintain compatibility with existing test suites (pytest for backend, Jest for frontend) to preserve test coverage and avoid rewriting hundreds of test cases.

5. **Budget Constraints**: LLM API costs must remain at zero using Google Gemini's free tier (15 requests/minute limit). This constrains request volume and requires rate limiting to stay within free tier quotas.

6. **Response Time SLA**: 95th percentile response time cannot exceed 3 seconds to maintain acceptable user experience, limiting complex multi-step RAG pipelines.

7. **Vector Database Limitations**: Qdrant cloud free tier limits to 1GB storage and 1M vectors, constraining the volume of documentation that can be indexed.

8. **CORS and Security**: Must maintain secure CORS configuration without allowing unrestricted access, while supporting cross-origin requests from legitimate frontend deployments.

9. **Backwards Compatibility**: Existing conversation logs and analytics pipelines must continue functioning without modification during and after the recreation.

10. **No Breaking Changes to Docusaurus**: Cannot modify core Docusaurus configuration files in ways that would prevent future Docusaurus version upgrades.

11. **Mandatory Context7 MCP Usage for Framework Context**: All agents working on planning, tasks generation, and implementation phases MUST use Context7 MCP server to retrieve up-to-date documentation and code examples for OpenAI Agents SDK and ChatKit. Agents are NOT permitted to rely solely on internal knowledge or make assumptions about these frameworks without first querying Context7 for:
    - OpenAI Agents SDK Python (`/openai/openai-agents-python`): Agent patterns, session management, function tools, LiteLLM integration
    - OpenAI ChatKit React (`/openai/chatkit-js`): Widget integration, theming, backend connection, event handling

    This ensures agents have accurate, current framework information and prevents outdated or incorrect implementation approaches.

## Out of Scope *(if applicable)*

1. **Document Ingestion Pipeline**: Rebuilding the system that chunks, embeds, and indexes documentation into the vector database. Assume this infrastructure already exists and functions correctly.

2. **User Authentication and Authorization**: Implementing user accounts, login systems, or personalized chat history across sessions. The chatbot remains anonymous and session-based.

3. **Multi-Language Support**: Translating documentation, handling non-English queries, or providing responses in multiple languages. English-only for this iteration.

4. **Voice Input/Output**: Adding speech-to-text or text-to-speech capabilities for hands-free interaction. Text-based chat only.

5. **Admin Dashboard**: Creating interfaces for monitoring chat analytics, reviewing conversations, or managing chatbot configuration. These remain command-line or config-file-based.

6. **Custom LLM Fine-Tuning**: Training or fine-tuning custom language models on domain-specific data. Use existing general-purpose LLMs via API.

7. **Advanced RAG Techniques**: Implementing sophisticated features like query rewriting, hypothetical document embeddings (HyDE), or multi-hop reasoning chains. Stick to standard retrieval-augmented generation.

8. **Mobile App Integration**: Extending the chatbot to native iOS/Android apps. Focus remains on web-based documentation site integration.

9. **Conversation Moderation**: Building content filtering for inappropriate queries or implementing human-in-the-loop review workflows. Basic off-topic detection only.

10. **Performance Optimization for Scale**: Engineering for massive scale (100K+ daily users) with distributed caching, load balancing, or edge deployment. Target is moderate documentation site traffic (hundreds of daily users).

11. **Feedback Collection UI**: Adding thumbs-up/down buttons, detailed feedback forms, or satisfaction surveys within the chat widget. Implicit metrics only (conversation length, abandonment rate).

12. **Integration with External Systems**: Connecting to ticketing systems, CRMs, or other third-party platforms for escalation or data synchronization.

## Dependencies *(if applicable)*

### External Systems

- **Qdrant Cloud**: Vector database service hosting embedded documentation chunks. If Qdrant experiences downtime or API changes, the retrieval pipeline breaks. Owner: Qdrant team. SLA: 99.9% uptime per their terms.

- **Google Gemini API (Free Tier)**: Primary LLM provider for response generation using the `gemini-2.0-flash` model. Subject to rate limits (approximately 15 requests/minute on free tier) and potential model deprecations. Owner: Google AI. Accessed via LiteLLM integration in OpenAI Agents SDK. No fallback provider configured to maintain zero-cost operation.

- **Render Platform**: Hosting infrastructure for both frontend static site and backend web service. Deployment pipeline depends on Render's build system and environment configuration. Owner: Render.com.

- **Context7 MCP Server**: Required documentation source for OpenAI Agents SDK and ChatKit framework information during all development phases (planning, tasks, implementation). Agents must query Context7 library IDs `/openai/openai-agents-python` and `/openai/chatkit-js` for up-to-date code examples, API references, and integration patterns. Owner: Context7. This is a MANDATORY dependency for ensuring implementation accuracy.

### Internal Systems

- **Docusaurus Documentation Site**: The frontend application that embeds the chatbot widget. Changes to Docusaurus configuration (e.g., theme customization, build process) can affect chatbot integration. Owner: Internal documentation team.

- **Documentation Content Repository**: Source of truth for documentation that gets indexed into the vector database. Content updates require re-embedding and re-indexing. Owner: Content authors and technical writers.

### Libraries and Frameworks

- **OpenAI Agents SDK (Python)**: Primary framework for building the RAG chatbot with multi-agent capabilities. Provides lightweight primitives for agent orchestration, conversation management (SQLiteSession/RedisSession), built-in tracing, and tool integration. Owner: OpenAI. Version: Latest stable (0.2.9+). Chosen for its simplicity, production-ready patterns, and direct integration with multiple LLM providers including Google Gemini.

**Key Framework Capabilities**:
- **Agent System**: Create conversational agents with custom instructions and tools using `Agent` class
- **Session Management**: Built-in conversation memory via `SQLiteSession` (local persistence) or `RedisSession` (distributed/scalable)
- **Function Tools**: Define RAG retrieval logic as `@function_tool` decorated Python functions that agents can invoke
- **Runner**: Unified execution interface via `Runner.run()` for orchestrating agent interactions with automatic context management
- **LLM Flexibility**: Supports Google Gemini (via LiteLLM integration) as the primary free-tier LLM provider

**LLM Integration via LiteLLM**:
- **LiteLLM Extension**: Install with `pip install "openai-agents[litellm]"` to enable Gemini support
- **Gemini Configuration**: Use `LitellmModel(model="gemini/gemini-2.0-flash", api_key="...")` for free-tier access
- **Usage Tracking**: Enable with `ModelSettings(include_usage=True)` for cost monitoring and token tracking
- **Unified API**: Single interface for multiple LLM providers without code changes

**Backend Integration Approach**:
- **Embedding Model Library**: Maintain current Sentence Transformers (`all-MiniLM-L6-v2`) for consistency with existing Qdrant vector database embeddings. No framework lock-in required.
- **Vector Database Client**: Keep Qdrant Python client as-is. Wrap retrieval logic in `@function_tool` decorated functions that query Qdrant and return relevant document chunks.
- **LLM Orchestration**: Leverage OpenAI Agents SDK's built-in retry logic, error handling, and session management instead of custom implementation. Eliminates need for manual Tenacity decorators and custom fallback chains.

---

- **OpenAI ChatKit (@openai/chatkit-react)**: Modern, production-ready React UI framework for building AI-powered chat interfaces. Replaces custom ChatbotWidget with a professional prebuilt widget featuring markdown rendering, code syntax highlighting, response streaming, mobile responsiveness, and deep customization. Owner: OpenAI. Install: `npm install @openai/chatkit-react`.

**ChatKit Prebuilt Widget Features**:
- **Complete Chat UI**: Ready-to-use interface with message bubbles, avatars, timestamps, and input composer
- **Markdown & Code Support**: Automatic rendering of formatted text and syntax-highlighted code blocks
- **Responsive & Mobile-Friendly**: Adapts seamlessly to desktop and mobile screen sizes
- **Built-in Streaming**: Token-by-token response display with typing indicators
- **Theme Customization**: Dark/light modes, accent colors, border radius, typography, density settings
- **Event Lifecycle**: Hooks for `onReady`, `onError`, `onResponseStart`, `onResponseEnd`, `onThreadChange`
- **Client Tools**: Expose client-side actions (copy message, share, open links) that the chat can invoke
- **Custom Backend Integration**: Connect to any API backend (FastAPI) via `getClientSecret()` callback

**Frontend Integration Approach**:
- **Replace Custom Widget**: Remove current `ChatbotWidget.tsx` and `ChatbotWidget.module.css` (70 lines total)
- **Install ChatKit**: `npm install @openai/chatkit-react` in Docusaurus project (`docs/` directory)
- **Backend Connection**: Configure `useChatKit({ api: { getClientSecret: async () => {...} } })` to fetch session tokens from FastAPI `/chat` endpoint
- **Docusaurus Integration**: Wrap `<ChatKit control={control} />` in existing `BrowserOnly` component pattern (same as current implementation in `Root.tsx`)
- **Theme Matching**: Customize ChatKit theme to match Docusaurus color scheme using `theme: { colorScheme, color, radius, typography }` options

## Non-Goals *(if applicable)*

1. **Achieving 100% Factual Accuracy**: While aiming for high relevance and correctness, acknowledge that LLMs can occasionally produce incorrect or hallucinated information. Focus on improving retrieval quality and citation transparency rather than guaranteeing perfect accuracy.

2. **Real-Time Streaming Responses**: ChatKit provides built-in streaming support out of the box. This is now IN SCOPE and will be implemented as part of the ChatKit integration (User Story 5).

3. **Comprehensive Testing of All Edge Cases**: Given the infinite variety of user inputs, exhaustively testing every possible query is impractical. Focus on representative test cases covering common patterns, documented edge cases, and previously reported bugs.

4. **Zero Downtime Deployment**: While maintaining high availability is important, requiring sophisticated blue-green deployment or canary releases is over-engineered for a documentation site chatbot. Brief maintenance windows (< 5 minutes) during off-peak hours are acceptable.

5. **Competing with ChatGPT's Capabilities**: The chatbot is domain-specific and documentation-focused, not a general-purpose AI assistant. It's acceptable for it to decline general knowledge questions or lack the conversational sophistication of frontier models.

6. **Handling Adversarial Attacks**: While basic input sanitization is required, defending against determined adversarial users attempting prompt injection, jailbreaking, or other sophisticated attacks is out of scope. Rely on API-level protections from LLM providers.

7. **Offline Functionality**: The chatbot requires active internet connectivity to access vector databases and LLM APIs. Supporting offline modes or client-side inference is not a goal.

8. **Automatic Documentation Updates**: If documentation content changes, the vector database must be manually re-indexed. Automatically detecting content changes and triggering re-embedding pipelines is out of scope.
