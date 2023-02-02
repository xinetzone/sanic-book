=
(Schema Configurations)=
# 模式配置

Strawberry 允许自定义如何通过传递配置来生成模式。目前只允许禁用字段和参数名称的自动驼峰大小写。

要定制模式，可以创建 `StrawberryConfig` 实例，如下面的例子所示：

```python
import strawberry

from strawberry.schema.config import StrawberryConfig


@strawberry.type
class Query:
    example_field: str


schema = strawberry.Schema(query=Query, config=StrawberryConfig(auto_camel_case=False))
```

在这种情况下，禁用了自动驼峰大小写功能，所以你的输出模式将是这样的：

```graphql
type Query {
  example_field: String!
}
```
