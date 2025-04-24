# MathViz AI - Mathematical Concept Visualizer

A chatbot-style web application that explains mathematical concepts with visualizations using AI.

## Features

- Chat interface for submitting math-related queries
- AI-generated explanations of mathematical concepts
- Visual demonstrations using Manim-generated videos
- Responsive design for all device sizes
- Audio narration synchronized with visuals

## Technology Stack

- **Frontend**: React, TypeScript, Tailwind CSS
- **Backend**: Flask (Python)
- **AI**: Placeholders for Gemini and CodeGen models
- **Visualization**: Manim (Mathematical Animation Engine)
- **Audio**: gTTS (Google Text-to-Speech) and MoviePy

## Getting Started

### Prerequisites

- Node.js 16+
- Python 3.8+
- FFmpeg (optional, for video generation)

### Installation

1. Clone the repository
2. Install frontend dependencies:
   ```bash
   npm install
   ```
3. Install backend dependencies:
   ```bash
   cd api
   pip install -r requirements.txt
   ```

### Running the Application

Start both frontend and backend with one command:
```bash
npm run start
```

Or run them separately:
- Frontend: `npm run dev`
- Backend: `cd api && flask run --debug`

## Development Notes

- The current implementation uses placeholder responses for AI-generated content
- For production use, you would need to implement actual API calls to models like Gemini
- The Manim execution is simulated; real implementation would require Manim installed

## Project Structure

- `/src` - React frontend
- `/api` - Flask backend
  - `/api/utils` - Backend utilities for model integration, video processing
  - `/api/static` - Generated content (videos, code)