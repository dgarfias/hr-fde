import time
import base64
from fastapi import APIRouter, Response, Request, HTTPException, status
import hmac
import hashlib
import time
import base64
from app.config import get_settings
from app.middleware.auth import _verify_session_cookie

settings = get_settings()
router = APIRouter(prefix="/api/auth")

def _sign_session() -> str:
    """Create a signed session token using the dashboard password as the HMAC key."""
    if not settings.dashboard_password:
        return ""
    payload = f"v1:{int(time.time())}"
    import hmac, hashlib
    sig = hmac.new(
        settings.dashboard_password.encode(),
        payload.encode(),
        hashlib.sha256,
    ).hexdigest()[:32]
    return base64.b64encode(f"{payload}:{sig}".encode()).decode()

@router.post("/login")
async def login(body: dict, response: Response):
    """Authenticate and set session cookie."""
    password = body.get("password", "")
    if not settings.dashboard_password:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Dashboard password not configured",
        )
    if not hmac.compare_digest(password, settings.dashboard_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
        )

    token = _sign_session()
    response.set_cookie(
        key="session",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=86400 * 7,
        path="/",
    )
    return {"status": "ok"}

@router.post("/logout")
async def logout(response: Response):
    """Clear session cookie."""
    response.delete_cookie(key="session", path="/")
    return {"status": "ok"}

@router.get("/me")
async def me(request: Request):
    """Check if user is authenticated."""
    token = request.cookies.get("session")
    if token and _verify_session_cookie(token):
        return {"authenticated": True}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
