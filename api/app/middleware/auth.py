from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import get_settings
import hmac
import hashlib
import base64

settings = get_settings()
security = HTTPBearer(auto_error=False)
SESSION_VERSION = "v1"

def _verify_session_cookie(token: str) -> bool:
    """Verify the session cookie hasn't been tampered with."""
    if not settings.dashboard_password:
        return False
    try:
        decoded = base64.b64decode(token).decode()
        payload, sig = decoded.rsplit(":", 1)
        expected_sig = hmac.new(
            settings.dashboard_password.encode(),
            payload.encode(),
            hashlib.sha256,
        ).hexdigest()[:32]
        return hmac.compare_digest(sig, expected_sig)
    except Exception:
        return False

async def api_key_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = credentials.credentials
    if token != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API key",
        )
    return token

# Dashboard cookie-based auth
async def dashboard_auth(request: Request):
    if not settings.dashboard_password:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Dashboard password not configured",
        )

    token = request.cookies.get("session")
    if not token or not _verify_session_cookie(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"Set-Cookie": "session=; Max-Age=0; Path=/; HttpOnly"},
        )
    return True
