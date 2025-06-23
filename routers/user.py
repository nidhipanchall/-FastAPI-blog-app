from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from passlib.context import CryptContext

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashed_password
    )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists or invalid data.")
    return new_user

@router.get("/", response_model=list[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {id} not found")
    return user

@router.put("/{id}", response_model=schemas.UserOut)
def update_user(id: int, request: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {id} not found")
    user.name = request.name
    user.email = request.email
    user.password = pwd_context.hash(request.password)  # Hash updated password
    try:
        db.commit()
        db.refresh(user)
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists or update failed.")
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {id} not found")
    db.delete(user)
    db.commit()
    return {"message": f"User with ID {id} deleted successfully"}
