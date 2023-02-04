# ./my_blueprint.py
from sanic.response import json
from sanic import Blueprint
from sanic.request import Request

bp = Blueprint("groups")

@bp.post("/groups/<number:int>")
async def handler1(request: Request, number: int):
    return {    
    "name":"分组名称",
    "description":"关于分组的描述",
    "creation time":"当前时间",
    "update time":"当前时间",
    "device number": 0                   
}

@bp.get("/groups/<group_code:str>")
async def handler2(request: Request, group_code: str):
    return {       
        "group code": "code" ,           
        "group name":"name",
        "description":"关于分组的描述",
        "creation time":"创建时间",
        "update time":"最新修改时间",
        "device number":"10"
    }
    
