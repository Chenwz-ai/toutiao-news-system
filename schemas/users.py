from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRegister(BaseModel):
    username:str
    password:str

class UserLogin(BaseModel):
    username:str
    password:str

class UserInfoBase(BaseModel):
    """
    ⽤户信息基础数据模型
    """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个⼈简介")


#user_info对应的类
class UserInfoResponse(UserInfoBase):
    id: int
    username: str
    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True
    )


#data 数据类型
class UserAuthResponse(BaseModel):
     token:str
     user_info:UserInfoResponse = Field(...,alias="userInfo")

     #模型类配置
     model_config = ConfigDict(
         populate_by_name=True,
         from_attributes= True
     )


#更新用户信息
class UserUpdateRequest(BaseModel):
    nickname:str = None
    avatar:str = None
    gender:str = None
    bio:str = None
    phone:str = None


class UserChangePasswordRequest(BaseModel):
    old_password:str = Field(...,description="旧密码",alias="oldPassword")
    new_password:str = Field(...,description="新密码",alias="newPassword",min_length=6)