from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from database.connection import get_session
from models.users import NewUser, User, UserSignIn

user_router = APIRouter(tags=["users"])


@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_new_user(
    data: NewUser,
    session: Session = Depends(get_session),
) -> dict:
    existing_user = session.exec(
        select(User).where(User.email == data.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied email exists",
        )
    user = User(
        email=data.email,
        password=data.password,
        events=[event.model_dump() for event in data.events or []],
    )
    session.add(user)
    session.commit()
    return {"message": "User successfully registered!"}


@user_router.post("/signin")
async def sign_user_in(
    data: UserSignIn,
    session: Session = Depends(get_session),
) -> dict:
    user = session.exec(
        select(User).where(User.email == data.email)
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
        )
    if user.password != data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong credentials passed",
        )
    return {"message": "User signed in successfully"}
