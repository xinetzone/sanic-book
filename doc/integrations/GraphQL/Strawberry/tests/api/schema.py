import strawberry

@strawberry.type
class User:
    id: strawberry.ID
    name: str
    
def get_author_for_book(root) -> "Author":
    return Author(name="Michael Crichton")


@strawberry.type
class Book:
    title: str
    author: str #"Author" = strawberry.field(resolver=get_author_for_book)

def get_books_for_author(root):
    return [Book(title="Jurassic Park")]


@strawberry.type
class Author:
    name: str
    books: list[Book] = strawberry.field(resolver=get_books_for_author)

# 在这个例子中，你可以安全地忽略 Query，它是 strawberry.Schema 所要求的，
# 所以为了完整起见，这里包含了它
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