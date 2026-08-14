from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class NewsItemBase(BaseModel):
    id: int
    title: str
    description: Optional[ str] =  None
    image: Optional[str] = None
    author: Optional[str] = None
    category_id: Optional[int] = Field(alias="categoryId")
    views:int
    publish_time:Optional[datetime] = Field(None,alias="publishTime")

    model_config = ConfigDict(
        populate_by_name=True,  # 字段名兼容
        from_attributes= True   # 允许字段名从orm_model中获取
    )