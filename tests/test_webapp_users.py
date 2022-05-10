import pytest
import webapp
from flask_pymongo import PyMongo
from flask import session
import io
from bson.objectid import ObjectId
from tests.test_webapp_fixtures import *

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
        == 404
    )

    # clean up code
    webapp.mongo.db.users.delete_one({"username": ""})


def test_user_edit_page(client):
    """
    check that users can edit their accounts
    edit page is correctly returned
    """
    assert client.get("/profile/edit").status_code == 200
    assert b"<body>" in client.get("/profile/edit").data

    # this will make sure client data is on the page automatically
    assert b"value=name" in client.get("/profile/edit", subdomain="blue").data


def test_user_edit_put(client, pet):
    """this will make sure the client can post new data"""

    pet_id = pet.get('_id')
    request = client.post(
        "/profile/edit",
        subdomain="blue",
        data={
            "username": "name",
            "password": {
                "$binary": {
                    "base64": "Z0FBQUFBQmllYmRPUEN0VkE5eTJiTGthTlBVekFpZUUyZGVrRU1ZUmxxa3llTWJrTTRsMWJjT1B5R1dKc0hsQ2FheE42SnhvNXM2ZWhkZEJuc3p1VUR4RDBCM0I5em0tS0E9PQ==",
                    "subType": "00",
                }
            },
            "shelter_name": "UPDATED",
            "email": "name@my.bcit.ca",
            "street": "UPDATED",
            "city": "UPDATED",
            "province": "UPDATED",
            "postal": "UPDATED",
            "phone": "UPDATED",
        },
    )

    # redirect to the profile page
    assert request.status_code == 302

    # this will check that the profile page has been changed
    assert b"UPDATED" in client.get("/profile", subdomain="blue").data

    # this will check that pet contact info is updated
    assert b"UPDATED" in client.get(f"/adopt/{pet_id}")

    # clean up

    webapp.mongo.db.pets.delete_one(
        {"_id": ObjectId("6279b0cb5ddd36ffc185525b")})
