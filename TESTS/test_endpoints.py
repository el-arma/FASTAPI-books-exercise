import requests

PORT = 8000

def get_books(port: int = PORT):
    api_URI = "/api/v1/books"
    myURI = f"http://127.0.0.1:{port}/{api_URI}"
    res = requests.get(myURI)
    return res

def get_book(api_URI: str, port: int = PORT):
    myURI = f"http://127.0.0.1:{port}{api_URI}"
    res = requests.get(myURI)
    return res

def test_health_check(port: int = PORT):
    api_URI = "/health"
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
    res = get_book("/api/v1/books/1")
    assert res.status_code == 200
    assert res.json()['title'] == "The Hunger Games (The Hunger Games, #1)"

def test_add_book(port: int = PORT):
    api_URI = "/api/v1/books"
    myURI = f"http://127.0.0.1:{port}/{api_URI}"
    
    testJSONData = {
    "author": "J.K. Rowling",
    "title": "Hary Pioter"
    }

    res = requests.post(myURI, json = testJSONData)
    assert res.status_code == 201

    location: str = res.headers.get("Location")

    assert get_book(location).json()['title'] == "Hary Pioter"

def test_put_book(port: int = PORT):

    api_URI = "api/v1/books"
    myURI = f"http://127.0.0.1:{port}/{api_URI}"
    
    test_JSON_Data = {
    "author": "J.K. Rowling",
    "title": "Hary Pioter"
    }

    res = requests.post(myURI, json = test_JSON_Data)
    assert res.status_code == 201

    location: str = res.headers.get("Location")
    api_URI = "/api/v1/book"
    myURI = f"http://127.0.0.1:{port}{location}"
    
    updt_test_JSON_Data = {
    "author": "J.K. Gowling",
    "title": "Gary Pjoter"
    }

    res = requests.put(myURI, json = updt_test_JSON_Data)

    assert res.status_code == 204

    assert get_book(location).json()['title'] == "Gary Pjoter"




# def test_del_book(port: int = PORT):
#     book_count = len(get_books().json())
#     api_URI = f"/api/v1/book/{book_count}"
#     myURI = f"http://127.0.0.1:{port}/{api_URI}"
#     res = requests.delete(myURI)
#     assert res.status_code == 200
#     new_book_count = len(get_books().json())
#     assert new_book_count == book_count - 1



# def test_del_book_err(port: int = PORT):
#     book_count = len(get_books().json())
#     api_URI = f"/api/v1/book/{book_count + 1}"
#     myURI = f"http://127.0.0.1:{port}/{api_URI}"
#     res = requests.delete(myURI)
#     assert res.status_code == 404
    
# # add tests for put & update

# # ============================================================ RUN TEST ============================================================
# # TO RUN: pytest -v
