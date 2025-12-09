# Deploying agentkit Amazing to Vercel

This guide explains how to deploy your ChatKit application (agentkit Amazing) to Vercel.

## Prerequisites

1. A [Vercel account](https://vercel.com/signup)
2. [Vercel CLI](https://vercel.com/docs/cli) installed (optional, for command-line deployment)
3. OpenAI API key with ChatKit access
4. ChatKit workflow ID from your OpenAI account

## Environment Variables

You need to configure the following environment variables in Vercel:

### Required Variables

- **OPENAI_API_KEY**: Your OpenAI API key (starts with `sk-proj-...`)
  - Get this from: https://platform.openai.com/api-keys

- **CHATKIT_WORKFLOW_ID**: Your ChatKit workflow ID (starts with `wf_...`)
  - Create a workflow at: https://platform.openai.com/chatkit/workflows

### Optional Variables

- **ENVIRONMENT**: Set to `production` (automatically set in vercel.json)
- **CHATKIT_API_BASE**: Override the default OpenAI API base URL if needed (default: `https://api.openai.com`)

## Deployment Methods

### Method 1: Deploy via Vercel Dashboard (Recommended)

1. **Connect Your Repository**
   - Go to https://vercel.com/new
   - Import your Git repository
   - Select the repository containing this project

2. **Configure Project Settings**
   - **Framework Preset**: Other
   - **Root Directory**: Leave as `./` (root)
   - **Build Command**: `npm run vercel-build`
   - **Output Directory**: `managed-chatkit/frontend/dist`
   - **Install Command**: `npm install`

3. **Add Environment Variables**
   - Go to your project settings → Environment Variables
   - Add the required variables listed above
   - Make sure to add them for all environments (Production, Preview, Development)

4. **Deploy**
   - Click "Deploy"
   - Wait for the build to complete
   - Your app will be live at `https://your-project.vercel.app`

### Method 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   # For production deployment
   vercel --prod

   # For preview deployment
   vercel
   ```

4. **Set Environment Variables**
   ```bash
   vercel env add OPENAI_API_KEY production
   vercel env add CHATKIT_WORKFLOW_ID production
   ```

## Project Structure

This is a monorepo containing:

- **Frontend**: React + Vite application (`managed-chatkit/frontend/`)
  - Built with Vite
  - Uses @openai/chatkit-react
  - Outputs to `dist/` directory

- **Backend**: FastAPI Python application (`managed-chatkit/backend/`)
  - Handles session creation for ChatKit
  - Proxies requests to OpenAI's ChatKit API
  - Deployed as serverless functions

## Vercel Configuration

The project includes a `vercel.json` file that configures:

- Static frontend build from Vite
- Python serverless functions for the backend API
- Routing rules to direct `/api/*` requests to the backend
- Environment variable references

## Testing Your Deployment

After deployment:

1. Visit your Vercel URL
2. The ChatKit interface should load
3. Try sending a message to test the workflow integration
4. Check Vercel Function Logs if you encounter any issues

## Troubleshooting

### Build Fails

- Verify Node.js version is 18.18 or higher
- Check that all dependencies are correctly listed in package.json
- Review build logs in Vercel dashboard

### API Errors

- Verify environment variables are set correctly
- Check that your OPENAI_API_KEY has ChatKit access
- Verify the CHATKIT_WORKFLOW_ID is valid and published
- Review Function Logs in Vercel dashboard

### CORS Issues

- The backend is configured to allow all origins in development
- For production, you may want to restrict this in `managed-chatkit/backend/app/main.py`

## Custom Domain

To add a custom domain:

1. Go to your project in Vercel dashboard
2. Navigate to Settings → Domains
3. Add your custom domain
4. Follow DNS configuration instructions

## Continuous Deployment

Once connected to Git:

- Push to your main branch → Auto-deploys to production
- Push to other branches → Creates preview deployments
- Pull requests → Automatic preview deployments with unique URLs

## Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [OpenAI ChatKit Documentation](https://platform.openai.com/docs/guides/chatkit)
- [Vite Deployment Guide](https://vitejs.dev/guide/static-deploy.html#vercel)
