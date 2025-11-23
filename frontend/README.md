# Health & Air Quality Dashboard - Frontend

A React-based frontend application for monitoring health metrics and air quality data. Features two dashboards: a public Citizen Dashboard and a protected Health Authority Dashboard.

## Features

### Citizen Dashboard (Public)
- Personal health alerts
- Health trends visualization (line charts)
- Activity distribution (pie charts)
- Recent health statistics
- Real-time data updates

### Health Authority Dashboard (Protected)
- Public health risk maps (interactive Leaflet maps)
- System-wide outbreak alerts
- Community-level ML predictions
- Heatmaps and trend analytics
- Advanced monitoring panels

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **React Router** - Routing
- **Axios** - HTTP client
- **React Query** - Data fetching and caching
- **Recharts** - Chart library
- **Leaflet** - Interactive maps
- **TailwindCSS** - Styling

## Prerequisites

- Node.js 18+ and npm
- Backend API running on `http://localhost:8000`

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Building for Production

Build the application:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Environment Variables

Create a `.env` file in the frontend directory (optional):
```
VITE_API_BASE_URL=http://localhost:8000
```

If not set, the app defaults to `http://localhost:8000`

## Authentication

### Health Authority Login
- **Email:** `health@authority.gov`
- **Password:** `admin123`

The authentication uses localStorage to maintain session state.

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable components
│   │   ├── Alerts/         # Alert components
│   │   ├── Charts/         # Chart components
│   │   ├── Maps/           # Map components
│   │   ├── Layout.jsx      # Main layout with navbar
│   │   ├── ProtectedRoute.jsx
│   │   └── StatsCard.jsx
│   ├── pages/              # Page components
│   │   ├── Dashboard.jsx   # Landing page
│   │   ├── Login.jsx       # Login page
│   │   ├── CitizenDashboard.jsx
│   │   └── AuthorityDashboard.jsx
│   ├── services/           # API services
│   │   └── api.js          # All API endpoint functions
│   ├── utils/              # Utilities
│   │   └── auth.js         # Authentication helpers
│   ├── App.jsx             # Main app component
│   ├── main.jsx            # Entry point
│   └── index.css          # Global styles
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

## API Integration

The frontend integrates with the following API endpoints:

### Health Authority Endpoints
- `GET /api/health-authorities/risk-map` - Risk map data
- `GET /api/health-authorities/alerts` - Health alerts
- `GET /api/health-authorities/stats` - Health statistics

### Citizen Endpoints
- `GET /api/citizens/personal-alerts` - Personal alerts
- `GET /api/citizens/trends` - Personal trends
- `POST /api/citizens/predict-activity` - Activity prediction

### Prediction Endpoints
- `POST /api/predict/air-quality` - Air quality prediction

All API calls are handled through the `src/services/api.js` file using Axios.

## Deployment

### Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

3. Set environment variable:
   - In Vercel dashboard, add `VITE_API_BASE_URL` with your API URL

### Netlify

1. Install Netlify CLI:
```bash
npm i -g netlify-cli
```

2. Build the project:
```bash
npm run build
```

3. Deploy:
```bash
netlify deploy --prod --dir=dist
```

4. Set environment variable in Netlify dashboard:
   - `VITE_API_BASE_URL` = your API URL

### Manual Deployment

1. Build the project:
```bash
npm run build
```

2. The `dist` folder contains the production-ready files
3. Serve the `dist` folder using any static file server (nginx, Apache, etc.)

## Troubleshooting

### Map not displaying
- Ensure Leaflet CSS is loaded (included in `index.html`)
- Check browser console for CORS errors
- Verify API is returning valid coordinate data

### API connection issues
- Verify backend API is running on port 8000
- Check CORS settings in backend
- Verify `VITE_API_BASE_URL` environment variable

### Authentication not working
- Clear browser localStorage
- Check browser console for errors
- Verify credentials match: `health@authority.gov` / `admin123`

## License

This project is part of the MLOps pipeline assignment.

