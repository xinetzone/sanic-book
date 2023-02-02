(Interfaces)=
# 接口

接口是一种抽象类型，可以通过对象类型实现。

接口有字段，但从未实例化。相反，对象可以实现接口，这使它们成为该接口的成员。此外，字段可以返回接口类型。当这种情况发生时，返回的对象可以是该接口的任何成员。

例如，假设 `Customer` （接口）既可以是 `Individual`（对象），也可以是 `Company` （对象）。下面是在 [GraphQL 模式定义语言](https://graphql.org/learn/schema/#type-language)（Schema Definition Language，简称 SDL）中可能出现的情况：

```
interface Customer {
  name: String!
}

type Company implements Customer {
  employees: [Individual!]!
  name: String!
}

type Individual implements Customer {
  employed_by: Company
  name: String!
}

type Query {
  customers: [Customer!]!
}
```

注意，`Customer` 接口要求 `name: String!` 字段。`Company` 和 `Individual` 都实现了该字段，以便他们能够满足 `Customer` 接口。

查询时，可以选择接口上的字段：

```
query {
  customers {
    name
  }
}
```

无论对象是 `Company` 还是 `Individual`，都没有关系——你仍然得到他们的名字。如果你想要一些特定于对象的字段，你可以用[内联片段](https://graphql.org/learn/queries/#inline-fragments)查询它们，例如：

```
query {
  customers {
    name
    ... on Individual {
      company {
        name
      }
    }
  }
}
```

当您有一组可互换使用的对象时，接口是很好的选择，而且它们有几个重要的共同字段。当它们没有共同的字段时，使用 [Union](./union)。

## 定义接口

接口是使用 `@strawberry.interface` 装饰器定义的：

```python
import strawberry

@strawberry.interface
class Customer:
    name: str
```
```
interface Customer {
  name: String!
}
```

```{note}
接口类永远不应该直接实例化。
```

## 实现接口

要定义实现接口的对象类型，该类型必须继承自接口：

```python
import strawberry


@strawberry.type
class Individual(Customer):
    # additional fields
    ...


@strawberry.type
class Company(Customer):
    # additional fields
    ...
```

````{tip}
如果您添加了实现接口的对象类型，但该对象类型没有作为字段返回类型或联合成员出现在您的模式中，那么您将需要直接将该对象添加到模式定义中。
```python
schema = strawberry.Schema(query=Query, types=[Individual, Company])
```
````

接口也可以实现其他接口：

```python
import strawberry

@strawberry.interface
class Error:
    message: str

@strawberry.interface
class FieldError(Error):
    message: str
    field: str

@strawberry.type
class PasswordTooShort(FieldError):
    message: str
    field: str
    fix: str
```
```
interface Error {
  message: String!
}

interface FieldError implements Error {
  message: String!
  field: String!
}

type PasswordTooShort implements FieldError & Error {
  message: String!
  field: String!
  minLength: Int!
}
```

## 实现字段

接口也可以提供字段实现。例如：

```python
import strawberry


@strawberry.interface
class Customer:
    @strawberry.field
    def name(self) -> str:
        return self.name.title()
```

这个 resolve 方法将由实现该接口的对象调用。对象类可以通过定义自己的 `name` 字段来覆盖实现：

```python
import strawberry


@strawberry.type
class Company(Customer):
    @strawberry.field
    def name(self) -> str:
        return f"{self.name} Limited"
```

## 解析接口

当字段的返回类型是接口时，GraphQL 需要知道返回值使用什么特定的对象类型。在上面的例子中，每个 customer 必须被归类为 `Individual` 或 `Company`。要做到这一点，你需要总是从你的解析器返回对象类型的实例：

```python
import strawberry


@strawberry.type
class Query:
    @strawberry.field
    def best_customer(self) -> Customer:
        return Individual(name="Patrick")
```
