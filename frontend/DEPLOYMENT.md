# Deployment Instructions

This document provides step-by-step instructions for deploying the Health & Air Quality Dashboard frontend.

## Prerequisites

1. **Backend API Running**: Ensure the FastAPI backend is running and accessible
2. **Node.js 18+**: Required for building the frontend
3. **Build Tools**: npm or yarn

## Local Development Setup

1. **Install Dependencies**:
```bash
cd frontend
npm install
```

2. **Start Development Server**:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Production Build

1. **Build the Application**:
```bash
npm run build
```

This creates an optimized production build in the `dist` folder.

2. **Preview Production Build**:
```bash
npm run preview
```

## Deployment Options

### Option 1: Vercel (Recommended)

Vercel provides excellent React support with automatic deployments.

1. **Install Vercel CLI**:
```bash
npm i -g vercel
```

2. **Login to Vercel**:
```bash
vercel login
```

3. **Deploy**:
```bash
cd frontend
vercel
```

4. **Configure Environment Variables**:
   - Go to Vercel Dashboard → Your Project → Settings → Environment Variables
   - Add: `VITE_API_BASE_URL` = `https://your-api-url.com`

5. **Redeploy** after adding environment variables

### Option 2: Netlify

1. **Install Netlify CLI**:
```bash
npm i -g netlify-cli
```

2. **Login**:
```bash
netlify login
```

3. **Build and Deploy**:
```bash
cd frontend
npm run build
netlify deploy --prod --dir=dist
```

4. **Configure Environment Variables**:
   - Go to Netlify Dashboard → Site Settings → Environment Variables
   - Add: `VITE_API_BASE_URL` = `https://your-api-url.com`

5. **Redeploy** after adding environment variables

### Option 3: GitHub Pages

1. **Install gh-pages**:
```bash
npm install --save-dev gh-pages
```

2. **Update package.json**:
```json
{
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d dist"
  },
  "homepage": "https://yourusername.github.io/health-dashboard"
}
```

3. **Deploy**:
```bash
npm run deploy
```

**Note**: For GitHub Pages, you'll need to update the API base URL to use absolute URLs.

### Option 4: Traditional Web Server (Nginx, Apache, etc.)

1. **Build the application**:
```bash
npm run build
```

2. **Copy dist folder** to your web server directory:
   - Nginx: `/var/www/html/health-dashboard`
   - Apache: `/var/www/html/health-dashboard`

3. **Configure Nginx** (example):
```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /var/www/html/health-dashboard;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

4. **Set Environment Variables**:
   - Create a `.env.production` file or configure at build time:
```bash
VITE_API_BASE_URL=https://your-api-url.com npm run build
```

## Environment Variables

The frontend uses environment variables prefixed with `VITE_`. These are embedded at build time.

### Required Variables

- `VITE_API_BASE_URL`: Base URL of the backend API (default: `http://localhost:8000`)

### Setting Variables

**For Vercel/Netlify**: Set in the platform's dashboard

**For Build-time**: Create `.env.production`:
```
VITE_API_BASE_URL=https://api.yourdomain.com
```

Then build:
```bash
npm run build
```

## CORS Configuration

Ensure your backend API has CORS enabled for your frontend domain:

```python
# In FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Troubleshooting

### Build Errors

1. **Module not found**: Run `npm install` again
2. **Type errors**: Check Node.js version (requires 18+)
3. **Memory errors**: Increase Node memory: `NODE_OPTIONS=--max-old-space-size=4096 npm run build`

### Runtime Errors

1. **API connection failed**: 
   - Check `VITE_API_BASE_URL` is set correctly
   - Verify backend is running and accessible
   - Check CORS settings

2. **Map not loading**:
   - Verify Leaflet CSS is loaded
   - Check browser console for errors
   - Ensure API returns valid coordinate data

3. **Authentication issues**:
   - Clear browser localStorage
   - Check browser console for errors
   - Verify credentials: `health@authority.gov` / `admin123`

## Post-Deployment Checklist

- [ ] Environment variables configured
- [ ] Backend API accessible from frontend domain
- [ ] CORS configured on backend
- [ ] All routes working (dashboard, citizen, authority)
- [ ] Authentication working
- [ ] Maps loading correctly
- [ ] Charts displaying data
- [ ] API calls successful (check browser Network tab)

## Performance Optimization

1. **Enable Compression**: Configure gzip/brotli on your web server
2. **CDN**: Use a CDN for static assets
3. **Caching**: Set appropriate cache headers for static assets
4. **Code Splitting**: Already implemented via Vite

## Security Considerations

1. **HTTPS**: Always use HTTPS in production
2. **Environment Variables**: Never commit `.env` files
3. **API Keys**: If needed, store securely and never expose in frontend code
4. **CORS**: Restrict CORS to specific domains in production

## Support

For issues or questions, refer to:
- Frontend README: `frontend/README.md`
- API Documentation: `API_DOCUMENTATION.md`
- Main README: `readme.md`

