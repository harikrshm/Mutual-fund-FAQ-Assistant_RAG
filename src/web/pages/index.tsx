import React, { useState } from 'react';
import Head from 'next/head';
import Header from '../components/Header';
import DisclaimerBanner from '../components/DisclaimerBanner';
import QueryBox from '../components/QueryBox';
import ExamplesList from '../components/ExamplesList';
import ResultCard from '../components/ResultCard';
import { queryFAQ, FAQResponse } from '../utils/api-client';
import { detectPII } from '../utils/pii-detection';
import '../styles/tokens.css';

const EXAMPLE_QUESTIONS = [
  'What is the expense ratio of SBI Bluechip Fund?',
  'What is the lock-in period for SBI Long Term Equity Fund?',
  'What is the minimum SIP amount for SBI Flexicap Fund?',
  'What is the riskometer rating for SBI Magnum Gilt Fund?',
  'How to download statements for SBI Mutual Fund?',
];

export default function Home() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState<FAQResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleQuery = async (userQuery: string) => {
    // Reset state
    setError(null);
    setResponse(null);
    setQuery(userQuery);

    // Check for PII
    const piiResult = detectPII(userQuery);
    if (piiResult.hasPII) {
      setError(piiResult.message || 'Personal information detected');
      return;
    }

    // Query FAQ
    setLoading(true);
    try {
      const result = await queryFAQ(userQuery);
      setResponse(result);

      if (result.status === 'error' && result.message) {
        setError(result.message);
      }
    } catch (err: any) {
      setError('An error occurred while processing your query. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (example: string) => {
    handleQuery(example);
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: 'var(--color-background-alt)',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <Head>
        <title>Mutual Fund FAQ Assistant</title>
        <meta name="description" content="FAQ Assistant for SBI Mutual Fund schemes" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Header />
      <DisclaimerBanner dismissible={false} />

      <main
        style={{
          flex: 1,
          maxWidth: '800px',
          width: '100%',
          margin: '0 auto',
          padding: 'var(--spacing-8) var(--spacing-6)',
        }}
      >
        <div
          style={{
            textAlign: 'center',
            marginBottom: 'var(--spacing-8)',
          }}
        >
          <h2
            style={{
              fontSize: 'var(--font-size-3xl)',
              fontWeight: 'var(--font-weight-bold)',
              color: 'var(--color-text)',
              marginBottom: 'var(--spacing-4)',
            }}
          >
            Ask a Question
          </h2>
          <p
            style={{
              fontSize: 'var(--font-size-base)',
              color: 'var(--color-text-light)',
              margin: 0,
            }}
          >
            Get factual information about SBI Mutual Fund schemes
          </p>
        </div>

        <QueryBox
          onSubmit={handleQuery}
          disabled={loading}
          loading={loading}
          error={error || undefined}
        />

        <ExamplesList examples={EXAMPLE_QUESTIONS} onExampleClick={handleExampleClick} />

        {loading && (
          <div
            style={{
              marginTop: 'var(--spacing-6)',
              padding: 'var(--spacing-6)',
              backgroundColor: 'var(--color-background)',
              border: `1px solid var(--color-border)`,
              borderRadius: 'var(--radius-lg)',
              textAlign: 'center',
              color: 'var(--color-text-light)',
            }}
          >
            Loading...
          </div>
        )}

        {response && response.status === 'success' && response.answer && (
          <ResultCard
            answer={response.answer}
            source={response.source || ''}
            lastUpdated={response.last_updated || ''}
          />
        )}

        {response && response.status === 'refusal' && (
          <div
            style={{
              marginTop: 'var(--spacing-6)',
              padding: 'var(--spacing-6)',
              backgroundColor: 'var(--color-background)',
              border: `1px solid var(--color-border)`,
              borderRadius: 'var(--radius-lg)',
              color: 'var(--color-text)',
            }}
          >
            <p style={{ margin: 0, marginBottom: 'var(--spacing-4)' }}>
              {response.message}
            </p>
            {response.source && (
              <a
                href={response.source}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  color: 'var(--color-link)',
                  textDecoration: 'none',
                }}
              >
                Learn more at AMFI →
              </a>
            )}
          </div>
        )}

        {response && response.status === 'no_match' && (
          <div
            style={{
              marginTop: 'var(--spacing-6)',
              padding: 'var(--spacing-6)',
              backgroundColor: 'var(--color-background)',
              border: `1px solid var(--color-border)`,
              borderRadius: 'var(--radius-lg)',
              color: 'var(--color-text-light)',
              textAlign: 'center',
            }}
          >
            <p style={{ margin: 0 }}>{response.message}</p>
          </div>
        )}
      </main>
    </div>
  );
}

