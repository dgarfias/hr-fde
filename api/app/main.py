from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import logging
import os

from app.config import get_settings
from app.database import engine, Base
from app.middleware.auth import api_key_auth

from app.routers import health, loads, fmcsa, dashboard_api, auth, call_records

settings = get_settings()
logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger(__name__)

app = FastAPI(
    title="HappyRobot Inbound Carrier Sales API",
    description="Backend API for load search, FMCSA verification, offer logging, and metrics.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    logger.info("Starting up...")

    if not settings.dashboard_password:
        logger.error("DASHBOARD_PASSWORD environment variable is required but not set. Dashboard cannot start.")
        raise RuntimeError("DASHBOARD_PASSWORD is required. Set it in your .env file or environment.")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created/verified.")

@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutting down...")
    await engine.dispose()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# Public health endpoint
app.include_router(health.router, tags=["Health"])

# Protected routes (voice agent tools)
app.include_router(loads.router, prefix="/loads", tags=["Loads"], dependencies=[Depends(api_key_auth)])
app.include_router(fmcsa.router, prefix="/fmcsa", tags=["FMCSA"], dependencies=[Depends(api_key_auth)])

# Unified call record endpoint — workflow sends all data here at end of call
app.include_router(call_records.router, tags=["Call Records"])

# Dashboard-facing routes (password protected)
app.include_router(auth.router, tags=["Auth"])
app.include_router(dashboard_api.router, tags=["Dashboard"])
# Proxy removed — dashboard no longer calls HappyRobot API directly

# Serve dashboard static files (production only; try multiple paths)
_possible_static_dirs = [
    os.path.join(os.path.dirname(__file__), "..", "..", "dashboard", "dist"),   # local dev from repo root
    os.path.join(os.path.dirname(__file__), "..", "dashboard", "dist"),          # inside docker /app
    "/dashboard/dist",                                                            # docker-compose volume mount
]
static_dir = None
for d in _possible_static_dirs:
    if os.path.isdir(d):
        static_dir = d
        break

if static_dir:
    # Register SPA routes BEFORE static files so they take precedence
    @app.get("/")
    @app.get("/calls")
    @app.get("/calls/{call_id:path}")
    async def serve_dashboard(request: Request):
        return FileResponse(os.path.join(static_dir, "index.html"))

    # Mount static files for assets (js, css, images)
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
    logger.info(f"Serving dashboard from {static_dir}")
else:
    logger.warning("Dashboard dist/ not found; API-only mode.")
