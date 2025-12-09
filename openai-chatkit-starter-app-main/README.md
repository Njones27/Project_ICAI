# agentkit Amazing

A ChatKit-powered conversational AI application built with OpenAI's managed ChatKit integration.

## Project Overview

This application provides a production-ready ChatKit interface with a React frontend and FastAPI backend, configured for easy deployment to Vercel.

## Quick Start

### Local Development

1. Install dependencies:
   ```bash
   npm install
   cd managed-chatkit/frontend && npm install
   ```

2. Configure environment variables:
   ```bash
   cp managed-chatkit/.env.example managed-chatkit/.env
   ```

   Edit `managed-chatkit/.env` and add:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `NEXT_PUBLIC_CHATKIT_WORKFLOW_ID`: Your ChatKit workflow ID

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Deployment

See [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for detailed deployment instructions to Vercel.

## Project Structure

- [**managed-chatkit**](managed-chatkit) – Main application with hosted ChatKit workflows
  - `frontend/` - React + Vite frontend
  - `backend/` - FastAPI Python backend
- [**chatkit**](chatkit) - Alternative self-hosted ChatKit integration example
