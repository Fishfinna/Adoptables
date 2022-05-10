import pytest
import webapp
from flask_pymongo import PyMongo
from flask import session
from bson.objectid import ObjectId

# fixtue data


@pytest.fixture
def client():
    # Creates the test environment

    client = webapp.app.test_client()

    with client.session_transaction(subdomain="blue") as session:
        # assume that a user is signed in
        session["user"] = {"username": "name", "password": b"password"}

    return client


@pytest.fixture
def pet():
    """
    This will create and return a pet document
    make sure you delete it at the end of use!!!
    """
    # clear any that currently exist
    webapp.mongo.db.pets.delete_one(
        {"_id": ObjectId("6279b0cb5ddd36ffc185525b")})

    # make only one
    webapp.mongo.db.pets.insert_one(
        {
            "_id": ObjectId("6279b0cb5ddd36ffc185525b"),
            "name": "pet_name",
            "gender": "pet_gender",
            "species": "dog",
            "age": "pet_age",
            "description": "pet_description",
            "image": "filename",
            "data": b"123",
            "shelter_username": "name",
        }
    )

    selected_pet = webapp.mongo.db.pets.find_one(
        {"_id": ObjectId("6279b0cb5ddd36ffc185525b")}
    )

    return selected_pet


@pytest.fixture
def user():
    """
    This will create and return a user document
    make sure you delete it at the end of use!!!
    """

    webapp.mongo.db.users.insert_one(
        {
            "username": "name",
            "password": b"Z0FBQUFBQmllYmRPUEN0VkE5eTJiTGthTlBVekFpZUUyZGVrRU1ZUmxxa3llTWJrTTRsMWJjT1B5R1dKc0hsQ2FheE42SnhvNXM2ZWhkZEJuc3p1VUR4RDBCM0I5em0tS0E9PQ==",
            "shelter_name": "sad place",
            "email": "name@my.bcit.ca",
            "street": "123Rd",
            "city": "TOWN",
            "province": "BC",
            "postal": "V0P  2o2",
            "phone": "123 123 123",
        }
    )

    return webapp.mongo.db.users.find_one({"username": "name"})
