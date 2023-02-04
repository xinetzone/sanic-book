(Resolvers)=
# 解析器
在定义 GraphQL 模式时，通常从 API 的模式定义开始，例如，看一下这个模式：

::::{card-carousel} 2
:::{card} Python
```python
import strawberry

@strawberry.type
class User:
    name: str


@strawberry.type
class Query:
    last_user: User
```
:::
:::{card} Schema
```
type User {
    name: String!
}

type Query {
    lastUser: User!
}
```
:::
::::


已经定义了 `User` 类型和 `Query` 类型。接下来，为了定义如何从服务器返回数据，将把解析器附加到字段。

## 定义解析器

让我们创建解析器，并将其附加到 `lastUser` 字段。解析器是返回数据的 Python 函数。在 Strawberry 中有两种定义解析器的方法；第一个是传递函数给字段定义，像这样：

```python
def get_last_user() -> User:
    return User(name="Marco")


@strawberry.type
class Query:
    last_user: User = strawberry.field(resolver=get_last_user)
```

现在当 Strawberry 执行下面的查询时，它将调用 `get_last_user` 函数来获取 `lastUser` 字段的数据：

```{eval-rst}
.. graphiql:: 
  :query:
    {
      lastUser {
        name
     }
    }
  :response:
    {
      "data": {
        "lastUser": {
        "name": "Marco"
      }
    }
   }
```

## 将解析器定义为方法

定义解析器的另一种方法是使用 `strawberry.field` 作为装饰器，像在这里：

```python
@strawberry.type
class Query:
    @strawberry.field
    def last_user(self) -> User:
        return User(name="Marco")
```

当您想要合并解析器和类型或当您有非常小的解析器。

```{note}
`self` 参数在这里有点特殊，当执行 GraphQL 查询时，在使用装饰器定义的解析器的情况下，`self` 参数对应于该字段的 `root` 值。在本例中，`root` 值是值 `Query` 类型，通常为 `None`。在 Schema 上调用 `execute` 方法时，可以更改 `root` 值。下面将详细介绍 `root` 值。
```

## 定义参数

字段也可以有参数；在 Strawberry 中，字段的参数是在解析器上定义的，就像在 Python 函数中通常做的那样。在 `Query` 中定义字段，按 `ID` 返回用户：

```python
import strawberry


@strawberry.type
class User:
    name: str


@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: strawberry.ID) -> User:
        # here you'd use the `id` to get the user from the database
        return User(name="Marco")
```
```
type User {
    name: String!
}

type Query {
    user(id: ID!): User!
}
```

### 可选参数

可选或可空参数可以用 {func}`~typing.Optional` 表示。如果你需要区分 `null`（在 Python 中映射为 `None`）和没有传入参数，你可以使用 `UNSET`：
::::{card-carousel} 2
:::{card} Python
:width: 100%
```python
import strawberry

@strawberry.type
class Query:
    @strawberry.field
    def hello(self, name: str|None = None) -> str:
        if name is None:
            return "Hello world!"
        return f"Hello {name}!"

    @strawberry.field
    def greet(self, name: str|None = strawberry.UNSET) -> str:
        if name is strawberry.UNSET:
            return "Name was not set!"
        if name is None:
            return "Name was null!"
        return f"Hello {name}!"
```
:::{card} Schema
:width: 75%
```
type Query {
    hello(name: String = null): String!
    greet(name: String): String!
}
```
:::
::::
这样你会得到：

```{eval-rst}
.. graphiql:: 
  :query:
    {
    unset: greet
    null: greet(name: null)
    name: greet(name: "Dominique")
    }
  :response:
    {
    "data": {
        "unset": "Name was not set!",
        "null": "Name was null!",
        "name": "Hello Dominique!"
    }
    }
```

## 访问字段的父级数据

希望能够在解析器中访问来自字段的父字段的数据是很常见的。例如，假设想在 `User` 上定义 `fullName` 字段。可以用结合了名字和姓氏的解析器定义新字段：

::::{card-carousel} 2
:::{card} Python
```python
import strawberry


@strawberry.type
class User:
    first_name: str
    last_name: str

    @strawberry.field
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
```
:::
:::{card} Schema
```
type User {
    firstName: String!
    lastName: String!
    fullName: String!
}
```
:::
::::

在修饰过的解析器的情况下，你可以使用 `self` 参数，就像你在普通 Python class[^1] 的方法中所做的那样。对于定义为普通 Python 函数的解析器，您可以使用特殊的 `root` 形参，当添加到函数的实参中时，Strawberry 会将父参数的值传递给它：

```python
import strawberry


def full_name(root: User) -> str:
    return f"{root.first_name} {root.last_name}"


@strawberry.type
class User:
    first_name: str
    last_name: str
    full_name: str = strawberry.field(resolver=full_name)
```

## 访问执行信息

有时访问当前执行上下文的信息是有用的。Strawberry 允许声明 `Info` 类型的参数，该参数将自动传递给解析器。此参数包含当前执行上下文的信息。

```python
import strawberry
from strawberry.types import Info


def full_name(root: User, info: Info) -> str:
    return f"{root.first_name} {root.last_name} {info.field_name}"


@strawberry.type
class User:
    first_name: str
    last_name: str
    full_name: str = strawberry.field(resolver=full_name)
```

```{tip}
你不必称这个参数为 `info`，它的名字可以是任何东西。Strawberry 使用类型将正确的值传递给解析器。
```

### 解析器 API

`Info` 对象包含当前执行上下文的信息：

`class Info(Generic[ContextType, RootValueType])`

| Parameter name  | Type                      | Description                                                           |
| --------------- | ------------------------- | --------------------------------------------------------------------- |
| field_name      | `str`                     | The name of the current field (generally camel-cased)                 |
| python_name     | `str`                     | The 'Python name' of the field (generally snake-cased)                |
| context         | `ContextType`             | The value of the context                                              |
| root_value      | `RootValueType`           | The value for the root type                                           |
| variable_values | `Dict[str, Any]`          | The variables for this operation                                      |
| operation       | `OperationDefinitionNode` | The ast for the current operation (public API might change in future) |
| path            | `Path`                    | The path for the current field                                        |
| selected_fields | `List[SelectedField]`     | Additional information related to the current field                   |
| schema          | `Schema`                  | The Strawberry schema instance                                        |

[^1]:
    see
    [this discussion](https://github.com/strawberry-graphql/strawberry/discussions/515)
    for more context around the self parameter.
