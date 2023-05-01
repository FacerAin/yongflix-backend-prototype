from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from database.connection import Database
from models.users import TokenResponse, User

router = APIRouter(tags=["User"])
database = Database(User)
hash_password = HashPassword()


@router.post("/signup")
async def signup_user(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User Already exists."
        )
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    await database.save(user)
    return {"message": "User successfully registered."}


@router.post("/signin", response_model=TokenResponse)
async def signin_user(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_exist = await User.find_one(User.email == user.username)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User does not exist."
        )

    if hash_password.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.email)
        return {"access_token": access_token, "token_type": "Bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong credentials passed"
    )
