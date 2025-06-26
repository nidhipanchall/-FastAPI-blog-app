from fastapi import FastAPI
from routers import blog, user, auth
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Blog App",
    description="A simple blog API with user management and JWT authentication.",
    version="1.0.0"
)

app.include_router(user.router)
app.include_router(blog.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Blog!"}
