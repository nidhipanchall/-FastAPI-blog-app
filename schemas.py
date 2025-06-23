from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True  


class BlogBase(BaseModel):
    title: str
    body: str

class BlogCreate(BlogBase):
    pass

class BlogOut(BlogBase):
    id: int

    class Config:
        from_attributes = True  
