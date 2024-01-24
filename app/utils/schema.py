import strawberry

@strawberry.type
class Book:
    title: str
    author: str

@strawberry.type
class Query:
    books: list[Book]

def get_books():
    return [
        Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
        ),
    ]
@strawberry.type
class Query:
    books: list[Book] = strawberry.field(resolver=get_books)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, title: str, author: str) -> Book:
        print(f"Adding {title} by {author}")

        return Book(title=title, author=author)

schema = strawberry.Schema(query=Query, mutation=Mutation)
