from string import Template
from sanic import Sanic, Request, HTTPResponse
from sanic.response import html, text
from _config import TomlConfig

# 获取注册表
toml_config = TomlConfig(path="./configs/main.toml")
app = Sanic.get_app(toml_config.APP_NAME)

