import pytest
import webapp
from flask_pymongo import PyMongo
from flask import session
import io
from bson.objectid import ObjectId
from tests.test_webapp_fixtures import *


# pet manipulation tests

def test_add_pet(client):
    """this will test adding a pet"""

    request = client.post(
        "/add/newPet",
        content_type="multipart/form-data",
        subdomain="blue",
        data={
            "pet_name": "",
            "pet_gender": "",
            "species": "dog",
            "pet_age": "",
            "pet_description": "",
            "myfile": (io.BytesIO(b"some initial text data"), "file_name"),
        },
    )

    assert request.status_code == 302

    # clean up
    webapp.mongo.db.pets.delete_one(
        {"name": "", "gender": "", "species": "dog"})


def test_edit_pet(client, pet):
    """
    test editing a pet
    this test adds a pet and then edits it
    """

    # set up
    pet_id = str(pet.get("_id"))

    # check that the edit page is available
    request_page = client.get(f"/edit/{pet_id}")
    assert request_page.status_code == 200
    assert b'<form method="post"' in request_page.data

    # check that we can put edited content
    request_update = client.post(
        f"/edit/{pet_id}/put",
        content_type="multipart/form-data",
        subdomain="blue",
        data={
            "pet_name": "Updated Name",
            "pet_gender": "",
            "species": "dog",
            "pet_age": "",
            "pet_description": "",
            "myfile": (io.BytesIO(b"some initial text data"), "file_name"),
        },
    )

    # check that everything worked as expected
    assert request_update.status_code == 302

    # makes sure the data is posted to the website
    assert b"Updated Name" in client.get("/").data
    assert b"Updated Name" in client.get(f"/adopt/{pet_id}").data

    # remove the pet
    webapp.mongo.db.pets.delete_one(
        {"_id": ObjectId("6279b0cb5ddd36ffc185525b")})


def test_images(client, pet):
    """test image not found"""

    # make sure it fails with broken links
    assert client.get("/file/IM-BROKEN!!!!").status_code == 404

    # make sure it can find image data
    assert b"123" in client.get(f"/file/{pet.get('image')}").data
    # remove the pet
    webapp.mongo.db.pets.delete_one(
        {"_id": ObjectId("6279b0cb5ddd36ffc185525b")})


def test_delete_error(client):
    # make sure errors are being thrown here
    assert client.get("/remove/IM-BROKEN!!!!").status_code == 404


def test_delete(client, pet):
    pet_id = pet.get("_id")

    # make sure the pet is there to start
    assert client.get(f"/adopt/{pet_id}").status_code == 200

    # check that the user can delete the added pet
    assert client.get(f"/remove/{pet_id}", subdomain="blue").status_code == 302

    # make sure the pet is gone
    assert client.get(f"/adopt/{pet_id}").status_code == 404

    # check that the user can not delete the pet again
    assert client.get(f"/remove/{pet_id}", subdomain="blue").status_code == 404
