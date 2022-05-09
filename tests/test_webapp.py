import pytest
import webapp
from flask_pymongo import PyMongo
from flask import session
import io


@pytest.fixture
def client():
    # Creates the test environment

    # make the test database
    webapp.app.config[
        "MONGO_URI"
    ] = "mongodb://acit2911:acit2911@acit-shard-00-00.czvf4.mongodb.net:27017,acit-shard-00-01.czvf4.mongodb.net:27017,acit-shard-00-02.czvf4.mongodb.net:27017/pet-test?ssl=true&replicaSet=atlas-11g06a-shard-0&authSource=admin&retryWrites=true&w=majority"

    webapp.app.secret_key = 'top secret'

    return webapp.app.test_client()


def test_homepage(client):
    """checks that the homepage is working"""
    assert client.get("/").status_code == 200
    assert b'<main class="pet-list">' in client.get("/").data


def test_login(client):
    """makes sure the login page is being sent"""
    assert client.get("/login").status_code == 200
    assert b'<main class="login-form">' in client.get("/login").data


def test_logout(client):
    """check the logout"""

    assert client.get("/logout").status_code == 302


def test_image_not_found(client):
    """test image not found"""
    assert client.get("/file/NA").status_code == 404


def test_remove_pet(client):
    """test deleting a pet"""
    assert client.get("/remove/nan").status_code == 404


def test_signup(client):
    """test the return of the sign up page"""
    assert client.get("/signup").status_code == 200
    assert b'<main class="signup-page">' in client.get("/signup").data


def test_info(client):
    """test the info return from the login page"""
    assert client.get("/info").status_code == 200
    assert b'<main' in client.get("/info").data


def test_sign_up(client):
    """checks the sign up form"""
    webapp.mongo.db.users.delete_one({"username": ""})
    assert client.post("/signup/accounts", data={
        "username": "",
        "password": "password",
        "shelter name": "shelter name",
        "email": "email",
        "street": "street",
        "city": "city",
        "province": "province",
        "postal": "zipcode",
        "phone": "phone",
    }).status_code == 302

    # this will crash because a user in the system with this name already exists
    assert client.post("/signup/accounts", data={
        "username": "",
        "password": "password",
        "shelter name": "shelter name",
        "email": "email",
        "street": "street",
        "city": "city",
        "province": "province",
        "postal": "zipcode",
        "phone": "phone",
    }).status_code == 404
    webapp.mongo.db.users.delete_one({"username": ""})


def test_full_pet(client):
    """this will test adding a pet, editing it, and removing it"""

    start = client.get("/").data

    with client.session_transaction() as session:

        session["user"] = {"username": "name"}
        request = client.post("/add/newPet", content_type="multipart/form-data", data={
            "pet_name": "",
            "pet_gender": "",
            "pet_species": "",
            "pet_age": "",
            "pet_description": "",
            'myfile': (io.BytesIO(b"some initial text data"), "file_name")
        })

        assert start not in request.data


# this code can be used to set session data
# with client.session_transaction(subdomain='blue') as session:
#     session["user"] = 123
