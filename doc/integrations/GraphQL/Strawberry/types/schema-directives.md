---
title: Schema Directives
---
(Schema Directives)=
# 模式指令

Strawberry 支持[模式指令](https://spec.graphql.org/June2018/#TypeSystemDirectiveLocation)，这些指令不会改变 GraphQL 模式的行为，而是提供了向其添加额外元数据的方法。

> 例如，[Apollo Federation](../guides/federation.md) 集成是基于模式指令的。

模式中使用：

```python
# directives.py
import strawberry
from strawberry.schema_directive import Location


@strawberry.schema_directive(locations=[Location.OBJECT])
class Keys:
    fields: str
```
```python
from .directives import Keys


@strawberry.type(directives=[Keys(fields="id")])
class User:
    id: strawberry.ID
    name: str
```

这将产生以下模式：

```
type User @keys(fields: "id") {
  id: ID!
  name: String!
}
```

## 重载字段名称

可以使用 `strawberry.directive_field` 重载字段名称：

```python
@strawberry.schema_directive(locations=[Location.OBJECT])
class Keys:
    fields: str = strawberry.directive_field(name="as")
```

## 站点

模式指令可以应用于模式的许多不同部分。以下是所有允许的站点列表：

| Name                   |                         | Description                                              |
| ---------------------- | ----------------------- | -------------------------------------------------------- |
| SCHEMA                 | `strawberry.Schema`     | The definition of a schema                               |
| SCALAR                 | `strawberry.scalar`     | The definition of a scalar                               |
| OBJECT                 | `strawberry.type`       | The definition of an object type                         |
| FIELD_DEFINITION       | `strawberry.field`      | The definition of a field on an object type or interface |
| ARGUMENT_DEFINITION    | `strawberry.argument`   | The definition of an argument                            |
| INTERFACE              | `strawberry.interface`  | The definition of an interface                           |
| UNION                  | `strawberry.union`      | The definition of an union                               |
| ENUM                   | `strawberry.enum`       | The definition of a enum                                 |
| ENUM_VALUE             | `strawberry.enum_value` | The definition of a enum value                           |
| INPUT_OBJECT           | `strawberry.input`      | The definition of an input object type                   |
| INPUT_FIELD_DEFINITION | `strawberry.field`      | The definition of a field on an input type               |
