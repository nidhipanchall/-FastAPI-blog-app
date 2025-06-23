from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)

@router.get("/", response_model=list[schemas.BlogOut])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.get("/{id}", response_model=schemas.BlogOut)
def get_blog_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with ID {id} not found")
    return blog

@router.post("/", response_model=schemas.BlogOut, status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.BlogCreate, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.put("/{id}", response_model=schemas.BlogOut)
def update_blog(id: int, request: schemas.BlogCreate, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with ID {id} not found")
    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return blog

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with ID {id} not found")
    db.delete(blog)
    db.commit()
    return {"message": f"Blog with ID {id} deleted successfully"}
