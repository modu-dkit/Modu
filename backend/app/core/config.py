import os

from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./modu.db")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def require_auth_configuration() -> None:
    missing = [
        name
        for name, value in (
            ("GOOGLE_CLIENT_ID", GOOGLE_CLIENT_ID),
            ("JWT_SECRET_KEY", JWT_SECRET_KEY),
        )
        if not value
    ]
    if missing:
        raise RuntimeError(
            f"Missing required authentication settings: {', '.join(missing)}"
        )
