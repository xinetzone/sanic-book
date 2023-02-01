(Mutations)=
# 变更

与查询相反，GraphQL 中的变更表示修改服务器端数据和/或对服务器造成副作用的操作。例如，您可以在应用程序中创建新实例的变更，或者发送一封电子邮件的变更。与查询一样，它们接受参数，并可以返回常规字段所能返回的任何内容，包括新类型和现有对象类型。这对于在变更后获取对象的新状态非常有用。

让我们改进[入门教程](../intro.md)中的 `books` 项目，并实现应该添加一本书的变更：

```python
import strawberry


# Reader, you can safely ignore Query in this example, it is required by
# strawberry.Schema so it is included here for completeness
@strawberry.type
class Query:
    @strawberry.field
    def hello() -> str:
        return "world"


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, title: str, author: str) -> Book:
        print(f"Adding {title} by {author}")

        return Book(title=title, author=author)


schema = strawberry.Schema(query=Query, mutation=Mutation)
```

与查询一样，变更在类中定义，然后传递给 Schema 函数。这里创建了 `addBook` 变更，它接受标题和作者，并返回 `Book` 类型。将发送以下 GraphQL 文档到服务器来执行变更：

```
mutation {
  addBook(title: "The Little Prince", author: "Antoine de Saint-Exupéry") {
    title
  }
}
```

`addBook` 变更就是简化的例子。在实际应用程序中，变更通常需要处理错误并将这些错误传递回客户端。例如，如果这本书已经存在，可能希望返回异常。

查看关于[处理错误的文档](../guides/errors#expected-errors)，了解如何从变更中返回类型的并集。

## 无返回数据的变更

也可以编写不返回任何东西的变更。它被映射到 `Void` GraphQL 标量，并且总是返回 `null`

```python
@strawberry.type
class Mutation:
    @strawberry.mutation
    def restart() -> None:
        print(f'Restarting the server')
```

```schema
type Mutation {
  restart: Void
}
```

```{note}
带有 void-result 的变更违背了 [GQL 最佳实践](https://graphql-rules.com/rules/mutation-payload)。
```
