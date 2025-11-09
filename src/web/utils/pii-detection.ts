/**
 * PII Detection Utilities for Frontend
 * Detects Personal Identifiable Information in user queries
 */

const PAN_PATTERN = /[A-Z]{5}[0-9]{4}[A-Z]/;
const AADHAAR_PATTERN = /\b\d{4}\s?\d{4}\s?\d{4}\b/;
const ACCOUNT_PATTERN = /\b\d{9,18}\b/;

export interface PIIDetectionResult {
  hasPII: boolean;
  detectedTypes: string[];
  message?: string;
}

export function detectPII(query: string): PIIDetectionResult {
  const detectedTypes: string[] = [];

  // Check for PAN
  if (PAN_PATTERN.test(query)) {
    detectedTypes.push('PAN');
  }

  // Check for Aadhaar
  if (AADHAAR_PATTERN.test(query)) {
    detectedTypes.push('Aadhaar');
  }

  // Check for account numbers (9-18 digits)
  if (ACCOUNT_PATTERN.test(query)) {
    detectedTypes.push('Account Number');
  }

  if (detectedTypes.length > 0) {
    return {
      hasPII: true,
      detectedTypes,
      message: `Personal information detected: ${detectedTypes.join(', ')}. Please remove personal information from your query.`,
    };
  }

  return {
    hasPII: false,
    detectedTypes: [],
  };
}

