/**
 * API Service for calling the backend
 */

// Backend API URL for Uvicorn local development
const API_BASE_URL = 'http://localhost:8000';

interface Citation {
  source: string;
  text: string;
}

interface QueryResponse {
  query: string;
  response: string;
  citations: Citation[];
}

/**
 * Query the laws API with a question
 */
export async function queryLaws(query: string): Promise<QueryResponse> {
  const url = `${API_BASE_URL}/query?query=${encodeURIComponent(query)}`;
  
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API request failed: ${response.status} - ${errorText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error querying API:', error);
    throw error;
  }
}