from fastapi import FastAPI, Depends, Body, HTTPException, status, Response
import sqlite3
import os
from LOGGERS.loggers import create_logger
from contextlib import asynccontextmanager


ENV = os.getenv("ENV", "PROD") 

DB_NAME_PROD = r"DB\PROD\books.db"

if ENV == "TEST": 
    DB_NAME = "in-memory"
else:
    DB_NAME = DB_NAME_PROD

logger = create_logger("main-logger")

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info(f"MODE: {ENV} | DB: {DB_NAME}")

    if ENV == "TEST":
        app.state.test_connection = sqlite3.connect(
            "file::memory:?cache=shared",
            uri=True,
            check_same_thread=False
        )
        app.state.test_connection.row_factory = sqlite3.Row
        app.state.test_connection.execute("""
            CREATE TABLE books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                code_id TEXT NOT NULL,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                amount INTEGER NOT NULL, 
                price REAL NOT NULL,
                cover_image_url TEXT
            );
        """)
        app.state.test_connection.commit()

    yield

    if ENV == "TEST":
        app.state.test_connection.close()

    logger.info("Application gracefully shutting down")

app = FastAPI(lifespan=lifespan)

# Dependency
def get_db():
    if ENV == "TEST":
        yield app.state.test_connection
    else:
        conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        # check_same_thread = False - can be deleted
        # prevents using same thread in many requests, but here we have separates threads for each endpoint
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

@app.get("/")
def home():
    return {"message": "Hello 📚🐛"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# list all books
#TODO: list gets big, Offset Pagination needed
@app.get("/api/v1/books")
def get_all_books(db = Depends(get_db)):
    cursor = db.execute("SELECT * FROM books;")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

# return book record by id:
# Path parameter (/book/{id}) → use it when you are identifying a specific resource.
@app.get("/api/v1/books/{book_id}")
def get_book(book_id: int, db = Depends(get_db)):
    cursor = db.execute("SELECT * FROM books WHERE book_id = ? ;", (book_id,))
    row = cursor.fetchone()

    if row is None:
        raise HTTPException(404, detail=f"Book with id {book_id} not found")
    
    return dict(row)

# query string: return all books of given author 
# Query parameter (?author=) → use it when you are filtering, searching, or modifying how a collection is returned.
@app.get("/api/v1/books-by-author")
def get_authors_books(author: str, db = Depends(get_db)):
    cursor = db.execute("SELECT * FROM books WHERE author = ? ;", (author,))
    rows = cursor.fetchall()

    return [dict(row) for row in rows]

# get random book:
@app.get("/api/v1/random-book")
def get_rand_book(db = Depends(get_db)):
    cursor = db.execute("SELECT * FROM books ORDER BY RANDOM() LIMIT 1;")
    # NOTE: This query may not be optimal for large data set!
    row = cursor.fetchone()
    if not row:
        raise HTTPException(404, detail="No books available in the database")
    return dict(row)

# add new book:
@app.post("/api/v1/books", status_code = status.HTTP_201_CREATED)
def add_book(book_data: dict, response: Response, db = Depends(get_db)):

    try:
        code_id = book_data["code_id"]
        title = book_data["title"]
        author = book_data["author"]
        amount = book_data["amount"]
        price = book_data["price"]
        cover_image_url = book_data["cover_image_url"]
    except KeyError:
        raise HTTPException(400, detail="Bad fields provided.")

    cursor = db.execute(
    "INSERT INTO books (code_id, title, author, amount, price, cover_image_url) VALUES (?, ?, ?, ?, ?, ?);",
    (code_id, title, author, amount, price, cover_image_url)
    )
    db.commit()
    
    created_id = cursor.lastrowid

    # Set Location header:
    response.headers["Location"] = f"/api/v1/books/{created_id}"

    return {
        "book_id": created_id,
        "code_id": code_id,
        "title": title,
        "author": author,
        "amount": amount,
        "price": price,
        "cover_image_url": cover_image_url
    }

# update book (all fields):
@app.put("/api/v1/books/{book_id}", status_code = status.HTTP_204_NO_CONTENT)
def update_book(book_id: int, book_data: dict, db = Depends(get_db)):

    try:
        title = book_data["title"]
        author = book_data["author"]
    except KeyError:
        raise HTTPException(400, detail="Bad fields provided.")
    
    cursor = db.execute("UPDATE books SET title = ?, author = ? WHERE book_id = ?;", (title, author, book_id))
    db.commit()
    
    if cursor.rowcount == 0:
        raise HTTPException(404, detail=f"Book with id {book_id} not found")

    return None

# update book (given field):
@app.patch("/api/v1/books/{book_id}", status_code = status.HTTP_204_NO_CONTENT)
def patch_book(book_id: int, book_data: dict, db = Depends(get_db)):

    allowed_fields = {"code_id", "title", "author", "amount", "price", "cover_image_url"}  # whitelist of fields

    if not book_data:
        raise HTTPException(400, detail="No fields provided.")

    fields = []
    values = []

    for key, value in book_data.items():
        if key in allowed_fields:
            fields.append(f"{key} = ?")
            values.append(value)

    values.append(book_id)

    if not fields:
        raise HTTPException(400, detail="No fields provided.")
    
    query = f"UPDATE books SET {', '.join(fields)} WHERE book_id = ?;"

    cursor = db.execute(query, values)
    db.commit()

    if cursor.rowcount == 0:
        raise HTTPException(404, detail=f"Book with id {book_id} not found")

    return None


# delete book by id:
@app.delete("/api/v1/books/{book_id}", status_code = status.HTTP_204_NO_CONTENT)
def del_book(book_id: int, db = Depends(get_db), ):
    cursor = db.execute("DELETE FROM books WHERE book_id = ? ;", (book_id,))
    db.commit()

    if cursor.rowcount == 0:
        raise HTTPException(404, detail=f"Book with id {book_id} not found")
    
    return None

# ============================================================ RUN ============================================================
# to run man.:
# uvicorn main:app --reload 

# for tests:
# (can be one per terminal session):
# set ENV=TEST
# uvicorn main:app --reload


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

