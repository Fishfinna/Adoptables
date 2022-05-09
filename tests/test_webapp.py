import pytest
import webapp
from flask_pymongo import PyMongo
from flask import session
import io


@pytest.fixture
def client():
    # Creates the test environment

    client = webapp.app.test_client()

    with client.session_transaction(subdomain='blue') as session:
        # assume that a user is signed in
        session["user"] = {"username": "name", "password": b"password"}

    return client

# general users


def test_homepage(client):
    """checks that the homepage is working"""
    assert client.get("/").status_code == 200
    assert b'<main class="pet-list">' in client.get("/").data

# profile details


def test_login_page(client):
    """makes sure the login page is being sent"""
    assert client.get("/login").status_code == 200
    assert b'<main class="login-form">' in client.get("/login").data


def test_logout_page(client):
    """check the logout"""

    assert client.get("/logout").status_code == 302


def test_signup(client):
    """test the return of the sign up page"""
    assert client.get("/signup").status_code == 200
    assert b'<main class="signup-page">' in client.get("/signup").data


# test adding a user


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

    # clean up code
    webapp.mongo.db.users.delete_one({"username": ""})


# pet manipulation

def test_remove_pet(client):
    """test deleting a pet"""
    assert client.get("/remove/nan").status_code == 404


def test_info(client):
    """test the info return from the login page"""
    assert client.get("/info").status_code == 200
    assert b'<main' in client.get("/info").data


def test_add_pet(client):
    """this will test adding a pet"""

    request = client.post("/add/newPet", content_type="multipart/form-data", subdomain='blue', data={
        "pet_name": "",
        "pet_gender": "",
        "species": "dog",
        "pet_age": "",
        "pet_description": "",
        'myfile': (io.BytesIO(b"some initial text data"), "file_name")
    })

    assert request.status_code == 302


def test_edit_pet(client):
    """
    test editing a pet
    this test is meant to be run after the add pet test
    """

    selected_pet = webapp.mongo.db.pets.find_one(
        {"data": b"some initial text data"})

    pet_id = str(selected_pet.get('_id'))

    # check that the edit page is available
    request_page = client.get(f"/edit/{pet_id}")
    assert request_page.status_code == 200
    assert b'<form method="post"' in request_page.data

    # check that we can put edited content
    request_update = client.post(f"/edit/{pet_id}/put", content_type="multipart/form-data", subdomain='blue', data={
        "pet_name": "Updated Name",
        "pet_gender": "",
        "species": "dog",
        "pet_age": "",
        "pet_description": "",
        'myfile': (io.BytesIO(b"some initial text data"), "file_name")
    })

    assert request_update.status_code == 302
    # makes sure the data is posted to the website
    assert b'Updated Name' in client.get("/").data
    assert b'Updated Name' in client.get(f"/adopt/{pet_id}").data


def test_images(client):
    """test image not found"""
    pet = webapp.mongo.db.pets.find_one(
        {"data": b"some initial text data"})

    # make sure it fails with broken links
    assert client.get("/file/IM-BROKEN!!!!").status_code == 404

    # make sure it can find image data
    assert b'some initial text data' in client.get(
        f"/file/{pet.get('image')}").data


def test_delete(client):
    pet = webapp.mongo.db.pets.find_one(
        {"data": b"some initial text data"})

    # make sure errors are being thrown here
    assert client.get("/remove/IM-BROKEN!!!!").status_code == 404

    # check that the user can delete the added pet
    assert client.post(f"/remove/{pet.get('_id')}",
                       subdomain='blue').status_code == 302
