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
        return render_template("404.html"), 404


@app.route("/", methods=["GET", "POST"])
def homepage():
    """home page"""

    if request.method == "GET":
        try:
            pets = [Pet(*x.values()) for x in mongo.db.pets.find({})]
            return render_template("homepage.html", pets=list(pets), session=session)
        except:
            return render_template("404.html"), 404

    # this will respond to the searching feature
    elif request.method == "POST":
        pets = [Pet(*x.values()) for x in mongo.db.pets.find({})]
        search_pets = [
            pet
            for pet in list(pets)
            if request.form.get("search").upper() in str(pet.to_dict()).upper()
        ]
        if len(search_pets) == 0:
            return render_template(
                "homepage.html",
                pets=list(search_pets),
                session=session,
                error="No pets found",
            )
        return render_template("homepage.html", pets=list(search_pets), session=session)
    else:
        return render_template("404.html", error="method not allowed"), 405


@app.route("/info")
def infopage():
    """learn more page"""
    try:
        return render_template("info.html")
    except:
        return render_template("404.html"), 404


@app.route("/adopt/<string:id>")
def adopt_info(id):
    """shows the individual pet page"""
    try:
        selected = mongo.db.pets.find_one_or_404({"_id": ObjectId(id)})
        pet = Pet(*selected.values())
        profile = mongo.db.users.find_one({"username": pet.shelter_username})
        return render_template("pet.html", pet=pet, profile=profile, session=session)
    except:
        return render_template("404.html"), 404


@app.route("/remove/<id>", methods=["GET", "POST"])
def delete_pet(id):
    """this will delete pets and redirect to home"""
    try:
        pet = mongo.db.pets.find_one_or_404({"_id": ObjectId(id)})
        if session["user"].get("username") == pet.get("shelter_username"):
            mongo.db.pets.delete_one({"_id": ObjectId(id)})
            return redirect("/profile")
        else:
            return render_template("404.html", error="invalid permissions"), 404
    except:
        return render_template("404.html"), 404


@app.route("/add")
def addpet():
    """Add a pet form page"""
    try:
        return render_template("add.html", session=session)
    except:
        return render_template("404.html"), 404


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
    """this will display the currently selected pet"""

    try:
        selected = mongo.db.pets.find_one({"_id": ObjectId(id)})
        pet = Pet(*selected.values())
        return render_template("edit.html", pet=pet, session=session)
    except:
        return render_template("404.html"), 404


@app.route("/edit/<id>/put", methods=["POST"])
def pet_manage_edit(id):
    """This will be the update pet page output"""

    try:
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
    except:
        return render_template("404.html"), 404


@app.route("/signup")
def signup():
    """sets up the sign up page"""
    try:
        if session.get("error"):
            error = session["error"]
            session["error"] = None
            return render_template("signup.html", error=error)
        else:
            return render_template("signup.html")
    except Exception:
        return render_template("404.html", error=Exception), 404


@app.route("/signup/accounts", methods=["POST"])
def manage_signup():
    """manages the sign up data"""

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
        session["error"] = "username taken"
        return redirect("/signup")

    user_account = User(*user_data.values())
    mongo.db.users.insert_one(user_account.get_account())
    selected = mongo.db.users.find_one({"username": request.form.get("username")})
    account = User(*list(selected.values())[1:])
    session["user"] = account.get_account()

    return redirect("/profile")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    """display the current user profile"""
    try:
        user = session["user"]

        # this will create a list of all of the pets that belong to the user
        pets = [
            Pet(*x.values())
            for x in mongo.db.pets.find(
                {"shelter_username": session["user"].get("username")}
            )
        ]
        if request.method == "POST":
            pets = [
                pet
                for pet in list(pets)
                if request.form.get("search").upper() in str(pet.to_dict()).upper()
            ]
            if len(pets) == 0:
                return render_template(
                    "profile.html",
                    profile=user,
                    session=session,
                    pets=pets,
                    error="No pets matching this search can be found",
                )
        return render_template("profile.html", profile=user, session=session, pets=pets)
    except:
        return render_template("404.html", error="profile not found")


@app.route("/login")
def login():
    """let the user login"""
    try:
        session["user"] = None
        return render_template("login.html", session=session)
    except Exception:
        return render_template("404.html"), 404


@app.route("/login/manage", methods=["POST"])
def login_manage():
    """Manages the login of a user"""
    try:
        selected = mongo.db.users.find_one({"username": request.form.get("username")})
        if selected:
            account = User(*list(selected.values())[1:])

            if account.check_password(
                request.form.get("username"), request.form.get("password")
            ):
                session["user"] = account.get_account()
                return redirect("/profile")
        return render_template(
            "login.html", session=session, error="user can not be found"
        )
    except:
        return render_template(
            "login.html", session=session, error="user can not be found"
        )


@app.route("/logout")
def logout():
    """Logs the user out"""

    try:
        if session["user"]:
            session["user"] = None
        return redirect("/")
    except:
        return render_template("404.html", session=session)


@app.route("/profile/edit", methods=["GET", "POST"])
def edit_user():
    """edit the user account"""
    if request.method == "GET":
        return render_template("edit_user.html", user=session["user"])

    elif request.method == "POST":
        selected = mongo.db.users.find_one_or_404(
            {"username": session["user"].get("username")}
        )

        # updates the item
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
            }
        }

        mongo.db.users.update_one(selected, update_selected)

        selected = mongo.db.users.find_one(
            {"username": session["user"].get("username")}
        )
        account = User(*list(selected.values())[1:])

        session["user"] = account.get_account()

        return redirect("/profile")
    else:
        return render_template("login.html", session=session)


@app.route("/profile/delete")
def delete_user():
    """delete a user and their listed pets from the application"""

    try:
        if session["user"]:
            mongo.db.pets.delete_many(
                {"shelter_username": session["user"].get("username")}
            )

            mongo.db.users.delete_one({"username": session["user"].get("username")})
            session["user"] = None

        return redirect("/")
    except:
        return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
