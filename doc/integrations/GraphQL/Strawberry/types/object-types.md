(Object types)=
# 对象类型

对象类型是任何 GraphQL 模式的基础，用于定义模式中存在的对象类型。对象类型是通过定义名称和字段列表来创建的，下面是使用 GraphQL 模式语言定义的对象类型示例：

```
type Character {
  name: String!
  age: Int!
}
```

## 关于查询、变更和订阅的说明

在阅读 GraphQL 时，您可能会遇到三种特殊的对象类型：`Query`、`Mutation` 和 `Subscription`。它们被定义为标准对象类型，不同之处在于它们也被用作模式的入口点（也称为根类型）。

- `Query` 是所有查询操作的入口点。
- `Mutation` 是所有变更的切入点。
- `Subscription` 是所有订阅的切入点。

要了解如何定义模式，请阅读[模式基础](../general/schema-basics)知识。

## 定义对象类型

在 Strawberry 中，你可以使用 `@strawberry.type` 装饰器来定义对象类型：

```python
import strawberry

@strawberry.type
class Character:
    name: str
    age: int
```
```
type Character {
  name: String!
  age: int!
}
```

也可以引用其他类型，像这样：

```python
import strawberry

@strawberry.type
class Character:
    name: str
    age: int

@strawberry.type
class Book:
    title: str
    main_character: Character
```
```
type Character {
  name: String!
  age: Int!
}

type Book {
  title: String!
  mainCharacter: Character!
}
```

## 对象 API

`@strawberry.type(name: str = None, description: str = None)`

从类定义创建对象类型。

`name`：如果设置了，这将是 GraphQL 的名称，否则 GraphQL 将通过驼峰式的类名来生成。

`description`：这是在自省模式或使用 GraphiQL 导航模式时返回的 GraphQL 描述。
