(DataLoaders)=
# 数据记载器

Strawberry 内置了 DataLoader，这是通用的实用程序，可以通过批处理来减少对数据库或第三方 API 的请求数量
以及缓存请求。

```{note}
数据记载器提供了异步API，所以它们只在异步上下文中工作
```

请参阅官方 [DataLoaders 规范](https://github.com/graphql/dataloader) 以获得 DataLoaders 的高级指南。

## 基本用法

下面是如何使用 DataLoader，首先需要定义允许批量获取数据的函数。假设有一个用户类型，只有一个 id：

```python
import strawberry


@strawberry.type
class User:
    id: strawberry.ID
```

需要定义函数，根据传递的键列表返回用户列表：

```python
async def load_users(keys: list[int]) -> list[User]:
    return [User(id=key) for key in keys]
```

通常，这个函数将与数据库或第三方 API 交互，但对于我们的示例，不需要这样做。现在我们有了加载器函数，可以定义 DataLoader 并使用它：

```python
from strawberry.dataloader import DataLoader

loader = DataLoader(load_fn=load_users)

user = await loader.load(1)
```

这将导致调用 `load_users`，键值为 `[1]`。当你发出多个请求时，这个功能就会变得非常强大，就像下面这个例子：

```python
import asyncio

[user_a, user_b] = await asyncio.gather(loader.load(1), loader.load(2))
```

这将导致调用键值为 `[1, 2]` 的 `load_users`。因此，将对我们的数据库或第三方服务的调用数量减少到 1。

此外，默认情况下 DataLoader 会缓存负载，例如下面的代码：

```python
await loader.load(1)
await loader.load(1)
```

将导致只调用一次 `load_users`。

最后，有时想一次加载多个键。在这些情况下，可以使用 `load_many` 方法。

```python
[user_a, user_b, user_c] = await loader.load_many([1, 2, 3])
```

### 异常

与特定键相关的错误可以通过在返回列表的相应位置包含异常值来指示。此异常将由该键的 `load` 调用引发。使用上面相同的 `User` 类：

```python
from strawberry.dataloader import DataLoader

users_database = {
    1: User(id=1),
    2: User(id=2),
}


async def load_users(keys: list[int]) -> list[User | ValueError]:
    def lookup(key: int) -> User | ValueError:
        if user := users_database.get(key):
            return user
        return ValueError("not found")
    return [lookup(key) for key in keys]


loader = DataLoader(load_fn=load_users)
```

对于这个加载器，像 `await loader.load(1)` 这样的调用将返回 `User(id=1)`，而 `await loader.load(3)` 将引发 `ValueError("not found")`。

对于每个不正确的键，`load_users` 函数在列表中返回异常值是很重要的。使用 `keys == [1, 3]` 的调用返回 `[User(id=1), ValueError("not found")]`，并且不会直接引发 `ValueError`。如果 `load_users` 函数引发异常，即使是带有其他有效键的加载，如 `await loader.load(1)`，也会引发异常。

### 覆盖缓存键

缺省情况下，该输入作为缓存键。在上面的例子中，缓存键总是标量(int, float, string 等)，并且唯一地解析输入的数据。

在实际应用中，有时需要组合字段来惟一地标识数据。通过向 `DataLoader` 提供 `cache_key_fn` 参数，可以改变生成 key 的行为。当对象是键并且两个对象应该被认为是等价的时候，它也很有用。函数定义接受输入参数并返回 `Hashable` 类型。

```python
from strawberry.dataloader import DataLoader


class User:
    def __init__(self, custom_id: int, name: str):
        self.id: int = custom_id
        self.name: str = name


async def loader_fn(keys):
    return keys


def custom_cache_key(key):
    return key.id


loader = DataLoader(load_fn=loader_fn, cache_key_fn=custom_cache_key)
data1 = await loader.load(User(1, "Nick"))
data2 = await loader.load(User(1, "Nick"))
assert data1 == data2  # returns true
```

`loader.load(User(1, "Nick"))` 将在内部调用 `custom_cache_key`，将对象作为参数传递给函数，函数将返回 `User.id` 为键值 `1`。第二个调用将检查缓存中 `custom_cache_key` 返回的键，并从加载器缓存中返回缓存对象。

该实现依赖于用户在生成缓存键时处理冲突。如果发生冲突，将覆盖该键的数据。

### 缓存失效

默认情况下，dataloader 使用内部缓存。这对性能很有好处，但是当数据被修改(即变更)时，它可能会导致问题，因为缓存的数据不再有效！😮

要修复它，你可以显式地使缓存中的数据无效，使用以下方法之一：

- 使用 `loader.clear(id)` 指定 key，
- 使用 `loader.clear_many([id1, id2, id3, ...])` 指定多个 key，
- 使用 `loader.clear_all()` 使整个缓存失效。

### 将数据导入缓存

虽然数据加载器功能强大且高效，但它们不支持复杂的查询。

如果你的应用需要它们，你可能会混合使用数据加载器和直接数据库调用。

在这些场景中，将从外部检索到的数据导入到数据加载器中是很有用的，以避免之后重新加载数据。

例如：

```python
@strawberry.type
class Person:
    id: strawberry.ID
    friends_ids: strawberry.Private[List[strawberry.ID]]

    @strawberry.field
    async def friends(self) -> List[Person]:
      return await loader.load_many(self.friends_ids)

@strawberry.type
class Query:
    @strawberry.field
    async def get_all_people(self) -> List[User]:
        # Fetch all people from the database, without going through the dataloader abstraction
        people = await database.get_all_people()

        # Insert the people we fetched in the dataloader cache
        # Since "all people" are now in the cache, accessing `Person.friends` will not
        # trigger any extra database access
        loader.prime_many({person.id: person for person in people})

        return people
```
```
{
  getAllPeople {
    id
    friends {
      id
    }
  }
}
```

### 自定义缓存

DataLoader 默认缓存每个请求的，它在内存中缓存数据。对于所有用例，此策略可能不是最佳的或安全的。例如，如果您在分布式环境中使用 DataLoader，则可能希望使用分布式缓存。DataLoader 让你覆盖自定义缓存逻辑，它可以从其他持久缓存(例如 Redis )获取数据。

`DataLoader` 提供了参数 `cache_map`。它接受实现抽象接口 `AbstractCache` 的类的实例。接口方法有 `get`、`set`、`delete` 和 `clear`。

如果同时提供了 `cache_map` 参数，则 `cache_map` 参数将覆盖 `cache_key_fn` 参数。

```python
from typing import Any

import strawberry
from strawberry.types import Info
from strawberry.asgi import GraphQL
from strawberry.dataloader import DataLoader, AbstractCache

from starlette.requests import Request
from starlette.websockets import WebSocket
from starlette.responses import Response


class UserCache(AbstractCache):
    def __init__(self):
        self.cache = {}

    def get(self, key: Any) -> Any| None:
        return self.cache.get(key)  # fetch data from persistent cache

    def set(self, key: Any, value: Any) -> None:
        self.cache[key] = value  # store data in the cache

    def delete(self, key: Any) -> None:
        del self.cache[key]  # delete key from the cache

    def clear(self) -> None:
        self.cache.clear()  # clear the cache


@strawberry.type
class User:
    id: strawberry.ID
    name: str


async def load_users(keys) -> list[User]:
    return [User(id=key, name="Jane Doe") for key in keys]


class MyGraphQL(GraphQL):
    async def get_context(
        self, request: Request | WebSocket, response: Response|None
    ) -> Any:
        return {"user_loader": DataLoader(load_fn=load_users, cache_map=UserCache())}


@strawberry.type
class Query:
    @strawberry.field
    async def get_user(self, info: Info, id: strawberry.ID) -> User:
        return await info.context["user_loader"].load(id)


schema = strawberry.Schema(query=Query)
app = MyGraphQL(schema, graphiql=True)
```

## 使用 GraphQL

看一个如何在 GraphQL 中使用 DataLoaders 的例子：

```python
from strawberry.dataloader import DataLoader
import strawberry


@strawberry.type
class User:
    id: strawberry.ID


async def load_users(keys) -> list[User]:
    return [User(id=key) for key in keys]


loader = DataLoader(load_fn=load_users)


@strawberry.type
class Query:
    @strawberry.field
    async def get_user(self, id: strawberry.ID) -> User:
        return await loader.load(id)


schema = strawberry.Schema(query=Query)
```

这里定义了与前面相同的加载器，以及允许按 id 获取单个用户的 GraphQL 查询。可以通过执行以下请求来使用这个查询：

```{eval-rst}
.. graphiql::
  :query:
    {
      first: getUser(id: 1) {
          id
      }
      second: getUser(id: 2) {
          id
      }
    }
  :response:
    {
      "data": {
          "first": {
          "id": 1
          },
          "second": {
          "id": 2
          }
      }
    }
```

即使这个查询正在获取两个用户，它仍然会导致对 `load_users` 的一次调用。

## 上下文用法 context

正如您在上面的代码中所看到的，数据加载器是在解析器之外实例化的，因为需要在多个解析器之间甚至在多个解析器调用之间共享它。但是，当在服务器内部使用模式时，不推荐使用这种模式，因为只要服务器在运行，数据加载器就会缓存结果。

相反，一种常见的模式是在创建 GraphQL 上下文时创建数据加载器，这样它只缓存带有单个请求的结果。

使用 ASGI 视图的例子：

```python
from typing import Any

import strawberry
from strawberry.types import Info
from strawberry.asgi import GraphQL
from strawberry.dataloader import DataLoader

from starlette.requests import Request
from starlette.websockets import WebSocket
from starlette.responses import Response


@strawberry.type
class User:
    id: strawberry.ID


async def load_users(keys) -> list[User]:
    return [User(id=key) for key in keys]


class MyGraphQL(GraphQL):
    async def get_context(
        self, request: Request| WebSocket, response: Response|None
    ) -> Any:
        return {"user_loader": DataLoader(load_fn=load_users)}


@strawberry.type
class Query:
    @strawberry.field
    async def get_user(self, info: Info, id: strawberry.ID) -> User:
        return await info.context["user_loader"].load(id)


schema = strawberry.Schema(query=Query)
app = MyGraphQL(schema)
```

你现在可以在任何 ASGI 服务器上运行上面的例子，你可以阅读 [ASGI](../integrations/asgi.md) 来获得关于如何运行应用程序的更多细节。如果你选择 `uvicorn`，你可以安装它

```bash
pip install uvicorn
```

假设把上面的文件命名为 `schema.py`，那么：

```
uvicorn schema:app
```
