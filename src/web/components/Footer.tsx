import React from 'react';
import '../styles/tokens.css';

const Footer: React.FC = () => {
  return (
    <footer
      style={{
        width: '100%',
        padding: 'var(--spacing-6)',
        backgroundColor: 'var(--color-background)',
        borderTop: `1px solid var(--color-border)`,
        marginTop: 'var(--spacing-16)',
      }}
    >
      <div
        style={{
          maxWidth: '1200px',
          margin: '0 auto',
          textAlign: 'center',
          fontSize: 'var(--font-size-sm)',
          color: 'var(--color-text-light)',
        }}
      >
        <p style={{ margin: 0 }}>
          © {new Date().getFullYear()} Mutual Fund FAQ Assistant. Facts-only. No investment advice.
        </p>
      </div>
    </footer>
  );
};

export default Footer;

