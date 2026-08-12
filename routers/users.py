from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from schemas.users import UserRegister, UserAuthResponse, UserInfoResponse, UserLogin, UserUpdateRequest, \
    UserChangePasswordRequest
from config.db_conf import get_db
from crud import users
from starlette import status

from utills.response import success_response
from utills.auth import get_current_user

router = APIRouter(prefix="/api/user",tags=["users"])

@router.post("/register")
async def register(user_data:UserRegister,db:AsyncSession = Depends(get_db)):
    #注册逻辑:1.验证用户名是否已存在 2.创建用户 3.生成token 4.返回结果
    existing_user = await users.get_user_by_username(db,user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户名已存在")
    user = await users.create_user(db,user_data)
    token = await users.create_token(db,user.id)
    # return {
    #     "code" : 200,
    #     "message" :"注册成功",
    #     "data" : {
    #         "token":token,
    #         "userInfo":{
    #             "id":user.id,
    #             "username":user.username,
    #             "bio":user.bio,
    #             "avatar":user.avatar
    #         }
    #     }
    # }
    response_data = UserAuthResponse(token=token,userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功",data=response_data)

@router.post("/login")
async def login(user_data:UserLogin,db:AsyncSession = Depends(get_db)):
    # 登录逻辑:1.验证用户名密码 2.生成token 3.返回结果
    user = await users.authenticate_user(db,user_data.username,user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户名或密码错误")
    token = await users.create_token(db,user.id)
    response_data = UserAuthResponse(token=token,userInfo=UserInfoResponse.model_validate(user))


    return success_response(message="登录成功",data=response_data)

@router.get("/info")
async def get_user_info(user:User = Depends(get_current_user)):
    #1. 查token查用户,2.封装crud,3.功能整合成一个工具函数,4.路由导入使用:依赖注入的方式
    return success_response(message="获取用户信息成功",data=UserInfoResponse.model_validate(user))

@router.put("/update")
async def update_user_info(user_data:UserUpdateRequest,user:User = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
    #1. 查token查用户,2.更新(用户提交数据put提交->请求体参数->定义pydantic模型类)3.响应结果
    user = await users.update_user(db,user.username,user_data)
    return success_response(message="更新用户信息成功",data=UserInfoResponse.model_validate(user))

@router.put("/password")
async def update_password(password_data:UserChangePasswordRequest,
                          user:User = Depends(get_current_user),
                          db:AsyncSession = Depends(get_db)):
    res_change_password = await users.change_password(db,user,password_data.old_password,password_data.new_password)
    if not res_change_password:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="修改密码失败")
    return success_response(message="修改密码成功")


