from sanic import Sanic
from sanic.response import text
from _config import TomlConfig

toml_config = TomlConfig(path="./configs/main.toml")
app = Sanic(toml_config.APP_NAME, config=toml_config)


@app.get("/")
async def hello_world(request):
    return text("Hello, world.")


if __name__ == "__main__":
    app.run(dev=True, host='0.0.0.0', port=8080)
