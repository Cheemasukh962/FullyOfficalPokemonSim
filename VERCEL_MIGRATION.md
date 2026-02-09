# Vercel Migration Guide

This document outlines the changes made to enable deployment on Vercel as an alternative to Railway.

## What Changed?

### 1. Configuration Files

#### `vercel.json` (Updated)
- **Before**: Commented out configuration
- **After**: Active configuration with:
  - Python runtime setup (`@vercel/python`)
  - API routing to `api/app.py`
  - Static file routing from `public/` directory
  - Production environment variables

#### `.vercelignore` (New)
- Created to exclude unnecessary files from Vercel deployment
- Excludes: Python cache, IDEs, local databases, tests, documentation source, Railway-specific files

### 2. Documentation Updates

#### `README.md`
- Added comprehensive Vercel deployment instructions
- Included both Railway and Vercel deployment options
- Added Vercel-specific troubleshooting section
- Updated stack description to mention both platforms

## Key Differences: Railway vs Vercel

| Aspect | Railway | Vercel |
|--------|---------|--------|
| **Runtime** | Long-running server (Gunicorn) | Serverless functions |
| **Configuration** | `Procfile` + `railway.json` | `vercel.json` |
| **Static Files** | Served by Flask | Served directly from `public/` |
| **Database** | Railway PostgreSQL | Vercel Postgres or external |
| **Deployment** | Git push triggers auto-deploy | Git push or `vercel --prod` |
| **Pricing** | $5/month starter | $20/month Pro (hobby free) |

## What Stays the Same?

1. **Application Code**: No changes needed to Python code
2. **Dependencies**: Same `requirements.txt`
3. **Database Setup**: Both use `DATABASE_URL` environment variable
4. **Frontend**: Same HTML/CSS/JS in `public/` directory
5. **API Endpoints**: Same routes and functionality

## Migration Steps

### From Railway to Vercel

1. **Export Data** (if needed):
   - Backup your Railway PostgreSQL database
   - Export as SQL dump if moving to new database

2. **Set up Vercel Project**:
   ```bash
   npm i -g vercel
   vercel login
   vercel link
   ```

3. **Configure Database**:
   - **Option A**: Add Vercel Postgres from dashboard
   - **Option B**: Keep Railway PostgreSQL (set `DATABASE_URL` in Vercel)
   - **Option C**: Use another provider (Neon, Supabase, etc.)

4. **Set Environment Variables** in Vercel:
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `FLASK_ENV`: `production`

5. **Deploy**:
   ```bash
   vercel --prod
   ```

6. **Test the Deployment**:
   - Visit your Vercel URL
   - Test API endpoints (`/api/pokemon/<name>`, `/api/battle`, `/api/stats`)
   - Verify database connectivity

### From Vercel to Railway

1. **Set up Railway Project**:
   - Create new project in Railway
   - Add PostgreSQL database

2. **Set Environment Variables**:
   - `DATABASE_URL`: Railway PostgreSQL connection string

3. **Connect GitHub Repository**:
   - Railway will detect `Procfile` and auto-deploy

4. **Test the Deployment**:
   - Visit your Railway URL
   - Test API endpoints

## Important Notes

### Serverless Considerations (Vercel)
- **Cold Starts**: First request after inactivity may be slower
- **Timeouts**: 10s limit on Hobby tier, 60s on Pro
- **Stateless**: Each request is independent
- **Database Connections**: Use connection pooling to avoid exhausting connections

### Performance Tips
- Keep dependencies minimal for faster cold starts
- Use database connection pooling
- Consider caching strategies for frequently accessed data
- Monitor function execution times

## Troubleshooting

### Vercel Build Fails
- Check Python version compatibility (Vercel supports Python 3.9-3.11)
- Verify all dependencies in `requirements.txt` are Vercel-compatible
- Check deployment logs in Vercel dashboard

### Database Connection Issues
- Verify `DATABASE_URL` format: `postgresql://user:pass@host:port/db`
- Check if database allows external connections
- Verify SSL settings if required by provider

### API Routes Not Working
- Ensure `vercel.json` routing configuration is correct
- Check function logs in Vercel dashboard
- Verify API paths match the routing rules

## Testing Locally

### Test Vercel Configuration Locally
```bash
# Install Vercel CLI
npm i -g vercel

# Run locally
vercel dev
```

This will simulate Vercel's serverless environment locally.

## Rollback Plan

If issues occur on Vercel, you can quickly rollback:

1. **Use Railway**: The existing `Procfile` and `railway.json` are still in place
2. **Previous Vercel Deployment**: Use Vercel dashboard to rollback to previous deployment
3. **Git Revert**: Revert commits if needed (though configuration changes are non-breaking)

## Support Resources

- **Vercel Python Docs**: https://vercel.com/docs/functions/serverless-functions/runtimes/python
- **Railway Docs**: https://docs.railway.app/
- **Flask on Vercel**: https://vercel.com/guides/deploying-flask-with-vercel

## Conclusion

The application is now configured to work on both Railway and Vercel. Choose the platform that best fits your needs:

- **Railway**: Better for traditional web apps, longer-running processes, simpler deployment
- **Vercel**: Better for serverless, global edge network, integrated with modern web workflows

No code changes are required - just configuration and deployment platform choice.
