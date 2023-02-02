(Scalars)=
# 标量

标量类型表示查询叶部分的具体值。例如，在下面的查询中，name 字段将解析为标量类型（在这种情况下，它是 `String` 类型）：

```{eval-rst}
.. graphiql:: 
    :query:
      {
        user {
          name
        }
      }
    :response:
      {
        "data": {
          "user": {
            "name": "Patrick"
          }
        }
      }
```

有几个内置的标量，也可以定义自定义标量。（[Enums](./enums)也是叶值。）内置的标量是：

- `String`, maps to Python’s `str`
- `Int`, a signed 32-bit integer, maps to Python’s `int`
- `Float`, a signed double-precision floating-point value, maps to Python’s `float`
- `Boolean`, true or false, maps to Python’s `bool`
- `ID`, a specialised `String` for representing unique object identifiers
- `Date`, an ISO-8601 encoded [date](https://docs.python.org/3/library/datetime.html#date-objects)
- `DateTime`, an ISO-8601 encoded [datetime](https://docs.python.org/3/library/datetime.html#datetime-objects)
- `Time`, an ISO-8601 encoded [time](https://docs.python.org/3/library/datetime.html#time-objects)
- `Decimal`, a [Decimal](https://docs.python.org/3/library/decimal.html#decimal.Decimal) value serialized as a string
- `UUID`, a [UUID](https://docs.python.org/3/library/uuid.html#uuid.UUID) value serialized as a string
- `Void`, always null, maps to Python’s `None`

字段可以通过使用 Python 等效函数返回内置标量：

```python
import datetime
import decimal
import uuid
import strawberry

@strawberry.type
class Product:
    id: uuid.UUID
    name: str
    stock: int
    is_available: bool
    available_from: datetime.date
    same_day_shipping_before: datetime.time
    created_at: datetime.datetime
    price: decimal.Decimal
    void: None
```
```
type Product {
  id: UUID!
  name: String!
  stock: Int!
  isAvailable: Boolean!
  availableFrom: Date!
  sameDayShippingBefore: Time!
  createdAt: DateTime!
  price: Decimal!
  void: Void
}
```

标量类型也可以用作输入：

```python
import datetime
import strawberry


@strawberry.type
class Query:
    @strawberry.field
    def one_week_from(self, date_input: datetime.date) -> datetime.date:
        return date_input + datetime.timedelta(weeks=1)
```

## 自定义标量

可以为模式创建自定义标量，以表示数据模型中的特定类型。这有助于让客户知道对于特定的字段可以期望得到什么样的数据。要自定义标量，您需要给它名称和函数，告诉 Strawberry 如何序列化和反序列化该类型。例如，这里有自定义标量类型来表示 Base64 字符串：

```python
import base64
from typing import NewType

import strawberry

Base64 = strawberry.scalar(
    NewType("Base64", bytes),
    serialize=lambda v: base64.b64encode(v).decode("utf-8"),
    parse_value=lambda v: base64.b64decode(v).encode("utf-8"),
)


@strawberry.type
class Query:
    @strawberry.field
    def base64(self) -> Base64:
        return Base64(b"hi")


schema = strawberry.Schema(Query)

result = schema.execute_sync("{ base64 }")

assert results.data == {"base64": "aGk="}
```

````{note}
`Base16`、`Base32` 和 `Base64` 标量类型在 `strawberry.scalars` 中可用
```python
from strawberry.scalars import Base16, Base32, Base64
```
````

## JSONScalar 示例

```python
import json
from typing import Any, NewType

import strawberry

JSON = strawberry.scalar(
    NewType("JSON", object),
    description="The `JSON` scalar type represents JSON values as specified by ECMA-404",
    serialize=lambda v: v,
    parse_value=lambda v: v,
)
```

用法：

```python
@strawberry.type
class Query:
    @strawberry.field
    def data(self, info) -> JSON:
        return {"hello": {"a": 1}, "someNumbers": [1, 2, 3]}
```


```{eval-rst}
.. graphiql:: 
    :query:
      {
        ExampleDataQuery {
          data
        }
      }
    :response:
      {
        "data": {
          "hello": {
            "a": 1
          },
          "someNumbers": [1, 2, 3]
        }
      }
```
````{note}
`JSON` 标量类型在 `strawberry.scalars` 中可用。

```python
from strawberry.scalars import JSON
```
````

(overriding-built-in-scalars)=
## 覆盖内置的标量

要覆盖内置标量的行为，可以将覆盖映射传递给您的模式。下面是完整的例子，将内置的 `DateTime` 标量替换为将所有 datetimes 序列化为 unix 时间戳的标量：

```python
from datetime import datetime, timezone
import strawberry

# Define your custom scalar
EpochDateTime = strawberry.scalar(
    datetime,
    serialize=lambda value: int(value.timestamp()),
    parse_value=lambda value: datetime.fromtimestamp(int(value), timezone.utc),
)


@strawberry.type
class Query:
    @strawberry.field
    def current_time(self) -> datetime:
        return datetime.now()


schema = strawberry.Schema(
    Query,
    scalar_overrides={
        datetime: EpochDateTime,
    },
)
result = schema.execute_sync("{ currentTime }")
assert result.data == {"currentTime": 1628683200}
```
