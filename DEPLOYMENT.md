# Deployment Guide

This guide provides instructions for deploying the Physical AI and Humanoid Robotics Book Project.

## Architecture Overview

The project consists of two main services:
1. **Frontend**: A Docusaurus-based static site (documentation)
2. **Backend**: A FastAPI web service (RAG chatbot API)

## Deployment Platforms

### Render (Primary)

The project is configured for deployment on Render using the `render.yaml` file.

#### Prerequisites
- Render account
- Qdrant Cloud account (or self-hosted Qdrant instance)

#### Deployment Steps

1. **Connect your GitHub repository to Render**
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Select your repository
   - Render will automatically detect the `render.yaml` configuration

2. **Configure Environment Variables**

   For the **backend service**, set these environment variables:
   - `QDRANT_URL`: Your Qdrant instance URL
   - `QDRANT_API_KEY`: Your Qdrant API key
   - `QDRANT_COLLECTION_NAME`: `book_content` (or your preferred collection name)
   - `OPENAI_API_KEY`: Your OpenAI API key (if using OpenAI)
   - `PYTHON_VERSION`: Already set to `3.10.13`

   For the **frontend service**, set:
   - `BACKEND_URL`: The URL of your deployed backend service

3. **Deploy**
   - Render will automatically build and deploy both services based on the `render.yaml` configuration
   - The frontend will be deployed as a static site
   - The backend will be deployed as a web service

#### Service URLs
- Frontend: `https://physical-ai-robotics-docs.onrender.com` (or similar)
- Backend: `https://physical-ai-robotics-backend.onrender.com` (or similar)

### Alternative Deployment Options

#### Manual Deployment

1. **Backend (FastAPI)**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

2. **Frontend (Docusaurus)**
   ```bash
   cd docs
   npm install
   npm run build
   npm run serve  # for local serving of built site
   ```

#### Docker Deployment

Coming soon - Docker configurations can be added for containerized deployment.

## Environment Configuration

### Backend Environment Variables

Create a `.env` file in the `backend` directory:

```env
QDRANT_URL=https://your-cluster-url.qdrant.tech:6333
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=book_content
OPENAI_API_KEY=your_openai_api_key
PYTHON_VERSION=3.10.13
```

### Frontend Environment Variables

The Docusaurus site can be configured with environment variables in the build process:

```env
BACKEND_URL=https://your-backend-url.com
```

## Post-Deployment Steps

1. **Content Ingestion**
   After deploying the backend, you need to ingest the book content into your Qdrant vector database:
   ```bash
   python scripts/ingest.py
   ```

2. **Verification**
   - Check that the backend API is accessible and returns proper responses
   - Verify that the chatbot widget on the frontend can communicate with the backend
   - Test a few sample queries to ensure the RAG pipeline works

3. **Monitoring**
   - Set up health checks for both services
   - Monitor response times and error rates
   - Set up alerts for service downtime

## Troubleshooting

### Common Issues

1. **Backend not connecting to Qdrant**
   - Verify QDRANT_URL and QDRANT_API_KEY are correct
   - Check that the Qdrant collection exists
   - Ensure network connectivity between services

2. **Frontend can't reach backend**
   - Verify BACKEND_URL is set correctly
   - Check CORS configuration in the backend
   - Ensure the backend service is running and healthy

3. **Chatbot widget not appearing**
   - Verify the widget is properly integrated in the site layout
   - Check browser console for JavaScript errors
   - Confirm backend API endpoint is accessible

## Scaling Recommendations

### Frontend
- The Docusaurus site is a static site, so it scales well with CDN distribution
- Consider using a CDN like CloudFlare for improved performance

### Backend
- Monitor API response times and scale instances as needed
- Consider implementing caching for frequently requested content
- Set up auto-scaling based on request volume

## Security Considerations

- Use HTTPS for all services
- Rotate API keys regularly
- Implement rate limiting to prevent abuse
- Sanitize user inputs in the chatbot
- Keep dependencies up to date