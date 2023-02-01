(Queries)=
# 查询

在 GraphQL 中，使用查询从服务器获取数据。在 Strawberry 中，您可以通过定义查询类型来定义服务器提供的数据。

默认情况下，API 公开的所有字段都嵌套在 root 查询类型下。下面是在 Strawberry 中定义 root 查询类型的方法：

```python
@strawberry.type
class Query:
    name: str


schema = strawberry.Schema(query=Query)
```

这将创建模式，其中根类型 `Query` 只有名为 `name` 的字段。正如你所注意到的，没有提供获取数据的方法。为了做到这一点，需要提供 `resolver`，知道如何获取特定字段数据的函数。例如，在这种情况下，可以有函数总是返回相同的名称：

```python
def get_name() -> str:
    return "Strawberry"


@strawberry.type
class Query:
    name: str = strawberry.field(resolver=get_name)


schema = strawberry.Schema(query=Query)
```

所以现在，当请求 `name` 字段时，`get_name` 函数将被调用。
