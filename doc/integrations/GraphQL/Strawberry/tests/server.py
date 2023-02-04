from sanic import Sanic
from api.schema import schema, GraphQLView

app = Sanic(__name__)


app.add_route(
    GraphQLView.as_view(schema=schema, graphiql=True),
    "/groups",
    version="v1.1"
)
