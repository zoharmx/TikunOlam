# Tikun Olam Frontend

Modern React + TypeScript frontend for the Tikun Olam ethical AI reasoning framework.

## Features

- **Multi-Sefirot Visualization**: View analysis results from all 10 Kabbalistic Sefirot
- **BinahSigma Dashboard**: Dedicated view for multi-civilizational bias analysis
- **Real-time Analysis**: Submit scenarios and receive comprehensive ethical evaluations
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Dark Theme**: Professional dark UI with Kabbalah-inspired color scheme

## Technology Stack

- **React 18**: Modern UI library
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool and dev server
- **Axios**: HTTP client for API communication
- **CSS Variables**: Themeable design system

## Quick Start

### Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Application will be available at http://localhost:3000
```

### Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Docker

```bash
# Build and run with Docker Compose (from root directory)
docker-compose up --build tikun-frontend

# Or build individually
docker build -t tikun-frontend .
docker run -p 3000:80 tikun-frontend
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── Header.tsx       # Application header
│   │   ├── AnalysisForm.tsx # Scenario input form
│   │   ├── LoadingState.tsx # Loading animation with Sefirot stages
│   │   ├── Results.tsx      # Main results view with tabs
│   │   ├── BinahSigmaView.tsx # Multi-civilizational analysis view
│   │   └── SefirahCard.tsx  # Individual Sefirah display
│   ├── services/
│   │   └── api.ts          # API client
│   ├── types/
│   │   └── index.ts        # TypeScript interfaces
│   ├── App.tsx             # Main application component
│   ├── main.tsx            # Application entry point
│   └── index.css           # Global styles
├── index.html              # HTML template
├── vite.config.ts          # Vite configuration
├── tsconfig.json           # TypeScript configuration
├── Dockerfile              # Docker build configuration
├── nginx.conf              # Nginx server configuration
└── package.json            # Dependencies and scripts
```

## API Integration

The frontend connects to the Tikun Olam API backend:

- **Development**: Proxied through Vite dev server (`/api` → `http://localhost:8000`)
- **Production**: Proxied through Nginx (`/api` → `http://tikun-api:8000`)

## Environment Variables

No environment variables required. API endpoints are configured through proxy.

## Components

### AnalysisForm
- Input form for ethical scenarios
- Example scenarios included
- Character counter
- BinahSigma activation indicator

### LoadingState
- Animated Sefirot progression
- Shows current processing stage
- Estimated completion time

### Results
- Three tabs: Summary, 10 Sefirot, BinahSigma
- Overall metrics and decision
- Export functionality

### BinahSigmaView
- Bias delta visualization
- Western vs Eastern blind spots comparison
- Universal convergence points
- Transcendent synthesis

### SefirahCard
- Collapsible cards for each Sefirah
- Color-coded by Kabbalistic correspondence
- Detailed metrics and insights

## Color Scheme

Based on Kabbalistic Sefirot:

- **Keter** (Purple): Crown - Ethical validation
- **Chochmah** (Blue): Wisdom - Pattern analysis
- **Binah** (Teal): Understanding - Multi-civilizational
- **Chesed** (Gold): Kindness - Opportunities
- **Gevurah** (Red): Severity - Risks
- **Tiferet** (Orange): Beauty - Synthesis
- **Netzach** (Green): Victory - Strategy
- **Hod** (Steel Blue): Glory - Communication
- **Yesod** (Light Blue): Foundation - Integration
- **Malchut** (Royal Purple): Kingdom - Decision

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions

## Performance

- **Bundle Size**: ~150KB (gzipped)
- **First Contentful Paint**: <1s
- **Time to Interactive**: <2s

## Development

### Code Style

- TypeScript strict mode enabled
- ESLint for code quality
- Prettier for formatting (recommended)

### Adding New Components

```typescript
// components/NewComponent.tsx
interface NewComponentProps {
  data: string;
}

function NewComponent({ data }: NewComponentProps) {
  return <div>{data}</div>;
}

export default NewComponent;
```

## Deployment

### Nginx Configuration

The production build uses Nginx with:
- Gzip compression
- Security headers
- API proxying
- SPA routing support
- Static asset caching

### Docker Multi-stage Build

1. **Builder stage**: Compiles TypeScript and bundles with Vite
2. **Production stage**: Serves static files with Nginx

## License

Part of the Tikun Olam project.

## Support

For issues or questions, refer to the main project documentation.
