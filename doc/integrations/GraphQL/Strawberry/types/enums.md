(Enums)=
# 枚举

枚举是一种特殊类型，仅限于一组特定的值。例如，有一些可供选择的冰淇淋，想让用户只从这些选项中进行选择。Strawberry 支持使用 python 标准库中的 {mod}`enum` 定义枚举。下面是关于如何在 Strawberry 中创建枚举类型的快速教程。

首先，为新类型创建新类，它扩展了类 {class}`~enum.Enum`：
```python
from enum import Enum


class IceCreamFlavour(Enum):
    ...
```

然后，将选项作为该类中的变量列表：

```python
class IceCreamFlavour(Enum):
    VANILLA = "vanilla"
    STRAWBERRY = "strawberry"
    CHOCOLATE = "chocolate"
```

最后，需要将我们的类注册为 strawberry 类型。这是用 `strawberry.enum` 装饰器完成的：

```python
@strawberry.enum
class IceCreamFlavour(Enum):
    VANILLA = "vanilla"
    STRAWBERRY = "strawberry"
    CHOCOLATE = "chocolate"
```

看看如何在模式中使用 `enum`。

```python
@strawberry.type
class Query:
    @strawberry.field
    def best_flavour(self) -> IceCreamFlavour:
        return IceCreamFlavour.STRAWBERRY
```

定义上面的枚举类型将在 GraphQL 中产生以下模式：

```
enum IceCreamFlavour {
  VANILLA
  STRAWBERRY
  CHOCOLATE
}
```

下面是如何使用这个新创建的查询的示例：

```
query {
  bestFlavour
}
```

下面是执行查询的结果：

```json
{
  "data": {
    "bestFlavour": "STRAWBERRY"
  }
}
```

也可以在定义对象类型时使用枚举（使用 `strawberry.type`）。下面是使用 `Enum` 的对象的字段示例：

```python
@strawberry.type
class Cone:
    flavour: IceCreamFlavour
    num_scoops: int


@strawberry.type
class Query:
    @strawberry.field
    def cone(self) -> Cone:
        return Cone(flavour=IceCreamFlavour.STRAWBERRY, num_scoops=4)
```

这里有如何使用这个查询的例子：

```
query {
  cone {
    flavour
    numScoops
  }
}
```

下面是执行查询的结果：

```
{
  "data": {
    "cone": {
      "flavour": "STRAWBERRY",
      "numScoops": 4
    }
  }
}
```

```{note}
GraphQL 类型不像 python {mod}`enum` 那样是 `name: value` 的映射。Strawberry 使用枚举成员的名称创建 GraphQL 类型。
```

你也可以弃用枚举值。要做到这一点，你需要使用 `strawberry.enum_value` 和 `deprecation_reason` 使用更详细的语法。您可以混合和匹配字符串和详细语法。

```python
@strawberry.enum
class IceCreamFlavour(Enum):
    VANILLA = strawberry.enum_value("vanilla")
    STRAWBERRY = strawberry.enum_value("strawberry", deprecation_reason="We ran out")
    CHOCOLATE = "chocolate"
```

<AdditionalResources
  title="Enums"
  spec="https://spec.graphql.org/June2018/#sec-Enums"
  graphqlDocs="https://graphql.org/learn/schema/#enumeration-types"
/>
