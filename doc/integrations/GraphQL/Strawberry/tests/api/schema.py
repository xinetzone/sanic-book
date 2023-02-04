import uuid
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
class Group:
    group_id: strawberry.ID  # 分组 ID (递增主键，雪花算法生成) snowflake()
    number: strawberry.ID  # 分组编号（唯一）
    name: strawberry.ID  # 分组名称（唯一）
    creation_time: datetime.date  # 创建时间
    update_time: datetime.date  # 更新时间
    device_number: int = 0  # 组内设备数
    description: str | None = strawberry.UNSET  # 组描述


groups_database = {group_id: Group(group_id=group_id,
                                   number=number,
                                   name=name,
                                   creation_time=datetime.date.today(),
                                   update_time=datetime.date.today(),
                                   device_number=0)
                   for group_id, number, name in [("277218759112916992", uuid.UUID('{00010203-0405-0607-0809-0a0b0c0d0e0f}'), uuid.uuid1())]}


async def load_groups(keys: list[strawberry.ID]) -> list[Group | ValueError]:
    def lookup(key: strawberry.ID) -> Group | ValueError:
        if user := groups_database.get(key):
            print(user)
            return user
        return ValueError("not found")
    return [lookup(key) for key in keys]


class GraphQLView(_GraphQLView):
    async def get_context(self, request: Request, response: TemporalResponse) -> Any:
        return {"device_loader": DataLoader(load_fn=load_groups)}


@strawberry.type
class Query:
    @strawberry.field
    async def group(self, group_id: strawberry.ID, info: Info) -> Group:
        print(f"ID: {id}, {type(id)}")
        return await info.context["device_loader"].load(group_id)

    @strawberry.field
    async def groups(self, info: Info) -> list[Group]:
        return [await info.context["device_loader"].load(group_id) for group_id in groups_database.keys()]


@strawberry.input
class AddGroupInput:
    group_id: strawberry.ID  # 分组 ID (递增主键，雪花算法生成) snowflake()
    number: strawberry.ID  # 分组编号（唯一）
    name: strawberry.ID  # 分组名称（唯一）
    creation_time: datetime.date  # 创建时间
    update_time: datetime.date  # 更新时间
    device_number: int = 0  # 组内设备数
    description: str | None = strawberry.UNSET  # 组描述


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_group(self, group_id: strawberry.ID, name: str, number: str) -> Group:
        g = AddGroupInput(group_id=snowflake(),
                          number=uuid.UUID(number),
                          name=uuid.UUID(name),
                          creation_time=datetime.date.today(),
                          update_time=datetime.date.today(),
                          device_number=0
                          )
        groups_database[group_id] = g
        return g

    @strawberry.mutation
    def delete_group(self, group_id: strawberry.ID) -> int:
        groups_database.pop(group_id)
        return 204

    @strawberry.mutation
    def change_update_time(self, group_id: strawberry.ID, update_time: datetime.date) -> Group:
        g = groups_database.get(group_id)
        g.update_time = update_time
        return g

    @strawberry.mutation
    def change_device_number(self, group_id: strawberry.ID, device_number: int) -> Group:
        g = groups_database.get(group_id)
        g.device_number = device_number
        return g


schema = strawberry.Schema(query=Query, mutation=Mutation,
                           config=StrawberryConfig(auto_camel_case=False))
