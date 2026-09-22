from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from database import BookDatabaseManager


app = FastAPI(
    title="Book Data API",
    description="API for managing scraped book data",
    version="1.0"
)


db = BookDatabaseManager()


class Book(BaseModel):
    title: str
    price: float = Field(gt=0)
    in_stock: bool
    rating: int = Field(ge=1, le=5)


# GET all books
@app.get("/books")
def get_books():
    return db.get_all_books()


# GET single book
@app.get("/books/{book_id}")
def get_book(book_id: int):

    book = db.get_book(book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


# POST
@app.post("/books", status_code=201)
def create_book(book: Book):

    book_id = db.insert_book(
        book.title,
        book.price,
        book.in_stock,
        book.rating
    )

    return db.get_book(book_id)


# PUT
@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):

    updated = db.update_book(
        book_id,
        book.title,
        book.price,
        book.in_stock,
        book.rating
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return db.get_book(book_id)


# DELETE
@app.delete("/books/{book_id}")
def delete_book(book_id: int):

    deleted = db.delete_book(book_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return {
        "message": "Book deleted successfully"
    }