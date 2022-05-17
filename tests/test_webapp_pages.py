import pytest
import webapp
from flask_pymongo import PyMongo
from flask import session
import io
from bson.objectid import ObjectId
from tests.test_webapp_fixtures import *

# general users page checks


def test_homepage(client):
    """checks that the homepage is working"""
    assert client.get("/").status_code == 200
    assert b'<main>' in client.get("/").data

    # check errors
    request = client.delete("/")
    assert request.status_code == 405


def test_post_homepage(client, pet):
    """test searching on the home page"""
    pet  # init the pet fixture

    # test the search is returning the pet
    request = client.post(
        "/", data={"search": "pet_gender"})
    assert request.status_code == 200
    assert b"6279b0cb5ddd36ffc185525b" in request.data

    # check that the search empty is working
    request_none = client.post(
        "/", data={"search": ""})
    assert request_none.status_code == 200
    assert b"6279b0cb5ddd36ffc185525b" in request.data

    # clean up
    webapp.mongo.db.pets.delete_one(
        {"_id": ObjectId("6279b0cb5ddd36ffc185525b")})


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


def test_user_edit_page(client):
    """edit page is correctly returned"""
    assert client.get("/profile/edit").status_code == 200
    assert b"<body>" in client.get("/profile/edit").data

    # this will make sure client values are set on the page automatically
    assert b'value=' in client.get(
        "/profile/edit", subdomain="blue").data


def test_info(client):
    """test the info return from the login page"""
    assert client.get("/info").status_code == 200
    assert b"<main" in client.get("/info").data


# pet pages

def test_add_pet_form(client):
    assert b"<form" in client.get("/add").data
