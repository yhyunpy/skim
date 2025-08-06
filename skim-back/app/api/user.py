from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, Request
import shortuuid as suid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_google_user_info,
)
from app.database import get_sess
from app.models.user import Token, UserRes
from app.schemas.user import User

ROUTER = APIRouter()


async def create_user(sess: AsyncSession, google_user: dict):
    google_id = google_user.get("id")
    name = google_user.get("name")

    # 기존 회원 조회
    q = await sess.execute(
        select(User).where(User.auth_key == google_id, User.auth == "google")
    )
    user = q.scalars().first()

    if user:
        return user

    # 회원가입
    new_user = User(
        id=suid.uuid(),
        auth_key=google_id,
        auth="google",
        name=name,
        hashed_password=None,
    )
    sess.add(new_user)
    await sess.commit()
    await sess.refresh(new_user)
    return new_user


@ROUTER.get("/login")
async def get_login(
    code: str = Query(...),
    sess: AsyncSession = Depends(get_sess),
):
    """
    1. 프론트에서 Google 로그인 -> authorization code 발급
    2. Google이 프론트 oauth/callback 으로 사용자를 리디렉션 -> 프론트에서 백 /users/login 호출
    3. Google OAuth 서버에 요청 -> Google access_token 획득
    4. Google access_token으로 사용자 정보 조회
    5. 사용자 정보로 skim DB에서 회원 조회 또는 회원 생성
    6. skim JWT 발급
    """
    try:
        google_user_info = await get_google_user_info(code)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Google code")

    user = await create_user(sess, google_user_info)

    token_data = {"sub": user.id}

    return Token(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
    )


@ROUTER.get("/me", response_model=UserRes)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
