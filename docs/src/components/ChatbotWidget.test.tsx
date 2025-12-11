import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatbotWidget from './ChatbotWidget';

// Mock fetch API
global.fetch = jest.fn();

describe('ChatbotWidget', () => {
  beforeEach(() => {
    (global.fetch as jest.MockedFunction<typeof fetch>).mockClear();
  });

  test('renders closed chatbot initially', () => {
    render(<ChatbotWidget />);

    // Initially, the chat window should not be visible
    expect(screen.queryByRole('textbox')).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Chat/i })).toBeInTheDocument();
  });

  test('toggles chat window open and closed', () => {
    render(<ChatbotWidget />);

    // Click to open
    const toggleButton = screen.getByRole('button', { name: /Chat/i });
    fireEvent.click(toggleButton);

    // Chat window should now be visible
    expect(screen.getByRole('textbox')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Close/i })).toBeInTheDocument();

    // Click to close
    fireEvent.click(screen.getByRole('button', { name: /Close/i }));

    // Chat window should be hidden again
    expect(screen.queryByRole('textbox')).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Chat/i })).toBeInTheDocument();
  });

  test('sends a message when send button is clicked', async () => {
    const mockResponse = { answer: 'This is a test response' };
    (global.fetch as jest.MockedFunction<typeof fetch>).mockResolvedValue({
      json: jest.fn().mockResolvedValue(mockResponse),
    } as Response);

    render(<ChatbotWidget />);

    // Open the chat
    fireEvent.click(screen.getByRole('button', { name: /Chat/i }));

    // Type a message
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'Hello, world!' } });

    // Click send
    fireEvent.click(screen.getByText('Send'));

    // Wait for the message to appear
    await waitFor(() => {
      expect(screen.getByText('Hello, world!')).toBeInTheDocument();
    });

    // Check that fetch was called with correct parameters
    expect(global.fetch).toHaveBeenCalledWith('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: 'Hello, world!' }),
    });
  });

  test('sends a message when Enter key is pressed', async () => {
    const mockResponse = { answer: 'This is a test response' };
    (global.fetch as jest.MockedFunction<typeof fetch>).mockResolvedValue({
      json: jest.fn().mockResolvedValue(mockResponse),
    } as Response);

    render(<ChatbotWidget />);

    // Open the chat
    fireEvent.click(screen.getByRole('button', { name: /Chat/i }));

    // Type a message
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'Hello, world!' } });

    // Press Enter
    fireEvent.keyPress(input, { key: 'Enter', code: 'Enter' });

    // Wait for the message to appear
    await waitFor(() => {
      expect(screen.getByText('Hello, world!')).toBeInTheDocument();
    });

    // Check that fetch was called
    expect(global.fetch).toHaveBeenCalledTimes(1);
  });

  test('displays bot response after sending a message', async () => {
    const mockResponse = { answer: 'This is a test response' };
    (global.fetch as jest.MockedFunction<typeof fetch>).mockResolvedValue({
      json: jest.fn().mockResolvedValue(mockResponse),
    } as Response);

    render(<ChatbotWidget />);

    // Open the chat
    fireEvent.click(screen.getByRole('button', { name: /Chat/i }));

    // Type and send a message
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'Hello, bot!' } });
    fireEvent.click(screen.getByText('Send'));

    // Wait for the bot response to appear
    await waitFor(() => {
      expect(screen.getByText('This is a test response')).toBeInTheDocument();
    });
  });

  test('displays error message when fetch fails', async () => {
    (global.fetch as jest.MockedFunction<typeof fetch>).mockRejectedValue(
      new Error('Network error')
    );

    render(<ChatbotWidget />);

    // Open the chat
    fireEvent.click(screen.getByRole('button', { name: /Chat/i }));

    // Type and send a message
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'Hello, bot!' } });
    fireEvent.click(screen.getByText('Send'));

    // Wait for the error message to appear
    await waitFor(() => {
      expect(screen.getByText("Sorry, I'm having trouble connecting.")).toBeInTheDocument();
    });
  });

  test('does not send empty messages', () => {
    render(<ChatbotWidget />);

    // Open the chat
    fireEvent.click(screen.getByRole('button', { name: /Chat/i }));

    // Try to send an empty message
    fireEvent.click(screen.getByText('Send'));

    // Fetch should not have been called
    expect(global.fetch).not.toHaveBeenCalled();
  });

  test('shows loading indicator when fetching response', async () => {
    // Create a promise that doesn't resolve immediately to simulate loading
    const mockPromise = new Promise((resolve) => {
      setTimeout(() => resolve({ json: () => ({ answer: 'Test response' }) }), 100);
    });
    (global.fetch as jest.MockedFunction<typeof fetch>).mockReturnValue(mockPromise as Promise<Response>);

    render(<ChatbotWidget />);

    // Open the chat
    fireEvent.click(screen.getByRole('button', { name: /Chat/i }));

    // Type and send a message
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'Hello, bot!' } });
    fireEvent.click(screen.getByText('Send'));

    // Loading indicator should appear
    expect(screen.getByText('...')).toBeInTheDocument();
  });
});