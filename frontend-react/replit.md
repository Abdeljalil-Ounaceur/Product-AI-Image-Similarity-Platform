# Product Similarity Frontend React App

## Overview
This is a React single-page application (SPA) for product similarity search. Users can upload an image and the app will display similar images based on visual similarity.

**Current State**: The application is fully functional in standalone mode with mock data. It can also integrate with a backend API when available.

**Last Updated**: November 4, 2025

## Recent Changes
- **Nov 4, 2025 (Latest)**: Complete UI refactoring to "Visual Similarity Explorer"
  - Implemented modern dark theme with Tailwind CSS (via CDN)
  - Added Framer Motion for smooth animations and transitions
  - Created new components: Header, Footer, ResultsGrid, ResultCard
  - Redesigned UploadSection with drag-and-drop functionality
  - Added 4 clickable sample images for quick demo
  - Implemented confidence messaging based on similarity scores
  - Added responsive grid layout (3 cols desktop, 2 tablet, 1 mobile)
  - Created modal for system architecture diagram
  - Preserved backend API integration with fallback to mock data
  
- **Nov 4, 2025**: Initial setup in Replit environment
  - Configured React app to run on port 5000 (required for Replit)
  - Set up host configuration to work with Replit's proxy (0.0.0.0 binding)
  - Enabled host check bypass for iframe-based preview
  - Installed all npm dependencies
  - Created workflow for React Frontend

## Project Architecture

### Technology Stack
- **Frontend Framework**: React 19.2.0
- **Build Tool**: Create React App (react-scripts 5.0.1)
- **Styling**: Tailwind CSS 3.3.0 (via CDN)
- **Animations**: Framer Motion 3.x
- **Testing**: Jest with React Testing Library
- **Fonts**: Inter (Google Fonts)

### Directory Structure
```
/
├── public/              # Static assets
│   ├── mock-images/    # Sample images for testing
│   └── index.html      # HTML template
├── src/
│   ├── components/     # React components
│   │   ├── Header.jsx          # App header with architecture modal
│   │   ├── Footer.jsx          # App footer with credits
│   │   ├── UploadSection.jsx   # Drag-and-drop upload with samples
│   │   ├── ResultsGrid.jsx     # Grid layout for results
│   │   ├── ResultCard.jsx      # Individual result card with animations
│   │   ├── ImageItem.jsx       # (Legacy) Individual image display
│   │   └── ImageList.jsx       # (Legacy) List of similar images
│   ├── services/       # API integration
│   │   ├── api.js      # Real backend API calls
│   │   └── mockApi.js  # Mock data for standalone testing
│   ├── styles/         # Component-specific CSS
│   ├── App.js          # Main application component
│   └── index.js        # Entry point
└── package.json        # Dependencies and scripts
```

### Key Features
1. **Modern UI**: Dark theme with gradient backgrounds and smooth animations
2. **Drag-and-Drop Upload**: Intuitive file upload with drag-and-drop support
3. **Sample Images**: 4 clickable sample images for quick demo (Dada, Studio Ghibli, Anime, Cinematic)
4. **Confidence Messaging**: Dynamic UI states based on similarity scores:
   - Success (≥75% similarity): Shows positive message with metrics
   - Warning (60-75%): Alerts user about potential out-of-catalog images
   - Poor (<60%): Shows empty state with helpful message
5. **Responsive Grid**: Results display in 3/2/1 columns (desktop/tablet/mobile)
6. **Hover Effects**: Image cards zoom and show "View Details" on hover
7. **Similarity Scores**: Visual progress bars and percentage badges
8. **Architecture Modal**: View system architecture diagram from header
9. **API Integration**: Real backend API with fallback to mock data
10. **Reupload Flow**: Users can upload multiple images via "Try Another Image"

### API Integration
The app uses environment variable `REACT_APP_API_URL` to configure the backend API endpoint:
- Default: `http://localhost:8000`
- API endpoints:
  - `POST /api/upload` - Upload image for processing
  - `GET /api/similar/{imageId}` - Get similar images

To switch between mock and real API:
- Mock mode: Uncomment line 5 in `src/App.js`
- Real API mode: Uncomment line 4 in `src/App.js` (current setting)

## Configuration

### Environment Variables
- `PORT=5000` - Frontend port (required for Replit webview)
- `HOST=0.0.0.0` - Bind to all interfaces
- `DANGEROUSLY_DISABLE_HOST_CHECK=true` - Required for Replit proxy
- `WDS_SOCKET_PORT=0` - WebSocket configuration for HMR
- `DISABLE_ESLINT_PLUGIN=true` - Disables ESLint to avoid es-abstract compatibility issues

### Available Scripts
- `npm start` - Runs the development server on port 5000
- `npm run build` - Creates production build
- `npm test` - Runs test suite

## Workflow
**React Frontend**: Runs `npm start` on port 5000 with webview output

## Deployment Notes
This frontend can be deployed as a static site after running `npm run build`. The build output will be in the `/build` directory.

## User Preferences
None specified yet.

## To-Do
- ✅ Polish the frontend with a better UI and more meaningful look
- ✅ Add loading states and animations
- Consider adding error boundary components
- Replace Tailwind CDN with PostCSS build for production
- Add unit tests for new components
- Implement keyboard navigation for accessibility
- Add image preview modal on result card click
