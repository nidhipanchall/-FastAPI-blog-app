from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserLogin
from auth import create_access_token

router = APIRouter(
    tags=["Auth"]
)

@router.post("/login")
def login(request: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email, User.password == request.password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}
