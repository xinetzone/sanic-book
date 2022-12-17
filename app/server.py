import time
import asyncio
from sanic import Sanic, Request, HTTPResponse
from sanic.response import text
from _config import TomlConfig


class NanoSecondRequest(Request):
    @classmethod
    def generate_id(*_):
        return time.time_ns()

toml_config = TomlConfig(path="./configs/main.toml")
app = Sanic(toml_config.APP_NAME, config=toml_config)
app.config.FORWARDED_SECRET = "super-duper-secret"
app.config.REAL_IP_HEADER = "CF-Connecting-IP"
app.config.PROXIES_COUNT = 2


@app.get("/")
async def hello_world(request: Request) -> HTTPResponse:
    # return text("Hello, world.")
    print("IP: ", request.remote_addr)
    return text(f"{request.id}\n{request.remote_addr}")


if __name__ == "__main__":
    app.run(dev=True, host='0.0.0.0', port=8080)
