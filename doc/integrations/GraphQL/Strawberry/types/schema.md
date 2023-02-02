(Schema)=
# 模式

每个 GraphQL API 都有模式（Schema），用于定义 API 的所有功能。模式是通过传递三种[对象类型](./object-types)来定义的：`Query`、`Mutation` 和 `Subscription`。

`Mutation` 和 `Subscription` 是可选的，同时 `Query` 必须始终存在。

使用 Strawberry 定义的模式示例：

```python
import strawberry


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


schema = strawberry.Schema(Query)
```

## 模式 API 参考

```python
class Schema(Query, mutation=None, subscription=None, **kwargs):
    ...
```

<!-- TODO: add docs on directives, types, extensions and execution context class -->

#### `query: Type`

Strawberry 类型的根查询。通常称为 `Query`。

```{note}
创建 Schema 时总是需要查询类型。
```

#### `mutation: Optional[Type] = None`

根变更类型。通常叫做 `Mutation`。

#### `subscription: Optional[Type] = None`

根订阅类型。通常称为 `Subscription`。

#### `config: Optional[StrawberryConfig] = None`

传递 `StrawberryConfig` 对象来配置如何生成模式。阅读[更多](./schema-configurations)。

#### `types: List[Type] = []`

要注册到 Schema 的额外类型的列表，这些类型不是直接从根查询链接到的。 

````{dropdown} 使用接口时定义额外的 **types**
```python
from datetime import date
import strawberry


@strawberry.interface
class Customer:
    name: str


@strawberry.type
class Individual(Customer):
    date_of_birth: date


@strawberry.type
class Company(Customer):
    founded: date


@strawberry.type
class Query:
    @strawberry.field
    def get_customer(
        self, id: strawberry.ID
    ):  # -> Customer   note we're returning the interface here
        if id == "mark":
            return Individual(name="Mark", date_of_birth=date(1984, 5, 14))

        if id == "facebook":
            return Company(name="Facebook", founded=date(2004, 2, 1))


schema = strawberry.Schema(Query, types=[Individual, Company])
```
````

#### `extensions: List[Type[Extension]] = []`

添加到模式的 [extensions](../extensions)。

#### `scalar_overrides: Optional[Dict[object, ScalarWrapper]] = None`

重写内置标量的实现。[更多信息](overriding-built-in-scalars).

---

## 方法

### `.execute()` (async)

针对模式执行 GraphQL 操作（async）。

```python
async def execute(query, variable_values, context_value, root_value, operation_name):
    ...
```

#### `query: str`

要执行的 GraphQL 文档。

#### `variable_values: Optional[Dict[str, Any]] = None`

这个操作的变量。

#### `context_value: Optional[Any] = None`

将传递给解析器的上下文的值。

#### `root_value: Optional[Any] = None`

将传递给根解析器的根值的值。

#### `operation_name: Optional[str] = None`

要执行的操作的名称，在发送包含多个操作的文档时非常有用。如果没有指定 `operation_name`，则第一个
文档中的操作将被执行。

### `.execute_sync()`

针对模式执行 GraphQL 操作

```python
def execute_sync(query, variable_values, context_value, root_value, operation_name):
    ...
```

#### `query: str`

要执行的 GraphQL 文档。

#### `variable_values: Optional[Dict[str, Any]] = None`

这个操作的变量。

#### `context_value: Optional[Any] = None`

将传递给解析器的上下文的值。

#### `root_value: Optional[Any] = None`

将传递给根解析器的根值的值。

#### `operation_name: Optional[str] = None`

要执行的操作的名称，在发送包含多个操作的文档时非常有用。如果没有指定 `operation_name`，则第一个
文档中的操作将被执行。

---

## 处理执行错误

默认情况下，Strawberry 会将查询执行过程中遇到的任何错误记录到 `strawberry.execution` 日志。这种行为可以通过重写模式的 `strawberry.Schema` 类的 process_errors` 函数来改变。

默认的功能是这样的：

```python
# strawberry/schema/base.py
from strawberry.types import ExecutionContext

logger = logging.getLogger("strawberry.execution")


class BaseSchema:
    ...

    def process_errors(
        self,
        errors: List[GraphQLError],
        execution_context: Optional[ExecutionContext] = None,
    ) -> None:
        StrawberryLogger.error(error, execution_context)
```

```python
# strawberry/utils/logging.py
from strawberry.types import ExecutionContext


class StrawberryLogger:
    logger: Final[logging.Logger] = logging.getLogger("strawberry.execution")

    @classmethod
    def error(
        cls,
        error: GraphQLError,
        execution_context: Optional[ExecutionContext] = None,
        # https://www.python.org/dev/peps/pep-0484/#arbitrary-argument-lists-and-default-argument-values
        **logger_kwargs: Any,
    ) -> None:
        # "stack_info" is a boolean; check for None explicitly
        if logger_kwargs.get("stack_info") is None:
            logger_kwargs["stack_info"] = True

        # stacklevel was added in version 3.8
        # https://docs.python.org/3/library/logging.html#logging.Logger.debug
        if sys.version_info >= (3, 8):
            logger_kwargs["stacklevel"] = 3

        cls.logger.error(error, exc_info=error.original_error, **logger_kwargs)
```
