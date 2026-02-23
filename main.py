from fastapi import FastAPI, Depends, Body, HTTPException
import sqlite3
import random as rnd
import os
from TESTS.mockDB import create_test_db
from LOGGERS.loggers import create_logger
from contextlib import asynccontextmanager


ENV = os.getenv("ENV", "PROD") 

DB_NAME_TEST = r"DB\TEST\test_books.db"
DB_NAME_PROD = r"DB\PROD\books.db"

if ENV == "TEST": 
    DB_NAME = DB_NAME_TEST
else:
    DB_NAME = DB_NAME_PROD

logger = create_logger("main-logger")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    logger.info(f"MODE: {ENV} | DB: {DB_NAME}")
    if ENV == "TEST":
        create_test_db(DB_NAME_PROD, DB_NAME_TEST)
    
    yield
    
    # SHUTDOWN
    logger.info("Application gracefully shutting down")

app = FastAPI(lifespan=lifespan)

# Dependency
def get_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread = False)
    # check_same_thread = False - can be deleted
    # prevents using same thread in many requests, but here we have separates threads for each endpoint
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
@app.get("/api/v1/books")
def get_all_books(db = Depends(get_db)):
    cursor = db.execute("SELECT title FROM books;")
    rows = cursor.fetchall()
    return [row[0] for row in rows]

# return book by id:
# Path parameter (/book/{id}) → use it when you are identifying a specific resource.
@app.get("/api/v1/book/{book_id}")
def get_book(book_id: int, db = Depends(get_db)):
    cursor = db.execute(f"SELECT title FROM books WHERE book_id = ? ;", (book_id,))
    row = cursor.fetchone()

    if row is None:
        raise HTTPException(404, detail=f"Book with id {book_id} not found")
    
    return row[0]

# return book by id, but query string:
# Query parameter (?book_id=) → use it when you are filtering, searching, or modifying how a collection is returned.
@app.get("/api/v1/book")
def get_book_query(book_id: int, db = Depends(get_db)):
    cursor = db.execute("SELECT title FROM books WHERE book_id = ? ;", (book_id,))
    row = cursor.fetchone()
    
    if row is None:
        raise HTTPException(404, detail=f"Book with id {book_id} not found")
    
    return row[0]

# get random book:
@app.get("/api/v1/random-book")
def get_rand_book(db = Depends(get_db)):
    cursor = db.execute("SELECT COUNT(title) FROM books;")
    rows_count = cursor.fetchone()[0] # get number of rows
    random_id = rnd.randint(1, rows_count)
    cursor = db.execute("SELECT title FROM books WHERE book_id = ? ;", (random_id,))
    random_title = cursor.fetchone()[0] # get random title
    return random_title

# delete book by id:
@app.delete("/api/v1/book/{book_id}")
def del_book(book_id: int, db = Depends(get_db), ):
    cursor = db.execute("DELETE FROM books WHERE book_id = ? ;", (book_id,))
    db.commit()

    if cursor.rowcount == 0:
        raise HTTPException(404, detail=f"Book with id {book_id} not found")
    
    return {f"index: {book_id}": "DELETED"}

# add new book:
@app.post("/api/v1/book")
def add_book(book_data: dict = Body(...), db = Depends(get_db)):
    title = book_data["title"]
    author = book_data["author"]
    db.execute("INSERT INTO books (title, author) VALUES (?, ?);", (title, author))
    db.commit()
    return {
        "msg": "BOOK ADDED SUCCESSFULLY",
        "title": title,
        "author": author
    }

# update book (all fields):
@app.put("/api/v1/book/{book_id}")
# TODO: add error handling for non existing indexes (can use HTTPExept.)
def update_book(book_id: int, book_data: dict = Body(...), db = Depends(get_db)):
    author = book_data["author"]
    title = book_data["title"]
    cursor = db.execute("UPDATE books SET title = ?, author = ? WHERE book_id = ?;", (title, author, book_id))
    db.commit()
    
    if cursor.rowcount == 0:
        raise HTTPException(404, detail=f"Book with id {book_id} not found")

    return {
        "msg": "BOOK UPDATED SUCCESSFULLY",
        "title": title,
        "author": author
    }

# update book (given field):
@app.patch("/api/v1/book/{book_id}")
# TODO: add error handling for non existing indexes (can use HTTPExept.)
def patch_book(book_id: int, book_data: dict = Body(...), db = Depends(get_db)):

    allowed_fields = {"title", "author"}  # whitelist of fields

    fields = []
    values = []

    for key, value in book_data.items():
        if key in allowed_fields:
            fields.append(f"{key} = ?")
            values.append(value)

    values.append(book_id)

    query = f"UPDATE books SET {', '.join(fields)} WHERE book_id = ?;"

    cursor = db.execute(query, values)
    db.commit()

    if cursor.rowcount == 0:
        raise HTTPException(404, detail=f"Book with id {book_id} not found")

    return {
        "msg": "BOOK UPDATED SUCCESSFULLY",
    }


# ============================================================ RUN ============================================================
# to run man.:
# uvicorn main:app --reload 

# for tests:
# (can be one per terminal session):
# set ENV=TEST
# uvicorn main:app --reload


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host = "127.0.0.1", port = 8000)

