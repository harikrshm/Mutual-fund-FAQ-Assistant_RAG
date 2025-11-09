import React from 'react';
import '../styles/tokens.css';

interface SourceLinkProps {
  url: string;
  text?: string;
}

const SourceLink: React.FC<SourceLinkProps> = ({ url, text }) => {
  const displayText = text || url;

  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      style={{
        color: 'var(--color-link)',
        textDecoration: 'none',
        fontSize: 'var(--font-size-sm)',
        display: 'inline-flex',
        alignItems: 'center',
        gap: 'var(--spacing-1)',
        transition: 'var(--transition-base)',
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.color = 'var(--color-link-hover)';
        e.currentTarget.style.textDecoration = 'underline';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.color = 'var(--color-link)';
        e.currentTarget.style.textDecoration = 'none';
      }}
      aria-label={`Source: ${displayText} (opens in new tab)`}
    >
      {displayText}
      <span aria-hidden="true" style={{ fontSize: 'var(--font-size-xs)' }}>
        ↗
      </span>
    </a>
  );
};

export default SourceLink;

