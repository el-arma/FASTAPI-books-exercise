from fastapi import FastAPI, Depends, Body
import sqlite3
import random as rnd


app = FastAPI()

DB_NAME = "books.db"

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
# TODO: add error handling for non existing indexes
# Path parameter (/book/{id}) → use it when you are identifying a specific resource.
@app.get("/api/v1/book/{index}")
def get_book(index: int, db = Depends(get_db)):
    cursor = db.execute(f"SELECT title FROM books WHERE book_id = {index};")
    book_title = cursor.fetchone()[0] 
    return {"index": book_title}

# return book by id, but query string:
# TODO: add error handling for non existing indexes
# Query parameter (?book_id=) → use it when you are filtering, searching, or modifying how a collection is returned.
@app.get("/api/v1/book")
def get_book_query(book_id: int, db = Depends(get_db)):
    cursor = db.execute(f"SELECT title FROM books WHERE book_id = {book_id};")
    book_title = cursor.fetchone()[0] 
    return {"index": book_title}

# get random book:
@app.get("/api/v1/random-book")
def get_rand_book(db = Depends(get_db)):
    cursor = db.execute("SELECT COUNT(title) FROM books;")
    rows_count = cursor.fetchone()[0] # get number of rows
    random_id = rnd.randint(1, rows_count)
    cursor = db.execute(f"SELECT title FROM books WHERE book_id = {random_id};")
    random_title = cursor.fetchone()[0] # get random title
    return random_title

# delete book by id:
@app.delete("/api/v1/book/{index}")
# TODO: add error handling for non existing indexes (can use HTTPExept.)
def del_book(index: int, db = Depends(get_db), ):
    db.execute(f"DELETE FROM books WHERE book_id = {index};")
    db.commit()
    return {f"index: {index}": "DELETED"}

# add new book:
@app.post("/api/v1/book")
def add_book(book_data: dict = Body(...), db = Depends(get_db)):
    title = book_data["title"]
    author = book_data["author"]
    db.execute(f"INSERT INTO books (title, authors) VALUES ('{title}', '{author}');")
    db.commit()
    return {
        "msg": "BOOK ADDED SUCCESSFULLY",
        "title": title,
        "author": author
    }

# update book (all fields):
@app.put("/api/v1/book/{index}")
# TODO: add error handling for non existing indexes (can use HTTPExept.)
def update_book(index: int, book_data: dict = Body(...), db = Depends(get_db)):
    title = book_data["title"]
    author = book_data["author"]
    db.execute(f"UPDATE books SET title = '{title}', authors = '{author}' WHERE book_id = {index};")
    db.commit()
    return {
        "msg": "BOOK UPDATED SUCCESSFULLY",
        "title": title,
        "author": author
    }

# update book (given field):
@app.patch("/api/v1/book/{index}")
# TODO: add error handling for non existing indexes (can use HTTPExept.)
def patch_book(index: int, book_data: dict = Body(...), db = Depends(get_db)):
    
    print(book_data)

    allowed_fields = {"title", "authors"}  # whitelist of fields

    fields = []

    for key, value in book_data.items():
        if key in allowed_fields:
            fields.append(f"{key} = '{value}'")

    query = f"UPDATE books SET {', '.join(fields)} WHERE book_id = {index};"

    db.execute(query)
    db.commit()

    return {
        "msg": "BOOK UPDATED SUCCESSFULLY",
    }


# ============================================================ RUN ============================================================
# to run man.:
# uvicorn main:app --reload 

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host = "127.0.0.1", port = 8000)

