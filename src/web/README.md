# Mutual Fund FAQ Assistant - Web Frontend

This is the web frontend for the Mutual Fund FAQ Assistant, built with Next.js, React, and TypeScript.

## Setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+ (for backend API)
- Flask (for API server)

### Installation

1. Install dependencies:
```bash
cd src/web
npm install
```

2. Install Python dependencies for API server:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the Python API server:
```bash
cd src/api
python server.py
```
The API server will run on `http://localhost:5000`

2. Start the Next.js development server:
```bash
cd src/web
npm run dev
```
The web application will run on `http://localhost:3000`

### Environment Variables

Create a `.env.local` file in `src/web/`:
```
FAQ_API_URL=http://localhost:5000
```

## Project Structure

```
src/web/
├── components/          # React components
├── pages/              # Next.js pages
│   ├── api/           # API routes
│   └── index.tsx      # Home page
├── styles/            # CSS and design tokens
├── utils/             # Utility functions
├── __tests__/         # Unit tests
└── e2e/              # E2E tests
```

## Components

- **Header**: Site header with branding
- **QueryBox**: Main query input component
- **ExamplesList**: Example question chips
- **ResultCard**: FAQ answer display
- **SourceLink**: Source URL link component
- **DisclaimerBanner**: Compliance disclaimer banner
- **Footer**: Site footer

## Testing

### Unit Tests
```bash
npm test
```

### E2E Tests
```bash
npm run test:e2e
```

## Building for Production

```bash
npm run build
npm start
```

## Accessibility

The application follows WCAG AA standards:
- ARIA labels on all interactive elements
- Keyboard navigation support
- Color contrast compliance
- Screen reader support

## Design Tokens

Design tokens are defined in `styles/tokens.css` and can be customized to match Figma designs.

