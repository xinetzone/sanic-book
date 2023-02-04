import uuid
import decimal
import datetime
import strawberry
from strawberry.dataloader import DataLoader
from strawberry.schema.config import StrawberryConfig
from .snowflake import snowflake


@strawberry.type
class Device:
    device_id: int  # 设备ID，主键，雪花算法生成, 64bit长,
    device_sn: uuid.UUID  # 设备编号（唯一）
    device_name: str  # 设备名称
    device_description: str | None = strawberry.UNSET  # 设备描述
    device_creation_time: datetime.date  # 创建时间
    device_update_time: datetime.date  # 更新时间
    hardware_sn: str  # 硬件序列号
    hardware_model: str  # 硬件型号
    eth_mac: str | None = strawberry.UNSET  # 以太网卡MAC地址
    wifi_mac: str | None = strawberry.UNSET  # WiFi网卡MAC地址
    tle_imei: str  # LTE IMEI编码
    salt: str  # Salt，系统随机生成的一组字符串
    secret: str  # Secret， Passwor & Salt 散列, hash 使用 sha512
    software_infrastructure_version: str  # 基础程序版本号
    software_infrastructure_last_update:  datetime.date  # 基础程序上次更新时间
    software_infrastructure_state: str  # 基础程序状态
    software_business_version: str  # 业务程序版本号
    software_business_last_update: datetime.date  # 业务程序上次更新时间
    software_business_state: str  # 业务程序状态
    password: str


@strawberry.type
class Group:
    group_id: strawberry.ID  # 分组 ID (递增主键，雪花算法生成) snowflake()
    number: uuid.UUID  # 分组编号（唯一）
    name: uuid.UUID  # 分组名称（唯一）
    creation_time: datetime.date  # 创建时间
    update_time: datetime.date  # 更新时间
    device_number: int = 0  # 组内设备数
    description: str | None = strawberry.UNSET  # 组描述

# def get_group_for_code(root) -> "Author":
#     return Group(group_code)


@strawberry.input
class AddGroupInput:
    group_id: strawberry.ID  # 分组 ID (递增主键，雪花算法生成) snowflake()
    number: uuid.UUID  # 分组编号（唯一）
    name: uuid.UUID  # 分组名称（唯一）
    creation_time: datetime.date  # 创建时间
    update_time: datetime.date  # 更新时间
    device_number: int = 0  # 组内设备数
    description: str | None = strawberry.UNSET  # 组描述


group_codes = ["group1", "group2"]
device_groups = [Group(
    group_id=snowflake(),
    number=uuid.UUID('{00010203-0405-0607-0809-0a0b0c0d0e0f}'),
    name=uuid.uuid1(),
    creation_time=datetime.date.today(),
    update_time=datetime.date.today(),
    device_number=0
),
    Group(
        group_id=snowflake(),
        number=uuid.uuid4,
        name=uuid.UUID('{12345678-1234-5678-1234-567812345678}'),
        creation_time=datetime.date.today(),
        update_time=datetime.date.today(),
        device_number=1
)
]


def get_group_for_device(group_code: str) -> Group:
    return device_groups


@strawberry.type
class User:
    id: strawberry.ID


users_database = {
    1: User(1, "Nick"),
    2: User(2, "Tom"),
}

async def load_users(keys: list[int]) -> list[User | ValueError]:
    def lookup(key: int) -> User | ValueError:
        if user := users_database.get(key):
            return user
        return ValueError("not found")
    return [lookup(key) for key in keys]

loader = DataLoader(load_fn=load_users)


@strawberry.type
class Query:
    @strawberry.field
    async def get_user(self, id: strawberry.ID) -> User:
        return await loader.load(id)

    # users: list[User] = strawberry.field(resolver=user_loader.load)
    # groups: list[Group] = device_groups
    # group_code: Group = strawberry.field(resolver=get_group_for_device)
    @strawberry.field
    def hello(self) -> str:
        return "Hello"


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_group(self, name: str, number: str) -> Group:
        # print(f"Adding {title} by {author}")
        return AddGroupInput(group_id=snowflake(),
                             number=uuid.UUID(number),
                             name=uuid.UUID(name),
                             creation_time=datetime.date.today(),
                             update_time=datetime.date.today(),
                             device_number=0
                             )


schema = strawberry.Schema(query=Query, mutation=Mutation,
                           config=StrawberryConfig(auto_camel_case=False))
