from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from .config import settings

bearer = HTTPBearer(auto_error=False)
ALGORITHM = "HS256"


def verify_admin(email: str, password: str) -> bool:
    return email == settings.admin_email and password == settings.admin_password


def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    expire_delta = timedelta(
        minutes=expires_minutes or settings.access_token_expire_minutes
    )
    expire = datetime.now(timezone.utc) + expire_delta
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.app_secret_key, algorithm=ALGORITHM)


def get_current_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> str:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token"
        )
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.app_secret_key, algorithms=[ALGORITHM])
        subject: str | None = payload.get("sub")
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from exc
    if subject != settings.admin_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin only endpoint"
        )
    return subject
