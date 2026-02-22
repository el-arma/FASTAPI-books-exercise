import requests

PORT = 8000

def get_books(port: int = PORT):
    api_URI = "/api/v1/books"
    myURI = f"http://127.0.0.1:{port}/{api_URI}"
    res = requests.get(myURI)
    return res

def get_book(book_id: int, port: int = PORT):
    api_URI = f"/api/v1/book/{book_id}"
    myURI = f"http://127.0.0.1:{port}/{api_URI}"
    res = requests.get(myURI)
    return res

def test_health_check(port: int = PORT):
    api_URI = "health"
    myURI = f"http://127.0.0.1:{port}/{api_URI}"
    res = requests.get(myURI)
    assert res.status_code == 200

def test_get_books(port: int = PORT):
    res = get_books(port)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_get_rand_book(port: int = PORT):
    api_URI = "/api/v1/random-book"
    myURI = f"http://127.0.0.1:{port}/{api_URI}"
    res = requests.get(myURI)
    assert res.status_code == 200

def test_get_book(port: int = PORT):
    res = get_book(1)
    assert res.status_code == 200
    assert res.json() == "The Hunger Games (The Hunger Games, #1)"

def test_add_book(port: int = PORT):
    api_URI = "/api/v1/book"
    myURI = f"http://127.0.0.1:{port}/{api_URI}"
    
    testJSONData = {
    "author": "J.K. Rowling",
    "title": "Hary Pioter"
    }

    res = requests.post(myURI, json = testJSONData)
    book_count = len(get_books().json())
    assert res.status_code == 200
    assert get_book(book_count).json() == "Hary Pioter"


def test_del_book(port: int = PORT):
    book_count = len(get_books().json())
    api_URI = f"/api/v1/book/{book_count}"
    myURI = f"http://127.0.0.1:{port}/{api_URI}"
    res = requests.delete(myURI)
    assert res.status_code == 200
    new_book_count = len(get_books().json())
    assert new_book_count == book_count - 1

# ============================================================ RUN TEST ============================================================
# TO RUN: pytest -v

