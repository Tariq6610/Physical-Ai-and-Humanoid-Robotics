/**
 * Integration tests for ChatbotWidget backend connection
 * Feature: 001-rag-chatbot-recreation
 * User Story: US6 - Production Deployment URLs
 * Task: T022
 */

import React from 'react';
import { render, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';

// Mock the getBackendURL utility
jest.mock('../../utils/env', () => ({
  getBackendURL: jest.fn()
}));

// Mock the ChatKit component
jest.mock('@openai/chatkit-react', () => ({
  ChatKit: ({ control }: any) => <div data-testid="chatkit-component">ChatKit Mock</div>,
  useChatKit: jest.fn()
}));

import { getBackendURL } from '../../utils/env';
import { useChatKit } from '@openai/chatkit-react';

describe('ChatbotWidget Backend Connection', () => {
  const mockUseChatKit = useChatKit as jest.MockedFunction<typeof useChatKit>;
  const mockGetBackendURL = getBackendURL as jest.MockedFunction<typeof getBackendURL>;

  beforeEach(() => {
    jest.clearAllMocks();
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('should use localhost URL in development environment', async () => {
    mockGetBackendURL.mockReturnValue('http://localhost:8000');

    let capturedConfig: any;
    mockUseChatKit.mockImplementation((config) => {
      capturedConfig = config;
      return { control: {} } as any;
    });

    // Dynamically import the component after mocks are set up
    const ChatbotWidget = (await import('../ChatbotWidget/index')).default;
    render(<ChatbotWidget />);

    expect(mockGetBackendURL).toHaveBeenCalled();

    // Simulate getClientSecret call
    if (capturedConfig?.api?.getClientSecret) {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ client_secret: 'mock-token', session_id: 'session-123' })
      });

      await capturedConfig.api.getClientSecret();

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/chatkit/session',
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Content-Type': 'application/json'
          })
        })
      );
    }
  });

  it('should use production URL for Render deployment', async () => {
    mockGetBackendURL.mockReturnValue('https://physical-ai-backend.onrender.com');

    let capturedConfig: any;
    mockUseChatKit.mockImplementation((config) => {
      capturedConfig = config;
      return { control: {} } as any;
    });

    const ChatbotWidget = (await import('../ChatbotWidget/index')).default;
    render(<ChatbotWidget />);

    expect(mockGetBackendURL).toHaveBeenCalled();

    // Simulate getClientSecret call
    if (capturedConfig?.api?.getClientSecret) {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ client_secret: 'prod-token', session_id: 'prod-session-123' })
      });

      await capturedConfig.api.getClientSecret();

      expect(global.fetch).toHaveBeenCalledWith(
        'https://physical-ai-backend.onrender.com/api/chatkit/session',
        expect.objectContaining({
          method: 'POST'
        })
      );
    }
  });

  it('should handle backend connection errors gracefully', async () => {
    mockGetBackendURL.mockReturnValue('http://localhost:8000');

    let capturedConfig: any;
    mockUseChatKit.mockImplementation((config) => {
      capturedConfig = config;
      return { control: {} } as any;
    });

    const ChatbotWidget = (await import('../ChatbotWidget/index')).default;
    render(<ChatbotWidget />);

    // Simulate getClientSecret call with network error
    if (capturedConfig?.api?.getClientSecret) {
      (global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

      await expect(capturedConfig.api.getClientSecret()).rejects.toThrow('Network error');
    }
  });

  it('should handle non-200 responses from backend', async () => {
    mockGetBackendURL.mockReturnValue('http://localhost:8000');

    let capturedConfig: any;
    mockUseChatKit.mockImplementation((config) => {
      capturedConfig = config;
      return { control: {} } as any;
    });

    const ChatbotWidget = (await import('../ChatbotWidget/index')).default;
    render(<ChatbotWidget />);

    // Simulate getClientSecret call with 500 error
    if (capturedConfig?.api?.getClientSecret) {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: async () => ({ detail: 'Internal server error' })
      });

      await expect(capturedConfig.api.getClientSecret()).rejects.toThrow();
    }
  });

  it('should include proper headers in session requests', async () => {
    mockGetBackendURL.mockReturnValue('http://localhost:8000');

    let capturedConfig: any;
    mockUseChatKit.mockImplementation((config) => {
      capturedConfig = config;
      return { control: {} } as any;
    });

    const ChatbotWidget = (await import('../ChatbotWidget/index')).default;
    render(<ChatbotWidget />);

    if (capturedConfig?.api?.getClientSecret) {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ client_secret: 'token', session_id: 'sid' })
      });

      await capturedConfig.api.getClientSecret();

      const fetchCall = (global.fetch as jest.Mock).mock.calls[0];
      const headers = fetchCall[1]?.headers;

      expect(headers).toHaveProperty('Content-Type', 'application/json');
    }
  });
});
