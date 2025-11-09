import React, { useState } from 'react';
import '../styles/tokens.css';

interface DisclaimerBannerProps {
  text?: string;
  dismissible?: boolean;
}

const DEFAULT_DISCLAIMER = 'Facts-only. No investment advice. This assistant only provides factual information drawn from official AMC / AMFI / SEBI public pages. It does not offer investment advice, recommendations, or portfolio suggestions. Always verify critical details from the original scheme documents linked in each response.';

const DisclaimerBanner: React.FC<DisclaimerBannerProps> = ({
  text = DEFAULT_DISCLAIMER,
  dismissible = false,
}) => {
  const [dismissed, setDismissed] = useState(false);

  if (dismissed && dismissible) {
    return null;
  }

  return (
    <div
      style={{
        width: '100%',
        backgroundColor: 'var(--color-background-alt)',
        borderBottom: `1px solid var(--color-border)`,
        padding: 'var(--spacing-3) var(--spacing-6)',
        fontSize: 'var(--font-size-sm)',
        color: 'var(--color-text-light)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: 'var(--spacing-4)',
      }}
      role="alert"
      aria-live="polite"
    >
      <p style={{ margin: 0, flex: 1 }}>{text}</p>
      {dismissible && (
        <button
          onClick={() => setDismissed(true)}
          style={{
            background: 'none',
            border: 'none',
            color: 'var(--color-text-light)',
            cursor: 'pointer',
            fontSize: 'var(--font-size-lg)',
            padding: 'var(--spacing-1)',
            lineHeight: 1,
          }}
          aria-label="Dismiss disclaimer"
        >
          ×
        </button>
      )}
    </div>
  );
};

export default DisclaimerBanner;

