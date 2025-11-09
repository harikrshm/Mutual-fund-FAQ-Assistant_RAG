import { detectPII } from '../../utils/pii-detection';

describe('PII Detection', () => {
  it('detects PAN number', () => {
    const result = detectPII('My PAN is ABCDE1234F');
    expect(result.hasPII).toBe(true);
    expect(result.detectedTypes).toContain('PAN');
  });

  it('detects Aadhaar number', () => {
    const result = detectPII('My Aadhaar is 1234 5678 9012');
    expect(result.hasPII).toBe(true);
    expect(result.detectedTypes).toContain('Aadhaar');
  });

  it('detects account number', () => {
    const result = detectPII('Account number is 123456789012');
    expect(result.hasPII).toBe(true);
    expect(result.detectedTypes).toContain('Account Number');
  });

  it('returns no PII for normal query', () => {
    const result = detectPII('What is the expense ratio?');
    expect(result.hasPII).toBe(false);
    expect(result.detectedTypes).toHaveLength(0);
  });
});

