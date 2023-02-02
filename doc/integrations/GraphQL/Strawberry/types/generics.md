(Generics)=
# 泛型

Strawberry 支持使用 Python 的 `Generic` 类型动态创建可重用类型。

Strawberry 将从泛型类型和类型参数的组合中自动生成正确的 GraphQL 模式。泛型在对象类型、输入类型和查询参数、变更和标量中得到支持。

示例：

# 对象类型

```python
from typing import Generic, List, TypeVar

import strawberry

T = TypeVar("T")


@strawberry.type
class Page(Generic[T]):
    number: int
    items: List[T]
```

这个例子定义了泛型类型 `Page`，它可以用来表示任何类型的页面。例如，可以创建 `User` 对象页面：

```python
import strawberry

@strawberry.type
class User:
    name: str

@strawberry.type
class Query:
    users: Page[User]
```
```
type Query {
  users: UserPage!
}

type User {
  name: String!
}

type UserPage {
  number: Int!
  items: [User!]!
}
```

# 输入和参数类型

通过创建泛型输入类型，查询和变更的参数也可以成为泛型。在这里，将定义输入类型，它可以作为任何东西的集合，然后通过在变更上使用作为填充参数来创建专门化。

```python
import strawberry
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")

@strawberry.input
class CollectionInput(Generic[T]):
    values: List[T]

@strawberry.input
class PostInput:
    name: str

@strawberry.type
class Post:
    id: int
    name: str

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_posts(self, posts: CollectionInput[PostInput]) -> bool:
        return True

@strawberry.type
class Query:
    most_recent_post: Optional[Post] = None

schema = strawberry.Schema(query=Query, mutation=Mutation)
```
```
input PostInputCollectionInput {
  values: [PostInput!]!
}

input PostInput {
  name: String!
}

type Post {
  id: Int!
  name: String!
}

type Query {
  mostRecentPost: Post
}

type Mutation {
  addPosts(posts: PostInputCollectionInput!): Boolean!
}
```

````{note}
请注意，`CollectionInput` 和 `PostInput` 都是输入类型。将 `posts: CollectionInput[Post]` 提供给 `add_posts` （即使用非输入 `Post` 类型）将导致异常：
```
PostCollectionInput fields cannot be resolved. Input field type must be a
GraphQL input type
```
````

# 多个专门化

使用泛型类型的多个专门化可以正常工作。这里定义了 `Point2D` 类型，然后针对 `int` 和 `float` 专门化它。

```python
from typing import Generic, TypeVar

import strawberry

T = TypeVar('T')

@strawberry.input
class Point2D(Generic[T]):
    x: T
    y: T

@strawberry.type
class Mutation:
    @strawberry.mutation
    def store_line_float(self, a: Point2D[float], b: Point2D[float]) -> bool:
        return True

    @strawberry.mutation
    def store_line_int(self, a: Point2D[int], b: Point2D[int]) -> bool:
        return True
```
```
type Mutation {
  storeLineFloat(a: FloatPoint2D!, b: FloatPoint2D!): Boolean!
  storeLineInt(a: IntPoint2D!, b: IntPoint2D!): Boolean!
}

input FloatPoint2D {
  x: Float!
  y: Float!
}

input IntPoint2D {
  x: Int!
  y: Int!
}
```

# 可变泛型

在 {pep}`646` 中引入的可变泛型 (Variadic Generics) 目前不受支持。
