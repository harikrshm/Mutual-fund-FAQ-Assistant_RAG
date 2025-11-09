import React from 'react';
import '../styles/tokens.css';

interface ExamplesListProps {
  examples: string[];
  onExampleClick: (example: string) => void;
}

const ExamplesList: React.FC<ExamplesListProps> = ({ examples, onExampleClick }) => {
  return (
    <div
      style={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: 'var(--spacing-3)',
        marginTop: 'var(--spacing-6)',
      }}
    >
      {examples.map((example, index) => (
        <button
          key={index}
          onClick={() => onExampleClick(example)}
          style={{
            padding: 'var(--spacing-2) var(--spacing-4)',
            backgroundColor: 'var(--color-background)',
            border: `1px solid var(--color-border)`,
            borderRadius: 'var(--radius-full)',
            fontSize: 'var(--font-size-sm)',
            color: 'var(--color-text)',
            cursor: 'pointer',
            transition: 'var(--transition-base)',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = 'var(--color-background-alt)';
            e.currentTarget.style.borderColor = 'var(--color-primary)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = 'var(--color-background)';
            e.currentTarget.style.borderColor = 'var(--color-border)';
          }}
          aria-label={`Example question: ${example}`}
        >
          {example}
        </button>
      ))}
    </div>
  );
};

export default ExamplesList;

