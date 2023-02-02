import strawberry







def get_authors(root) -> list[Author]:
    return [Author(name="Michael Crichton")]


@strawberry.type
class Query:
    authors: list[Author] = strawberry.field(resolver=get_authors)
    books: list[Book] = strawberry.field(resolver=get_books_for_author)

@strawberry.input
class Point2D:
    x: float
    y: float

@strawberry.type
class Mutation:
    @strawberry.mutation
    def store_point(self, a: Point2D) -> bool:
        return True
        
@strawberry.input
class AddBookInput:
    title: str = strawberry.field(description="The title of the book")
    author: str = strawberry.field(description="The name of the author")

@strawberry.type
class Mutation:
    @strawberry.field
    def add_book(self, book: AddBookInput) -> Book:
        # return AddBookInput(title=title)
        ...

schema = strawberry.Schema(query=Query, mutation=Mutation)
