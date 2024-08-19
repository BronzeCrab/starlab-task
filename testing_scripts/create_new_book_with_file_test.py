import requests

# Making auth:
auth_res = requests.post(
    "http://127.0.0.1:8000/api-token-auth/",
    data={"username": "user_0", "password": "user_0"},
)
assert auth_res.status_code == 200

print("auth res:")
print(auth_res.text)
token = auth_res.json()["token"]


# Creating new Book:
headers = {
    "Authorization": f"Token {token}",
    "Content-type": "application/json",
}
print("headers")
print(headers)

post_book_res = requests.post(
    f"http://127.0.0.1:8000/books/",
    json={
        "title": "New book from test",
        "genre": "genre",
        "authors": [{"name": "author"}],
        "date_published": "2024-08-08",
    },
    headers=headers,
)

print("post_book res:")
print(post_book_res.text)
print(post_book_res.status_code)
assert post_book_res.status_code == 201


# Adding new file to the Book via PATCH:
book_id = post_book_res.json()["id"]
print(f"New created book id: {book_id}")
headers = {
    "Authorization": f"Token {token}",
    "Content-type": "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    "Content-Disposition": "attachment; filename=book_file.pdf",
}
print("headers")
print(headers)

with open("./testing_scripts/some.pdf", "rb") as f:
    patch_book_res = requests.patch(
        f"http://127.0.0.1:8000/books/{book_id}/set_book_file/",
        files={"new_book_file.pdf": f},
        headers=headers,
    )

    print("patch_book res:")
    print(patch_book_res.text)
    print(patch_book_res.status_code)
    assert patch_book_res.status_code == 200
