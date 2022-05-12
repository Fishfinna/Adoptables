from flask import (
    Flask,
    flash,
    request,
    session,
    jsonify,
    render_template,
    redirect,
    url_for,
    send_file,
)
import json
from flask_pymongo import PyMongo
from python.pet import Pet
from python.user import User
from bson.objectid import ObjectId
import random
import string

# flask set up
app = Flask(__name__)

# session set up
app.config["SECRET_KEY"] = "shhhhhthisissecret"

# Mongo Setup
app.config[
    "MONGO_URI"
] = "mongodb://acit2911:acit2911@acit-shard-00-00.czvf4.mongodb.net:27017,acit-shard-00-01.czvf4.mongodb.net:27017,acit-shard-00-02.czvf4.mongodb.net:27017/pet-app?ssl=true&replicaSet=atlas-11g06a-shard-0&authSource=admin&retryWrites=true&w=majority"
mongo = PyMongo(app)


@app.route("/file/<filename>")
def file(filename):
    """This will hosts binary images for us"""
    try:
        image = mongo.db.pets.find_one({"image": filename})["data"]
        return image
    except:
        return "404: file not found", 404


@app.route("/")
def homepage():
    """home page"""
    try:
        pets = [Pet(*x.values()) for x in mongo.db.pets.find({})]
        return render_template("homepage.html", pets=list(pets), session=session)
    except:
        return " ", 404


@app.route("/info")
def infopage():
    """learn more page"""
    return render_template("info.html")


@app.route("/adopt/<string:id>")
def adopt_info(id):
    """idividual pet page"""
    selected = mongo.db.pets.find_one_or_404({"_id": ObjectId(id)})
    pet = Pet(*selected.values())
    profile = mongo.db.users.find_one({"username": pet.shelter_username})
    return render_template("pet.html", pet=pet, profile=profile, session=session)


@app.route("/remove/<id>", methods=["GET", "POST"])
def delete_pet(id):
    """this will delete pets and redirect to home"""
    try:
        pet = mongo.db.pets.find_one_or_404({"_id": ObjectId(id)})
        if session["user"].get("username") == pet.get("shelter_username"):
            mongo.db.pets.delete_one({"_id": ObjectId(id)})
            return redirect("/profile")
        else:
            return "404: invalid user permissions", 404
    except:
        return "404: pet not found", 404


@app.route("/add")
def addpet():
    """Add a pet form page"""
    return render_template("add.html", session=session)


@app.route("/add/newPet", methods=["POST"])
def pet_manage_adder():
    """Manages the file storage"""
    if "myfile" in request.files:
        pet_photo = request.files["myfile"]  # this is a files object

        mongo.db.pets.insert_one(
            {
                "name": request.form.get("pet_name"),
                "gender": request.form.get("pet_gender"),
                "species": request.form.get("species"),
                "age": request.form.get("pet_age"),
                "description": request.form.get("pet_description"),
                # these two are for the image information:
                "image": "".join(
                    random.sample(string.ascii_letters + string.digits, 20)
                )
                + pet_photo.filename,
                "data": pet_photo.read(),
                "shelter_username": session["user"].get("username"),
            }
        )

    return redirect("/profile")


@app.route("/edit/<id>")
def editpet(id):
    """this will desplay the currently selected pet"""
    selected = mongo.db.pets.find_one({"_id": ObjectId(id)})
    pet = Pet(*selected.values())
    return render_template("edit.html", pet=pet, session=session)


@app.route("/edit/<id>/put", methods=["POST"])
def pet_manage_edit(id):
    """This will be the update pet page output"""
    selected = mongo.db.pets.find_one_or_404({"_id": ObjectId(id)})

    pet_data = selected["data"]
    image_name = selected["image"]
    if request.files["myfile"]:
        pet_photo = request.files["myfile"]
        image_name = (
            "".join(random.sample(string.ascii_letters + string.digits, 20))
            + pet_photo.filename
        )
        pet_data = pet_photo.read()

    update_selected = {
        "$set": {
            # the following object will replace that pet
            "name": request.form.get("pet_name"),
            "gender": request.form.get("pet_gender"),
            "species": request.form.get("species"),
            "age": request.form.get("pet_age"),
            "description": request.form.get("pet_description"),
            # these two are for the image information:
            "image": image_name,
            "data": pet_data,
        }
    }

    mongo.db.pets.update_one(selected, update_selected)

    return redirect("/profile")


