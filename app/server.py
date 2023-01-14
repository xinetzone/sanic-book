import time
from sanic import Sanic, Request, HTTPResponse
from sanic.response import html, text
from _config import TomlConfig

class NanoSecondRequest(Request):
    @classmethod
    def generate_id(*_):
        return time.time_ns()


toml_config = TomlConfig(path="./configs/main.toml")
app = Sanic(toml_config.APP_NAME, config=toml_config)
@app.get("/")
async def foo_handler(request):
    return text("I said foo!")
