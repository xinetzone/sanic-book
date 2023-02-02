---
title: Input types
---
(Input types)=
# 输入类型

除了[对象类型](./object-types)，GraphQL 还支持输入类型。虽然与对象类型类似，但它们更适合于输入数据，因为它们限制了字段可以使用的类型种类。

GraphQL 规范是这样[定义对象类型和输入类型之间的区别](https://spec.graphql.org/June2018/#sec-Input-Objects)的：

> GraphQL 对象类型（ObjectTypeDefinition）不适合重用（作为输入），因为对象类型可以包含定义参数的字段，也可以包含对接口和联合的引用，这两种类型都不适合用作输入参数。因此，输入对象在系统中有单独的类型。

## 定义输入类型

在 Strawberry 中，可以使用 `@strawberry.input` 装饰器来定义输入类型，像这样：

```python
import strawberry

@strawberry.input
class Point2D:
    x: float
    y: float

```
```
input Point2D {
  x: Float!
  y: Float!
}
```

然后你可以使用输入类型作为你的字段或变更的参数：

```python
import strawberry


@strawberry.type
class Mutation:
    @strawberry.mutation
    def store_point(self, a: Point2D) -> bool:
        return True
```

如果希望包含可选参数，则需要为它们提供默认值。例如，如果想扩展上面的例子，以允许我们的点的可选标签，可以这样做：

```python
import strawberry
from typing import Optional

@strawberry.input
class Point2D:
    x: float
    y: float
    label: Optional[str] = None
```
```
type Point2D {
    x: Float!
    y: Float!
    label: String = null
}
```

或者你也可以使用 `strawberry.UNSET` 来代替默认值 `None`，这将使该字段在模式中是可选的：

```python
import strawberry
from typing import Optional

@strawberry.input
class Point2D:
    x: float
    y: float
    label: Optional[str] = strawberry.UNSET
```
```
type Point2D {
    x: Float!
    y: Float!
    label: String
}
```

## 输入 API

`@strawberry.input(name: str = None, description: str = None)`

根据类定义创建输入类型。

- `name`：如果设置了，这将是 GraphQL 的名称，否则 GraphQL 将通过驼峰式的类名来生成。
- `description`：这是在自省模式或使用 GraphiQL 导航模式时返回的 GraphQL 描述。
