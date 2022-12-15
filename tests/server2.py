from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, text, html
import aiofiles
# import asyncio
# import uvloop
# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# 创建 Sanic 实例对象, Sanic 是 web 服务的入口类, 它等价于 flask.Flask
# 然后里面传递字符串作为应用的名字
app = Sanic("my_awesome_server")
# app.config 是 Config 对象, 可以存储相应的配置, 有以下几种加载方式
app.config.user_name = "xinetzone"  # 通过属性查找的方式设置


@app.get("/")
async def hello_world(request: Request) -> HTTPResponse:
    lst = []
    lst.append(f"请求的url: {request.url}")
    lst.append(f"请求的path: {request.path}")
    lst.append(f"请求的方法: {request.method}")
    lst.append(f"请求的查询参数: {request.query_args}")
    lst.append(f"请求的查询参数: {request.args}")
    lst.append(f"a: {request.args.get('a')}, "
               f"b: {request.args.get('b')}, "
               f"a_lst: {request.args.getlist('a')}, "
               f"c: {request.args.get('c')}, "
               f"c: {request.args.get('c', 'xxx')}")
    return text("\n".join(lst))

@app.reload_process_start
async def reload_start(*_):
    print(">>>>>> reload_start <<<<<<")


@app.main_process_start
async def main_start(*_):
    print(">>>>>> main_start <<<<<<")


app.register_listener(reload_start, "before_server_start")


if __name__ == "__main__":
    app.run(dev=True)
