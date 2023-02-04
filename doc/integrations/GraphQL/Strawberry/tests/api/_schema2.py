import uuid
# import decimal
import datetime
import strawberry
from strawberry.schema.config import StrawberryConfig
from .directives import Keys

def get_author_for_book(root) -> "Author":
    return Author(name="Michael Crichton")


@strawberry.type
class Book:
    title: str
    author: "Author" = strawberry.field(resolver=get_author_for_book)


def get_books_for_author(root):
    return [Book(title="Jurassic Park")]


@strawberry.type
class Author:
    name: str
    books: list[Book] = strawberry.field(resolver=get_books_for_author)


def get_authors(root) -> list[Author]:
    return [Author(name="Michael Crichton")]


@strawberry.input
class AddBookInput:
    title: str = strawberry.field(description="The title of the book")
    author: str = strawberry.field(description="The name of the author")


@strawberry.type(directives=[Keys(fields="id")])
class User:
    id: strawberry.ID
    name: str

@strawberry.type
class Query:
    authors: list[Author] = strawberry.field(resolver=get_authors)
    books: list[Book] = strawberry.field(resolver=get_books_for_author)
    @strawberry.field
    def one_week_from(self, date_input: datetime.date) -> datetime.date:
        return date_input + datetime.timedelta(weeks=1)
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, title: str, author: str) -> Book:
        print(f"Adding {title} by {author}")
        return AddBookInput(title=title, author=author)

schema = strawberry.Schema(query=Query, mutation=Mutation,
                           config=StrawberryConfig(auto_camel_case=False))
