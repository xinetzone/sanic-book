from strawberry.sanic.views import GraphQLView
from sanic import Sanic

from api.schema import schema
 
app = Sanic(__name__)


app.add_route(
    GraphQLView.as_view(schema=schema, graphiql=True),
    "/devices",
)
