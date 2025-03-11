from fastapi import APIRouter, Depends, HTTPException, Header
from database.database import get_db
from src.schemas.user import (
    Register_User_Schema,
    Login_User_Schema,
    ResetPasswordSchema,
)
from src.models.user import User, OTP
import uuid
from src.utils.user import (
    get_token,
    decode_token,
    pwd_context,
    pass_checker,
    find_same_email,
    send_email,
)
from sqlalchemy.orm import Session
from src.utils.user import gen_otp

user_router = APIRouter()


@user_router.post("/Register")
def register(user: Register_User_Schema, db: Session = Depends(get_db)):
    new_user = User(
        id=str(uuid.uuid4()),
        username=user.username,
        email=user.email,
        password=pwd_context.hash(user.password),
    )

    find_one_entry = db.query(User).first()
    if find_one_entry:
        find_same_email(user.email)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return "User registered successfully"


@user_router.post("/generate_otp")
def generate_otp(email: str):
    gen_otp(email)
    return "OTP generated successfully"


@user_router.get("/verify_otp")
def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):
    # breakpoint()
    find_user = db.query(User).filter(User.email == email).first()

    if not find_user:
        raise HTTPException(status_code=400, detail="User not found")

    find_otp = db.query(OTP).filter(OTP.email == email, OTP.otp == otp).first()

    if not find_otp:
        raise HTTPException(status_code=400, detail="OTP not found")

    db.delete(find_otp)
    db.commit()
    db.refresh(find_user)
    return "OTP verified successfully"


@user_router.post("/Login")
def login(user: Login_User_Schema, db: Session = Depends(get_db)):
    find_user = db.query(User).filter(User.email == user.email).first()

    if not find_user:
        raise HTTPException(status_code=400, detail="User not found")

    pass_checker(user.password, find_user.password)

    access_token = get_token(find_user.id, find_user.email)
    return access_token, "Login successfully"


@user_router.patch("/reset_password")
def reset_password(
    user: ResetPasswordSchema, token: str = Header(...), db: Session = Depends(get_db)
):
    user_detail = decode_token(token)
    id, email = user_detail

    find_user = db.query(User).filter(User.email == email).first()

    if not find_user:
        raise HTTPException(status_code=400, detail="User not found")

    pass_checker(user.old_password, find_user.password)

    if user.new_password == user.confirm_password:
        setattr(find_user, "password", user.confirm_password)
    else:
        raise HTTPException(
            status_code=400, detail="new password and confirm password does not match"
        )

    find_user.password = pwd_context.hash(user.confirm_password)

    send_email(
        find_user.email, "Reset Password mail", "Your password successfully reset"
    )

    db.commit()
    db.refresh(find_user)
    return "password reset successfully"


@user_router.delete("/delete_user")
def delete_user(email: str, password: str, db: Session = Depends(get_db)):
    find_user = (
        db.query(User).filter(User.email == email, User.password == password).first()
    )

    if not find_user:
        raise HTTPException(status_code=400, detail="user not found")

    db.delete(find_user)
    db.commit()
    return "user deleted successfully"
