/**
 * API Client for FAQ Assistant
 * Handles communication with the backend API
 */

export interface FAQResponse {
  status: 'success' | 'error' | 'no_match' | 'refusal';
  answer?: string;
  source?: string;
  last_updated?: string;
  error_type?: string;
  message?: string;
  matched_q_key?: string;
  similarity?: number;
}

export async function queryFAQ(query: string): Promise<FAQResponse> {
  try {
    const response = await fetch('/api/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: FAQResponse = await response.json();
    return data;
  } catch (error) {
    console.error('Error querying FAQ:', error);
    return {
      status: 'error',
      error_type: 'network_error',
      message: 'Failed to connect to the server. Please try again later.',
    };
  }
}

