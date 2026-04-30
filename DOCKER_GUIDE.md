# 🐳 Docker Deployment Guide

Complete guide to dockerize and deploy the Code Model Chat UI.

## 📋 Prerequisites

- Docker installed ([Download](https://www.docker.com/products/docker-desktop))
- Docker Compose installed (included with Docker Desktop)
- Git installed
- At least 2GB free disk space

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/tamiz-uddin/code-model.git
cd code-model
```

### 2. Build the Docker Image

```bash
docker build -t code-model-chat:latest .
```

### 3. Run the Container

```bash
docker run -p 5000:5000 code-model-chat:latest
```

### 4. Open in Browser

```
http://localhost:5000
```

## 🐳 Docker Compose (Recommended)

### 1. Start Services

```bash
docker-compose up -d
```

### 2. View Logs

```bash
docker-compose logs -f code-model-chat
```

### 3. Stop Services

```bash
docker-compose down
```

### 4. Rebuild Image

```bash
docker-compose up -d --build
```

## 📦 Docker Commands

### Build Image

```bash
# Build with default tag
docker build -t code-model-chat:latest .

# Build with version tag
docker build -t code-model-chat:v1.0 .

# Build with multiple tags
docker build -t code-model-chat:latest -t code-model-chat:v1.0 .
```

### Run Container

```bash
# Basic run
docker run -p 5000:5000 code-model-chat:latest

# Run with environment variables
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  code-model-chat:latest

# Run with volume mount
docker run -p 5000:5000 \
  -v $(pwd)/outputs:/app/outputs \
  code-model-chat:latest

# Run in background
docker run -d -p 5000:5000 \
  --name code-model-chat \
  code-model-chat:latest

# Run with resource limits
docker run -p 5000:5000 \
  --memory=2g \
  --cpus=2 \
  code-model-chat:latest
```

### Manage Containers

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# View container logs
docker logs code-model-chat

# Follow logs
docker logs -f code-model-chat

# Stop container
docker stop code-model-chat

# Start container
docker start code-model-chat

# Remove container
docker rm code-model-chat

# Execute command in container
docker exec -it code-model-chat bash

# View container stats
docker stats code-model-chat
```

### Manage Images

```bash
# List images
docker images

# Remove image
docker rmi code-model-chat:latest

# Tag image
docker tag code-model-chat:latest myregistry/code-model-chat:v1.0

# Push to registry
docker push myregistry/code-model-chat:v1.0

# Pull from registry
docker pull myregistry/code-model-chat:v1.0
```

## 🌐 Cloud Deployment

### AWS ECR

```bash
# Create ECR repository
aws ecr create-repository --repository-name code-model-chat

# Get login token
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  123456789.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag code-model-chat:latest \
  123456789.dkr.ecr.us-east-1.amazonaws.com/code-model-chat:latest

# Push to ECR
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/code-model-chat:latest

# Run on ECS
aws ecs run-task \
  --cluster default \
  --task-definition code-model-chat \
  --launch-type FARGATE
```

### Google Cloud Run

```bash
# Authenticate
gcloud auth login

# Set project
gcloud config set project PROJECT_ID

# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/code-model-chat

# Deploy
gcloud run deploy code-model-chat \
  --image gcr.io/PROJECT_ID/code-model-chat \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --cpu 2
```

### Azure Container Registry

```bash
# Create registry
az acr create --resource-group mygroup \
  --name myregistry --sku Basic

# Build and push
az acr build --registry myregistry \
  --image code-model-chat:latest .

# Deploy to Container Instances
az container create \
  --resource-group mygroup \
  --name code-model-chat \
  --image myregistry.azurecr.io/code-model-chat:latest \
  --cpu 2 --memory 2 \
  --ports 5000 \
  --registry-login-server myregistry.azurecr.io
```

### Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create code-model-chat

# Set stack
heroku stack:set container

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

## 🔧 Docker Compose Services

### Main Service: code-model-chat

```yaml
services:
  code-model-chat:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./outputs/models:/app/outputs/models:ro
      - ./templates:/app/templates:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## 📊 Performance Tuning

### Memory Optimization

```bash
# Limit memory to 2GB
docker run -p 5000:5000 \
  --memory=2g \
  code-model-chat:latest

# Limit memory and swap
docker run -p 5000:5000 \
  --memory=2g \
  --memory-swap=2g \
  code-model-chat:latest
```

### CPU Optimization

```bash
# Limit to 2 CPUs
docker run -p 5000:5000 \
  --cpus=2 \
  code-model-chat:latest

# Set CPU shares
docker run -p 5000:5000 \
  --cpu-shares=1024 \
  code-model-chat:latest
```

### Network Optimization

```bash
# Use host network (Linux only)
docker run -p 5000:5000 \
  --network host \
  code-model-chat:latest

# Set network bandwidth limit
docker run -p 5000:5000 \
  --network-opt "com.docker.network.driver.mtu=1500" \
  code-model-chat:latest
```

## 🔒 Security Best Practices

### 1. Use Non-Root User

```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

### 2. Read-Only Filesystem

```bash
docker run -p 5000:5000 \
  --read-only \
  --tmpfs /tmp \
  code-model-chat:latest
```

### 3. Drop Capabilities

```bash
docker run -p 5000:5000 \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  code-model-chat:latest
```

### 4. Use Secrets

```bash
# Create secret
echo "my-secret-value" | docker secret create my-secret -

# Use in compose
secrets:
  my-secret:
    external: true
```

### 5. Image Scanning

```bash
# Scan image for vulnerabilities
docker scan code-model-chat:latest

# Use Trivy
trivy image code-model-chat:latest
```

## 📈 Monitoring

### Docker Stats

```bash
# View real-time stats
docker stats code-model-chat

# View stats for all containers
docker stats
```

### Logging

```bash
# View logs
docker logs code-model-chat

# Follow logs
docker logs -f code-model-chat

# View last 100 lines
docker logs --tail 100 code-model-chat

# View logs with timestamps
docker logs -t code-model-chat

# View logs since specific time
docker logs --since 2024-04-30T10:00:00 code-model-chat
```

### Health Checks

```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' code-model-chat

# View health check logs
docker inspect --format='{{json .State.Health}}' code-model-chat | jq
```

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs code-model-chat

# Check container status
docker ps -a

# Inspect container
docker inspect code-model-chat

# Run with interactive shell
docker run -it code-model-chat bash
```

### Port Already in Use

```bash
# Find process using port
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port
docker run -p 5001:5000 code-model-chat:latest
```

### Out of Memory

```bash
# Check memory usage
docker stats code-model-chat

# Increase memory limit
docker run -p 5000:5000 \
  --memory=4g \
  code-model-chat:latest
```

### Slow Performance

```bash
# Check CPU usage
docker stats code-model-chat

# Increase CPU limit
docker run -p 5000:5000 \
  --cpus=4 \
  code-model-chat:latest

# Check disk I/O
docker stats --no-stream code-model-chat
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Security](https://docs.docker.com/engine/security/)

## 🎯 Next Steps

1. **Build the image:**
   ```bash
   docker build -t code-model-chat:latest .
   ```

2. **Run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

3. **Open in browser:**
   ```
   http://localhost:5000
   ```

4. **Deploy to cloud:**
   - AWS ECS
   - Google Cloud Run
   - Azure Container Instances
   - Heroku

---

**Happy containerizing! 🐳**
