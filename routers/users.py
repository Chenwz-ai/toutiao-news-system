from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserRegister
from config.db_conf import get_db
from crud import users
from starlette import status
router = APIRouter(prefix="/api/user",tags=["users"])

@router.post("/register")
async def register(user_data:UserRegister,db:AsyncSession = Depends(get_db)):
    #注册逻辑:1.验证用户名是否已存在 2.创建用户 3.生成token 4.返回结果
    existing_user = await users.get_user_by_username(db,user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户名已存在")
    user = await users.create_user(db,user_data)
    token = await users.create_token(db,user.id)
    return {
        "code" : 200,
        "message" :"注册成功",
        "data" : {
            "token":token,
            "userInfo":{
                "id":user.id,
                "username":user.username,
                "bio":user.bio,
                "avatar":user.avatar
            }
        }
    }