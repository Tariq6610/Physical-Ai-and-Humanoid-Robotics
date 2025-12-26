/**
 * ChatKit Configuration
 * Theme and API configuration for the ChatKit widget.
 */

import { getBackendURL, getChatKitSessionURL } from '../../utils/env';

/**
 * ChatKit theme configuration matching Docusaurus theme.
 */
export const chatKitTheme = {
  colorScheme: 'dark' as const,
  accent: {
    primary: '#25c2a0', // Docusaurus primary green
  },
  typography: {
    fontFamily: 'var(--ifm-font-family-base)',
  },
};

/**
 * Get backend API URL for ChatKit.
 */
export function getApiUrl(): string {
  return getBackendURL();
}

/**
 * Get ChatKit session URL for getClientSecret callback.
 */
export function getSessionUrl(): string {
  return getChatKitSessionURL();
}
