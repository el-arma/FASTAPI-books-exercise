import requests

# ================= CONFIG =================

PORT = 8000
BASE_URL = f"http://127.0.0.1:{PORT}"
API_PREFIX = "/api/v1"
CORE_API_URL = f"{BASE_URL}{API_PREFIX}"


# ================= HELPERS =================

def add_book(author="J.K. Rowling", title="Hary Pioter"):
    payload = {
        "author": author,
        "title": title
    }
    return requests.post(f"{CORE_API_URL}/books", json=payload)

def get_book(location: str):
    return requests.get(f"{BASE_URL}{location}")


# ================= TESTS =================

def test_health_check():
    res = requests.get(f"{BASE_URL}/health")
    assert res.status_code == 200


def test_get_books():
    add_book()
    res = requests.get(f"{CORE_API_URL}/books")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_rand_book():
    add_book()  # ensure DB not empty
    res = requests.get(f"{CORE_API_URL}/random-book")
    assert res.status_code == 200
    data = res.json()
    assert "id" in data
    assert "title" in data
    assert "author" in data


def test_get_book():
    res = add_book()
    assert res.status_code == 201

    location = res.headers["Location"]

    res = get_book(location)
    assert res.status_code == 200
    assert res.json()["title"] == "Hary Pioter"


def test_get_book_err():
    res = requests.get(f"{BASE_URL}/api/v1/books/999999")
    assert res.status_code == 404


def test_get_books_by_author():
    add_book(author="J.K. Rowling")
    add_book(author="Other Author")

    res = requests.get(
        f"{CORE_API_URL}/books-by-author",
        params={"author": "J.K. Rowling"}
    )

    assert res.status_code == 200

    data = res.json()
    assert isinstance(data, list)
    assert all(book["author"] == "J.K. Rowling" for book in data)


def test_add_book():
    res = add_book()
    assert res.status_code == 201

    location = res.headers["Location"]
    book = get_book(location).json()
    assert book["title"] == "Hary Pioter"
    assert book["author"] == "J.K. Rowling"


def test_put_book():
    res = add_book()
    location = res.headers["Location"]

    payload = {
        "author": "J.K. Growling",
        "title": "Gary Pjoter"
    }

    res = requests.put(f"{BASE_URL}{location}", json=payload)
    assert res.status_code == 204

    updated = get_book(location).json()
    assert updated["author"] == "J.K. Growling"
    assert updated["title"] == "Gary Pjoter"


def test_patch_book():
    res = add_book()
    location = res.headers["Location"]

    payload = {"title": "Gary Pjoter"}

    res = requests.patch(f"{BASE_URL}{location}", json=payload)
    assert res.status_code == 204

    assert get_book(location).json()["title"] == "Gary Pjoter"


def test_patch_book_err():
    payload = {"title": "Gary Pjoter"}
    res = requests.patch(f"{BASE_URL}/api/v1/books/999999", json=payload)
    assert res.status_code == 404


def test_del_book():
    res = add_book()
    location = res.headers["Location"]

    res = requests.delete(f"{BASE_URL}{location}")
    assert res.status_code == 204

    res = requests.delete(f"{BASE_URL}{location}")
    assert res.status_code == 404