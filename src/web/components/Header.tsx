import React from 'react';
import '../styles/tokens.css';

interface HeaderProps {
  title?: string;
}

const Header: React.FC<HeaderProps> = ({ title = 'Mutual Fund FAQ Assistant' }) => {
  return (
    <header
      style={{
        width: '100%',
        padding: 'var(--spacing-4) var(--spacing-6)',
        backgroundColor: 'var(--color-background)',
        borderBottom: `1px solid var(--color-border)`,
        boxShadow: 'var(--shadow-sm)',
      }}
    >
      <div
        style={{
          maxWidth: '1200px',
          margin: '0 auto',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <h1
          style={{
            fontSize: 'var(--font-size-2xl)',
            fontWeight: 'var(--font-weight-bold)',
            color: 'var(--color-text)',
            margin: 0,
          }}
        >
          {title}
        </h1>
      </div>
    </header>
  );
};

export default Header;

