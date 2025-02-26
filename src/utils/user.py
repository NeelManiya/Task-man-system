from config import ALGORITHM, SECRET_KEY
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from src.models.user import User
from database.database import SessionLocal
import uuid
from src.models.user import OTP
import random

db = SessionLocal()


def get_token(id: str, email: str):
    try:
        payload = {
            "id": id,
            "email": email,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=10),
        }
        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=500, detail="internal server error")


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id = payload.get("id")
        email = payload.get("email")

        if not id or not email:
            raise HTTPException(status_code=403, detail="invalid token")
        return id, email

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")


from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def pass_checker(user_pass, hash_pass):
    if pwd_context.verify(user_pass, hash_pass):
        return True
    else:
        raise HTTPException(status_code=401, detail="Password is incorrect")


def find_same_email(email: str):
    find_same_email = db.query(User).filter(User.email == email).first()

    if find_same_email:
        raise HTTPException(
            status_code=400, detail="Email already exists try different email"
        )


def gen_otp(email):
    find_user = db.query(User).filter(User.email == email).first()

    if not find_user:
        raise HTTPException(status_code=400, detail="User not found")

    random_otp = random.randint(1000, 9999)

    # store OTP in the database
    new_otp = OTP(
        id=str(uuid.uuid4()),
        email=find_user.email,
        user_id=find_user.id,
        otp=random_otp,
    )

    print(random_otp)

    send_email(find_user.email, "Login Email", f"your OTP is {random_otp}")

    db.add(new_otp)
    db.commit()
    db.refresh(new_otp)
    return "OTP generated successfully"


import smtplib
from config import SENDER_EMAIL, EMAIL_PASSWORD
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(receiver, subject, body):
    smt_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = SENDER_EMAIL
    smtp_password = EMAIL_PASSWORD

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # try:
    with smtplib.SMTP(smt_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(SENDER_EMAIL, receiver, msg.as_string())
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail="Email sending fail")
