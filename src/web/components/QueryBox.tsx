import React, { useState, KeyboardEvent } from 'react';
import '../styles/tokens.css';

interface QueryBoxProps {
  onSubmit: (query: string) => void;
  placeholder?: string;
  disabled?: boolean;
  error?: string;
  loading?: boolean;
}

const QueryBox: React.FC<QueryBoxProps> = ({
  onSubmit,
  placeholder = 'Ask a question about SBI Mutual Fund schemes...',
  disabled = false,
  error,
  loading = false,
}) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && !disabled && !loading) {
      onSubmit(query.trim());
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ width: '100%' }}>
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: 'var(--spacing-2)',
        }}
      >
        <div
          style={{
            position: 'relative',
            display: 'flex',
            gap: 'var(--spacing-2)',
            alignItems: 'flex-start',
          }}
        >
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            disabled={disabled || loading}
            rows={3}
            style={{
              flex: 1,
              padding: 'var(--spacing-3)',
              fontSize: 'var(--font-size-base)',
              fontFamily: 'var(--font-family)',
              border: `1px solid ${error ? 'var(--color-error)' : 'var(--color-border)'}`,
              borderRadius: 'var(--radius-lg)',
              resize: 'vertical',
              outline: 'none',
              transition: 'var(--transition-base)',
              backgroundColor: disabled || loading ? 'var(--color-background-alt)' : 'var(--color-background)',
              color: 'var(--color-text)',
            }}
            onFocus={(e) => {
              if (!error) {
                e.currentTarget.style.borderColor = 'var(--color-border-focus)';
                e.currentTarget.style.boxShadow = '0 0 0 3px rgba(37, 99, 235, 0.1)';
              }
            }}
            onBlur={(e) => {
              if (!error) {
                e.currentTarget.style.borderColor = 'var(--color-border)';
                e.currentTarget.style.boxShadow = 'none';
              }
            }}
            aria-label="Query input"
            aria-describedby={error ? 'query-error' : undefined}
            aria-invalid={!!error}
          />
          <button
            type="submit"
            disabled={disabled || loading || !query.trim()}
            style={{
              padding: 'var(--spacing-3) var(--spacing-6)',
              backgroundColor: disabled || loading || !query.trim() 
                ? 'var(--color-border)' 
                : 'var(--color-primary)',
              color: 'white',
              border: 'none',
              borderRadius: 'var(--radius-lg)',
              fontSize: 'var(--font-size-base)',
              fontWeight: 'var(--font-weight-medium)',
              cursor: disabled || loading || !query.trim() ? 'not-allowed' : 'pointer',
              transition: 'var(--transition-base)',
              whiteSpace: 'nowrap',
            }}
            onMouseEnter={(e) => {
              if (!disabled && !loading && query.trim()) {
                e.currentTarget.style.backgroundColor = 'var(--color-primary-hover)';
              }
            }}
            onMouseLeave={(e) => {
              if (!disabled && !loading && query.trim()) {
                e.currentTarget.style.backgroundColor = 'var(--color-primary)';
              }
            }}
            aria-label="Submit query"
          >
            {loading ? 'Loading...' : 'Submit'}
          </button>
        </div>

        {error && (
          <div
            id="query-error"
            role="alert"
            style={{
              padding: 'var(--spacing-2) var(--spacing-3)',
              backgroundColor: 'var(--color-error-bg)',
              border: `1px solid var(--color-error)`,
              borderRadius: 'var(--radius-md)',
              color: 'var(--color-error)',
              fontSize: 'var(--font-size-sm)',
            }}
          >
            {error}
          </div>
        )}
      </div>
    </form>
  );
};

export default QueryBox;

