/**
 * Next.js API Route for FAQ Queries
 * Proxies requests to Python Flask API server
 */

import type { NextApiRequest, NextApiResponse } from 'next';

interface QueryRequest {
  query: string;
}

interface QueryResponse {
  status: 'success' | 'error' | 'no_match' | 'refusal';
  answer?: string;
  source?: string;
  last_updated?: string;
  error_type?: string;
  message?: string;
  matched_q_key?: string;
  similarity?: number;
}

const API_BASE_URL = process.env.FAQ_API_URL || 'http://localhost:5000';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<QueryResponse>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({
      status: 'error',
      error_type: 'method_not_allowed',
      message: 'Method not allowed',
    });
  }

  const { query }: QueryRequest = req.body;

  if (!query || typeof query !== 'string') {
    return res.status(400).json({
      status: 'error',
      error_type: 'invalid_request',
      message: 'Query is required',
    });
  }

  try {
    // Proxy request to Python API server
    const response = await fetch(`${API_BASE_URL}/api/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      throw new Error(`API server error: ${response.status}`);
    }

    const result: QueryResponse = await response.json();
    return res.status(200).json(result);
  } catch (error: any) {
    console.error('Error processing FAQ query:', error);
    return res.status(500).json({
      status: 'error',
      error_type: 'server_error',
      message: 'An error occurred while processing your query. Please try again.',
    });
  }
}