@app.route("/signup")
def signup():
    """
    this will log out the user when they go to the log in screen
    """
    try:
        return render_template("signup.html")
    except:
        return "", 404


@app.route("/signup/accounts", methods=["POST"])
def manage_signup():
    user_data = {
        "username": request.form.get("username"),
        "password": request.form.get("password"),
        "shelter_name": request.form.get("shelter name"),
        "email": request.form.get("email"),
        "street": request.form.get("street"),
        "city": request.form.get("city"),
        "province": request.form.get("province"),
        "postal": request.form.get("zipcode"),
        "phone": request.form.get("phone"),
    }
    if mongo.db.users.find_one({"username": request.form.get("username")}):
        return render_template("invalid_username.html"), 404

    user_account = User(*user_data.values())
    mongo.db.users.insert_one(user_account.get_account())
    selected = mongo.db.users.find_one(
        {"username": request.form.get("username")})
    account = User(*list(selected.values())[1:])
    session["user"] = account.get_account()

    return redirect("/profile")


@app.route("/profile")
def profile():
    try:
        user = session["user"]
        pets = [
            Pet(*x.values())
            for x in mongo.db.pets.find(
                {"shelter_username": session["user"].get("username")}
            )
        ]
        return render_template(
            "profile.html", profile=session["user"], session=session, pets=pets
        )
    except Exception:
        return "error 404: can not find profile", 404


@app.route("/login")
def login():
    """
    this will log out the user when they go to the log in screen
    """
    try:
        session["user"] = None
        return render_template("login.html", session=session)
    except:
        return "", 404


@app.route("/login/manage", methods=["POST"])
def login_manage():
    try:
        selected = mongo.db.users.find_one(
            {"username": request.form.get("username")})
        if selected:
            account = User(*list(selected.values())[1:])

            if account.check_password(
                request.form.get("username"), request.form.get("password")
            ):
                session["user"] = account.get_account()
                return redirect("/profile")
        return render_template("invalid_account.html"), 404
    except:
        return render_template("invalid_account.html"), 404


@app.route("/logout")
def logout():
    """log the user out"""
    if session["user"]:
        # remove their session data
        session["user"] = None
        return redirect("/")
    else:
        return "", 404


@app.route("/profile/edit", methods=["GET", "POST"])
def edit_user():
    """edit the user account"""
    if request.method == "GET":
        return render_template("edit_user.html", user=session["user"])

    elif request.method == "POST":
        selected = mongo.db.users.find_one_or_404(
            {"username": session["user"].get("username")})

        update_selected = update_selected = {
            "$set": {
                "username": session["user"].get("username"),
                "password": session["user"].get("password"),
                "shelter_name": request.form.get("shelter name"),
                "email": request.form.get("email"),
                "street": request.form.get("street"),
                "city": request.form.get("city"),
                "province": request.form.get("province"),
                "postal": request.form.get("zipcode"),
                "phone": request.form.get("phone"),
            }}

        mongo.db.users.update_one(selected, update_selected)

        selected = mongo.db.users.find_one(
            {"username": session["user"].get("username")})
        account = User(*list(selected.values())[1:])

        session["user"] = account.get_account()

        return redirect("/profile")


@ app.route("/profile/delete")
def delete_user():
    """Delete a user and their listed pets from the application"""

    if session["user"]:
        mongo.db.pets.delete_many(
            {"shelter_username": session["user"].get("username")})

        mongo.db.users.delete_one(
            {"username": session["user"].get("username")})
        session["user"] = None

        return redirect("/")
    else:
        return "", 404


if __name__ == "__main__":
    app.run(debug=True)
