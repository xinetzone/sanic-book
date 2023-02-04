import uuid
import decimal
import datetime
from typing import Any
import strawberry
from strawberry.sanic.views import GraphQLView as _GraphQLView
from strawberry.types import Info
from strawberry.dataloader import DataLoader
from strawberry.http.temporal_response import TemporalResponse
from strawberry.schema.config import StrawberryConfig
from sanic.request import Request
from .snowflake import snowflake


@strawberry.type
class User:
    id: strawberry.ID

users_database = {
    "1": User(id=1),
    "2": User(id=2),
}

async def load_users(keys: list[strawberry.ID]) -> list[User | ValueError]:
    def lookup(key: strawberry.ID) -> User | ValueError:
        if user := users_database.get(key):
            print(user)
            return user
        return ValueError("not found")
    return [lookup(key) for key in keys]

class GraphQLView(_GraphQLView):
    async def get_context(self, request: Request, response: TemporalResponse) -> Any:
        return {"user_loader": DataLoader(load_fn=load_users)}

@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: strawberry.ID, info: Info) -> User:
        print(f"ID: {id}, {type(id)}")
        return await info.context["user_loader"].load(id)

schema = strawberry.Schema(query=Query, #mutation=Mutation,
                           config=StrawberryConfig(auto_camel_case=False))