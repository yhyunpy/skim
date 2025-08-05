import os
from datetime import datetime, timedelta

import httpx
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config import (
    ALGORITHM,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
    SECRET_KEY,
)
from app.database import get_sess
from app.schemas import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7


async def get_google_user_info(code: str):
    async with httpx.AsyncClient() as client:
        # Google OAuth 서버에 요청 → access_token 획득
        token_res = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token_res.raise_for_status()
        token_json = token_res.json()
        access_token = token_json.get("access_token")

        # access_token으로 사용자 정보 조회
        user_res = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_res.raise_for_status()
        return user_res.json()


def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_access_token(data: dict):
    return create_token(data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))


def create_refresh_token(data: dict):
    return create_token(data, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))


def verify_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(
    token: str = Depends(oauth2_scheme), sess: AsyncSession = Depends(get_sess)
):
    payload = verify_access_token(token)
    user_id = payload["sub"]
    q = await sess.execute(select(User).where(User.id == user_id))
    user = q.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
