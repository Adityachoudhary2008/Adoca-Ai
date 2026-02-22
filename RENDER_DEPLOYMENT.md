# 🚀 Render Deployment Guide

Complete guide to deploy Adoca AI to [Render](https://render.com) - a simple, modern cloud platform.

## ✅ Pre-deployment Checklist

- [x] Application is production-ready
- [x] Dockerfile is optimized (multi-stage build)
- [x] render.yaml configuration file created
- [x] Environment variables configured
- [x] GitHub repository is public
- [ ] Sarvam AI API key ready
- [ ] GitHub account connected to Render

## 📝 Step 1: Prepare Render Account

### 1.1 Create Render Account
1. Go to https://render.com
2. Sign up with GitHub (recommended for easier integration)
3. Authorize Render to access your GitHub repositories

### 1.2 Add Environment Variable
1. Go to Render Dashboard
2. Settings → Environment Variables
3. Add your Sarvam AI API key (we'll add it to the service)

## 🔗 Step 2: Connect GitHub Repository

1. On Render dashboard, click **"New +"** button
2. Select **"Web Service"**
3. Click **"Connect Repository"**
4. Search and select: `Adoryachoudhary2008/Adoca-Ai`
5. Click **"Connect"**

## ⚙️ Step 3: Configure Web Service

### 3.1 Basic Settings

| Setting | Value |
|---------|-------|
| **Name** | `adoca-ai` |
| **Environment** | `Docker` |
| **Region** | Choose closest to your users (e.g., Oregon, Singapore) |
| **Branch** | `main` |
| **Auto-deploy** | ✓ Enable (auto-deploy on push) |

### 3.2 Dockerfile & Build

| Setting | Value |
|---------|-------|
| **Dockerfile Path** | `./Dockerfile` |
| **Docker Context** | `./` |
| **Build Command** | `npm --prefix frontend ci && npm --prefix frontend run build` |

### 3.3 Instance Type

For production:
- **Render Pro**: $7/month (recommended)
- **Render Plus**: $12/month (for higher traffic)

For testing:
- **Free Tier**: 0.5 CPU, 512 MB RAM (limited to 750 hours/month)

## 🔐 Step 4: Add Environment Variables

**In the Render service configuration, add:**

```env
SARVAM_API_KEY=sk_your_actual_key_here
APP_ENV=production
LOG_LEVEL=INFO
MAX_RESPONSE_LENGTH=1000
MIN_CONTEXT_CHUNKS=2
MAX_CONTEXT_CHUNKS=5
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600
```

⚠️ **Important**: Use Render's secret management for `SARVAM_API_KEY`:
1. Go to service settings → **Environment Variables**
2. Click **Add Secret**
3. Key: `SARVAM_API_KEY`
4. Value: Your actual Sarvam API key
5. This will be encrypted and never exposed

## 🚀 Step 5: Deploy

### Option A: Deploy via render.yaml (Recommended)

1. On GitHub, create `.render.json` or use `render.yaml`
2. Push to main branch:
   ```bash
   git add render.yaml
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```
3. On Render dashboard, click **"Deploy latest commit"**
4. Watch the build logs in real-time

### Option B: Manual Deploy

1. Click **"Create Web Service"** button
2. Configure settings as above
3. Click **"Create Web Service"**
4. Render automatically builds and deploys

### Option C: Deploy from CLI

```bash
# Install Render CLI
npm install -g @render-oss/cli

# Login
render login

# Deploy
render create web-service \
  --name adoca-ai \
  --repo https://github.com/Adityachoudhary2008/Adoca-Ai \
  --branch main \
  --dockerfile-path ./Dockerfile \
  --instance-type starter
```

## 📊 Step 6: Monitor Deployment

1. **Build Logs**: View in real-time in Render dashboard
2. **Health Check**: Render automatically checks `/health` endpoint
3. **Live URL**: Get your live URL from dashboard (e.g., `https://adoca-ai.onrender.com`)
4. **Metrics**: Dashboard shows CPU, memory, requests/sec

### Common Build Issues

| Issue | Solution |
|-------|----------|
| **npm ERR! 404** | Ensure frontend has valid package.json |
| **ENOSPC: no space** | Increase build time in settings |
| **Python deps failed** | Check requirements.txt syntax |
| **Port already in use** | Render sets PORT env var automatically |

## 🔍 Step 7: Verify Deployment

Once deployed, test your endpoints:

```bash
# Health check
curl https://adoca-ai.onrender.com/health

# API docs
https://adoca-ai.onrender.com/api/docs

# Chat interface
https://adoca-ai.onrender.com

# Query endpoint
curl -X POST https://adoca-ai.onrender.com/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is Adoca?",
    "user_id": "render-test"
  }'
```

### Expected Response

```json
{
  "query": "What is Adoca?",
  "response": "Adoca is a conversational commerce platform...",
  "intent": "info",
  "context_chunks": 2,
  "latency_ms": 215,
  "status": "success",
  "timestamp": "2026-02-22T10:30:00"
}
```

## 🔄 Continuous Deployment

After initial deployment:

1. **Auto-deploy**: Any push to `main` automatically deploys
2. **Preview Deploys**: Create preview environment for pull requests
3. **Rollback**: Click "Rollback" in Render dashboard if needed
4. **Environment-specific**: Create separate services for dev/staging/prod

### Multiple Environments

```bash
# Production
main branch → https://adoca-ai.onrender.com

# Staging
staging branch → https://adoca-ai-staging.onrender.com

# Development
dev branch → https://adoca-ai-dev.onrender.com
```

## 💰 Costs

### Render Pricing

| Plan | CPU | RAM | Cost | Use Case |
|------|-----|-----|------|----------|
| **Free** | 0.5 | 512 MB | $0 | Testing (750 hrs/mo) |
| **Starter** | 0.5 | 512 MB | $7/mo | Small apps |
| **Standard** | 1 | 2 GB | $25/mo | Production |
| **Plus** | 2 | 4 GB | $50/mo | High traffic |

**Monthly estimate for production:** ~$7-25 (way cheaper than AWS/GCP!)

## 📈 Scaling

### Auto-scaling (Render Pro+)
```yaml
minInstances: 1
maxInstances: 3  # Auto-scale up to 3 instances
cpuThreshold: 80  # Scale up if CPU > 80%
memoryThreshold: 85  # Scale up if memory > 85%
```

## 🔒 Security Best Practices

1. **Secrets Management**
   - Use Render's encrypted secrets, not .env files
   - Rotate API keys monthly
   - Never commit secrets to GitHub

2. **HTTPS**
   - Render provides automatic SSL/TLS
   - All traffic forced to HTTPS

3. **Firewall**
   - Render includes basic DDoS protection
   - Add IP allowlist if needed

4. **Environment Isolation**
   - Separate services for dev/staging/prod
   - Different API keys per environment

## 🆘 Troubleshooting

### Service won't start
```
❌ Error: Port already in use
✅ Solution: Delete old service first, Render assigns unique ports
```

### Build timeout
```
❌ Error: Build exceeded 45 minutes
✅ Solution: 
  - Optimize Docker build layers
  - Use .dockerignore to exclude large files
  - Check build logs for slow steps
```

### Frontend not loading
```
❌ Error: 404 on /
✅ Solution:
  - Verify frontend/dist exists after build
  - Check build command completed successfully
  - Inspect Render build logs
```

### API key not working
```
❌ Error: Authentication failed
✅ Solution:
  - Verify SARVAM_API_KEY is set in Render secrets
  - Check key format and expiration
  - Get new key from Sarvam dashboard
```

### Database connection error
```
❌ Error: Cannot connect to database
✅ Solution:
  - For SQLite: Data persists in /app/data/
  - For PostgreSQL: Create Render Postgres service
  - Update DATABASE_PATH env var
```

## 📞 Support & Debugging

### View Logs

```bash
# Stream logs in real-time
curl https://api.render.com/v1/services/{SERVICE_ID}/logs \
  -H "Authorization: Bearer $RENDER_API_KEY"

# Or in Render dashboard: Service → Logs tab
```

### Health Monitoring

Render automatically monitors:
- CPU usage
- Memory usage
- Request latency
- Error rates
- Build success/failure

### Get Help

- 📖 [Render Documentation](https://render.com/docs)
- 💬 [Render Discord Community](https://discord.gg/render)
- 🐛 [GitHub Issues](https://github.com/Adityachoudhary2008/Adoca-Ai/issues)

## ✨ Advanced Configuration

### Custom Domain

1. In Render dashboard → Service Settings → Custom Domain
2. Add your domain: `adoca-ai.yourcompany.com`
3. Update DNS CNAME to: `adoca-ai.onrender.com`
4. Wait for DNS propagation (5-48 hours)

### Background Jobs

```python
# Add Celery for background tasks
# Edit requirements.txt to add: celery, redis

# Then create background worker:
# render.yaml - Add worker service
- type: background_worker
  name: adoca-ai-worker
  dockerfile: Dockerfile.worker
```

### Database Integration

```yaml
# Add PostgreSQL service in render.yaml
- type: pserv
  name: adoca-ai-db
  plan: starter
  database: adoca_production
```

## 🎉 You're Live!

Your Adoca AI is now running on Render! 

**Your live URL**: `https://adoca-ai.onrender.com`

Share it with your team:
- Frontend: https://adoca-ai.onrender.com
- API Docs: https://adoca-ai.onrender.com/api/docs
- Analytics: https://adoca-ai.onrender.com/analytics

---

**Questions?** Check the [Render docs](https://render.com/docs) or create a GitHub issue!

**Version**: 1.0.0 | **Last Updated**: 2026-02-22
