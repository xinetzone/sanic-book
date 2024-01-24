import time
from uuid import UUID
from sanic import Sanic, Request, HTTPResponse
from sanic.response import html, text, json
from utils.config import TomlConfig
from api import api


class NanoSecondRequest(Request):
    @classmethod
    def generate_id(*_):
        return time.time_ns()

# =================== 配置 ======================================
toml_config = TomlConfig(path="./configs/main.toml") # 定义配置
app = Sanic(toml_config.APP_NAME, config=toml_config) # 注册应用

# =================== 蓝图 ======================================
app.blueprint(api) # 注册蓝图

# =================== 应用 ======================================
@app.get("/")
async def foo_handler(request: Request) -> HTTPResponse:
    return json({"foo": "bar"})

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8888, debug=True, dev=True)
    app.run(host='localhost', port=8888, debug=True, dev=True)
