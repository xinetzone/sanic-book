from sanic.response import html, text, json
from sanic import Blueprint

info = Blueprint("info", url_prefix="/info")

@info.route("/")
async def bp_root(request):
    return text(info.name)
