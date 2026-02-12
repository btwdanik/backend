from datetime import datetime, timedelta, timezone
import jwt, os

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

def decode_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload