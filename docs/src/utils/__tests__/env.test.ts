/**
 * Tests for environment URL resolution utility
 * Feature: 001-rag-chatbot-recreation
 * User Story: US6 - Production Deployment URLs
 * Task: T021
 */

import { getBackendURL } from '../env';

describe('getBackendURL', () => {
  const originalWindow = global.window;

  beforeEach(() => {
    // Reset window object before each test
    delete (global as any).window;
  });

  afterEach(() => {
    // Restore original window
    global.window = originalWindow;
  });

  it('should return empty string when window is undefined (SSR)', () => {
    expect(getBackendURL()).toBe('');
  });

  it('should return localhost URL for localhost hostname', () => {
    (global as any).window = {
      location: {
        hostname: 'localhost'
      }
    };

    expect(getBackendURL()).toBe('http://localhost:8000');
  });

  it('should return localhost URL for 127.0.0.1', () => {
    (global as any).window = {
      location: {
        hostname: '127.0.0.1'
      }
    };

    expect(getBackendURL()).toBe('http://localhost:8000');
  });

  it('should return production URL for Render production hostname', () => {
    (global as any).window = {
      location: {
        hostname: 'physical-ai-robotics-docs.onrender.com'
      }
    };

    expect(getBackendURL()).toBe('https://physical-ai-backend.onrender.com');
  });

  it('should return localhost for unknown hostnames (development fallback)', () => {
    (global as any).window = {
      location: {
        hostname: 'some-staging-env.example.com'
      }
    };

    expect(getBackendURL()).toBe('http://localhost:8000');
  });

  it('should handle undefined location gracefully', () => {
    (global as any).window = {};

    expect(() => getBackendURL()).not.toThrow();
  });
});
