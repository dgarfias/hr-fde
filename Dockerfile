# Multi-stage build for unified monorepo deployment
# Stage 1: Build the React dashboard
FROM node:20-alpine AS dashboard-builder

WORKDIR /app/dashboard
COPY dashboard/package.json dashboard/package-lock.json* ./
RUN npm install
COPY dashboard/ .
RUN npm run build

# Stage 2: Build the Python API with dashboard static files baked in
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for psycopg2/asyncpg
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy API source code
COPY api/app ./app

# Copy built dashboard from Stage 1 into a location the API can serve
COPY --from=dashboard-builder /app/dashboard/dist ./dashboard/dist

# Set environment defaults (override with fly secrets or docker-compose env)
ENV DATABASE_URL=""
ENV API_KEY=""
ENV FMCSA_API_URL="https://mobile.fmcsa.dot.gov/qc/services/carriers/"
ENV FMCSA_API_KEY=""
ENV CORS_ORIGINS="*"
ENV LOG_LEVEL="info"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
