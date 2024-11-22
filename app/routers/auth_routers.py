from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate, User
from app.schemas.token_schemas import Token
from app.crud.user_crud import create_user, get_user_by_username
from app.core.security import verify_password, create_access_token
from app.db.session import get_db

router = APIRouter()

# Login endpoint to get the token
@router.post("/login", response_model=Token, include_in_schema=False)
# use fastapi.security OAuth2PasswordRequestForm to make fastapi/swagger auth work
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_in_db = get_user_by_username(db, username=form_data.username)
    if not user_in_db or not verify_password(form_data.password, user_in_db.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# # Login endpoint to get the token (without using OAuth2PasswordRequestForm)
# @router.post("/login", response_model=Token)
# def login(user: UserCreate, db: Session = Depends(get_db)):
#     user_in_db = get_user_by_username(db, username=user.username)
#     if not user_in_db or not verify_password(user.password, user_in_db.hashed_password):
#         raise HTTPException(status_code=400, detail="Invalid credentials")

#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}

# Register new user endpoint
@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = create_user(db, user)
    return new_user