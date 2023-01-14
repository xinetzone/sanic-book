import time
from string import Template
from sanic import Sanic, Request, HTTPResponse
# from sanic.log import logger
from sanic.response import html, text
from _config import TomlConfig
from auth import protected
from login import login


class NanoSecondRequest(Request):
    @classmethod
    def generate_id(*_):
        return time.time_ns()


toml_config = TomlConfig(path="./configs/main.toml")
app = Sanic(toml_config.APP_NAME, config=toml_config)
app.blueprint(login)
app.static("/static", "./_static")


@app.route("/<tag:strorempty>")
async def page(request: Request, tag: str) -> HTTPResponse:
    # return text("Hello, world.")
    # logger.info(f"logging {request.id}\n{request.remote_addr}")
    # return text(f"{request.id}\n{request.remote_addr}")
    root = "configs/index" if tag == "" else f"configs/{tag}"
    print("tag: ", tag)
    with open("templates/demo.html", encoding="utf-8") as fp:
        context = fp.read()
    with open(f"{root}/article.html", encoding="utf-8") as fp:
        article = fp.read()
    with open(f"{root}/aside.html", encoding="utf-8") as fp:
        aside = fp.read()
    return html(Template(context).substitute(article=article, aside=aside))


@app.get("/secret")
@protected
async def secret(request):
    """暂处于试验阶段"""
    return text("To go fast, you must be fast.")


@app.post("/form-post")
async def forms(request: Request) -> HTTPResponse:
   return text("DDD")

if __name__ == "__main__":
    app.run(dev=True, host='0.0.0.0', port=8080)
