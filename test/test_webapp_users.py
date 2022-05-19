import pytest
import webapp
from flask_pymongo import PyMongo
from flask import session
import io
from bson.objectid import ObjectId
from test.test_webapp_fixtures import *

# test adding a user


def test_sign_up(client):
    """checks the sign up form"""

    # in our app we will require users put names
    # so this will work only in the test environment
    webapp.mongo.db.users.delete_one({"username": ""})
    assert (
        client.post(
            "/signup/accounts",
            data={
                "username": "",
                "password": "password",
                "shelter name": "shelter name",
                "email": "email",
                "street": "street",
                "city": "city",
                "province": "province",
                "postal": "zipcode",
                "phone": "phone",
            },
        ).status_code
        == 302
    )

    # this will crash because a user in the system with this name already exists
    assert (
        client.post(
            "/signup/accounts",
            data={
                "username": "",
                "password": "password",
                "shelter name": "shelter name",
                "email": "email",
                "street": "street",
                "city": "city",
                "province": "province",
                "postal": "zipcode",
                "phone": "phone",
            },
        ).status_code
        == 302
    )

    # clean up code
    webapp.mongo.db.users.delete_one({"username": ""})


def test_user_edit_put(client, pet, user):
    """this will make sure the client can post new data"""

    pet_id = pet.get("_id")
    user_id = user.get("_id")

    request = client.post(
        "/profile/edit",
        subdomain="blue",
        data={
            "username": "name",
            "password": b"Z0FBQUFBQmllYmRPUEN0VkE5eTJiTGthTlBVekFpZUUyZGVrRU1ZUmxxa3llTWJrTTRsMWJjT1B5R1dKc0hsQ2FheE42SnhvNXM2ZWhkZEJuc3p1VUR4RDBCM0I5em0tS0E9PQ==",
            "shelter name": "UPDATED",
            "email": "name@my.bcit.ca",
            "street": "UPDATED",
            "city": "UPDATED",
            "province": "UPDATED",
            "zipcode": "UPDATED",
            "phone": "UPDATED",
        },
    )

    # redirect to the profile page
    assert request.status_code == 302

    # this will check that pet contact info is updated
    assert b"UPDATED" in client.get(f"/adopt/{pet_id}", subdomain="blue").data

    # remove the pet
    webapp.mongo.db.pets.delete_one({"_id": ObjectId("6279b0cb5ddd36ffc185525b")})

    # remove the user
    webapp.mongo.db.users.delete_one({"_id": ObjectId(f"{user_id}")})


def test_delete(client, user, pet):
    """Tests deleting the user"""

    pet_id = pet.get("_id")
    start = user

    # check if the user is there already
    assert b"name@my.bcit.ca" in client.get("/profile", subdomain="blue").data

    # delete account
    assert client.get("/profile/delete", subdomain="blue").status_code == 302

    # check that it's deleted
    assert (
        b"name@my.bcit.ca" not in client.get(f"/adopt/{pet_id}", subdomain="blue").data
    )


def test_login_manager(client):
    """test login"""
    assert b"user can not" in client.post("/login/manage", data={"username": ""}).data


def test_signup_error(client):
    """test the sign up page"""

    with client.session_transaction(subdomain="blue") as session:
        # assume that a user is signed in
        session["error"] = {"error": "IM BROKEN!!! :("}

    assert b"div" in client.get("/signup", subdomain="blue").data
