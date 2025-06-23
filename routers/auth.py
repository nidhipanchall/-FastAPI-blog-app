from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr

SECRET_KEY = "supersecretkey"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password)


@router.post("/register")
def register(request: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(models.User).filter(models.User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(request.password)
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User created successfully"}


@router.post("/login")
def login(request: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer"
    }



# {
#     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzUwNjc4MzMyfQ.lqcihOGfJBMcUND7-XpRnPdTpKqHyncUSYBIhYGF05Y",
#     "token_type": "bearer"
# }