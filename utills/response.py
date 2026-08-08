from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def success_response(message: str = "success",data=None):
    content = {"code":200,"message":message,"data":data}
    #把任何FastAPI, Pydantic,ORM对象转换成JSON
    return JSONResponse(content=jsonable_encoder(content))
