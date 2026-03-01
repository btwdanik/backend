from datetime import datetime, timedelta, timezone
import jwt, os
from starlette.responses import JSONResponse
from fastapi import status

from api.pydantic.user.models import UserSchemaAccessToken, UserSchemaRefreshToken
from dotenv import load_dotenv

load_dotenv()
ACCESS_TTL_MIN = int(os.getenv("ACCESS_TTL_MIN"))
ACCESS_TTL_DAYS = int(os.getenv("ACCESS_TTL_DAYS")) * 24
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(schema: UserSchemaAccessToken) -> str:
    payload = {
        "id": schema.id,
        "sub": schema.sub,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TTL_MIN),
        "iat": datetime.now(timezone.utc),
        "type": "access_token",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(schema: UserSchemaRefreshToken) -> str:
    payload = {
        "sub": schema.sub,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TTL_DAYS),
        "iat": datetime.now(timezone.utc),
        "type": "refresh_token",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict | JSONResponse:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="Token expired")
    except jwt.InvalidTokenError:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="Invalid token")