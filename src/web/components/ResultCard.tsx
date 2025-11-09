import React, { useState } from 'react';
import SourceLink from './SourceLink';
import '../styles/tokens.css';

interface ResultCardProps {
  answer: string;
  source: string;
  lastUpdated: string;
  showSourceDetails?: boolean;
}

const ResultCard: React.FC<ResultCardProps> = ({
  answer,
  source,
  lastUpdated,
  showSourceDetails = false,
}) => {
  const [showDetails, setShowDetails] = useState(showSourceDetails);

  return (
    <div
      style={{
        backgroundColor: 'var(--color-background)',
        border: `1px solid var(--color-border)`,
        borderRadius: 'var(--radius-lg)',
        padding: 'var(--spacing-6)',
        boxShadow: 'var(--shadow-md)',
        marginTop: 'var(--spacing-6)',
      }}
      role="region"
      aria-live="polite"
      aria-label="FAQ Answer"
    >
      <div
        style={{
          fontSize: 'var(--font-size-base)',
          lineHeight: 'var(--line-height-relaxed)',
          color: 'var(--color-text)',
          marginBottom: 'var(--spacing-4)',
        }}
      >
        {answer}
      </div>

      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: 'var(--spacing-2)',
          paddingTop: 'var(--spacing-4)',
          borderTop: `1px solid var(--color-border)`,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-2)' }}>
          <SourceLink url={source} />
        </div>

        <div
          style={{
            fontSize: 'var(--font-size-xs)',
            color: 'var(--color-text-muted)',
          }}
        >
          Last updated: {lastUpdated}
        </div>

        <button
          onClick={() => setShowDetails(!showDetails)}
          style={{
            marginTop: 'var(--spacing-2)',
            padding: 'var(--spacing-1) var(--spacing-2)',
            background: 'none',
            border: 'none',
            color: 'var(--color-link)',
            cursor: 'pointer',
            fontSize: 'var(--font-size-xs)',
            textDecoration: 'underline',
          }}
          aria-expanded={showDetails}
          aria-label="Toggle source details"
        >
          {showDetails ? 'Hide' : 'Show'} source details
        </button>

        {showDetails && (
          <div
            style={{
              marginTop: 'var(--spacing-2)',
              padding: 'var(--spacing-3)',
              backgroundColor: 'var(--color-background-alt)',
              borderRadius: 'var(--radius-md)',
              fontSize: 'var(--font-size-xs)',
              color: 'var(--color-text-light)',
            }}
          >
            <div>
              <strong>Source URL:</strong> {source}
            </div>
            <div style={{ marginTop: 'var(--spacing-1)' }}>
              <strong>Last Updated:</strong> {lastUpdated}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultCard;

