/**
 * Environment Utility
 * Provides environment-aware backend URL resolution for deployments.
 */

/**
 * Get the backend URL based on the current environment.
 *
 * @returns Backend URL appropriate for the current environment
 *
 * Logic:
 * - Production (physical-ai-robotics-docs.onrender.com) → Railway backend
 * - Development (localhost) → http://localhost:8000
 * - Other environments → http://localhost:8000 (default fallback)
 */
export function getBackendURL(): string {
  if (typeof window === 'undefined') {
    // Server-side rendering fallback
    return '';
  }

  // Handle missing location object
  if (!window.location || !window.location.hostname) {
    return 'http://localhost:8000';
  }

  const hostname = window.location.hostname;

  // Production deployment (frontend on Render, backend on Railway)
  if (hostname === 'physical-ai-robotics-docs.onrender.com') {
    return 'https://physical-ai-and-humanoid-robotics-production-5817.up.railway.app';
  }

  // Local development or other environments
  return 'http://localhost:8000';
}

/**
 * Check if the current environment is production.
 *
 * @returns true if running in production, false otherwise
 */
export function isProduction(): boolean {
  if (typeof window === 'undefined') {
    return false;
  }
  return window.location.hostname === 'physical-ai-robotics-docs.onrender.com';
}

/**
 * Get the full chat endpoint URL.
 *
 * @returns Full URL for the /chat endpoint
 */
export function getChatEndpointURL(): string {
  return `${getBackendURL()}/chat`;
}

/**
 * Get the full ChatKit session endpoint URL.
 *
 * @returns Full URL for the /api/chatkit/session endpoint
 */
export function getChatKitSessionURL(): string {
  return `${getBackendURL()}/api/chatkit/session`;
}
