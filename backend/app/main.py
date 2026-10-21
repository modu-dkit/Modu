from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.orm import Session

from app.auth import (
    GoogleSignInRequest,
    TokenResponse,
    get_current_user,
    sign_in_with_google,
)
from app.db.models.user import User
from app.db.session import get_db


app = FastAPI(title="Modu API")
auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/google", response_model=TokenResponse)
def google_sign_in(
    request: GoogleSignInRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    return sign_in_with_google(request, db)


app.include_router(auth_router)


@app.get("/private")
def private_page(current_user: User = Depends(get_current_user)) -> dict[str, str]:
    return {
        "message": "This is a private page",
        "user_id": current_user.id,
    }
