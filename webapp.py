from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file
import json
from flask_pymongo import PyMongo
from python.pet import Pet
from bson.objectid import ObjectId
from cryptography.fernet import Fernet
import random
import string


app = Flask(__name__)

# Mongo Setup
app.config["MONGO_URI"] = "mongodb://acit2911:acit2911@acit-shard-00-00.czvf4.mongodb.net:27017,acit-shard-00-01.czvf4.mongodb.net:27017,acit-shard-00-02.czvf4.mongodb.net:27017/pet-app?ssl=true&replicaSet=atlas-11g06a-shard-0&authSource=admin&retryWrites=true&w=majority"
mongo = PyMongo(app)


@app.route('/file/<filename>')
def file(filename):
    """This will hosts binary images for us"""
    return mongo.db.pets.find_one({"image": filename})['data']


@app.route("/")
def homepage():
    '''home page'''
    pets = [Pet(*x.values()) for x in mongo.db.pets.find({})]
    return render_template("homepage.html", pets=list(pets))


@app.route("/info")
def infopage():
    """learn more page"""
    return render_template("info.html")


@app.route("/adopt/<string:id>")
def petpage(id):
    """idividual pet page"""
    selected = mongo.db.pets.find_one({"_id": ObjectId(id)})
    pet = Pet(*selected.values())
    return render_template("pet.html", pet=pet)


@app.route("/remove/<id>", methods=["GET", "POST"])
def delete_pet(id):
    """this will delete pets and redirect to home"""
    mongo.db.pets.delete_one({"_id": ObjectId(id)})
    return redirect("/")


@app.route("/add")
def addpet():
    """Add a pet form page """
    return render_template("add.html")


@app.route("/add/newPet", methods=["POST"])
def pet_manage_adder():
    """Manages the file storage"""
    if "myfile" in request.files:
        pet_photo = request.files["myfile"]  # this is a files object

        mongo.db.pets.insert_one({
            "name": request.form.get("pet_name"),
            "gender": request.form.get("pet_gender"),
            "species": request.form.get("species"),
            "age": request.form.get("pet_age"),
            "description": request.form.get("pet_description"),
            # these two are for the image information:
            "image": ''.join(random.sample(string.ascii_letters+string.digits, 20)) + pet_photo.filename,
            "data": pet_photo.read()
        })

    return redirect('/')


@app.route("/edit/<id>")
def editpet(id):
    """this will desplay the currently selected pet"""
    selected = mongo.db.pets.find_one({"_id": ObjectId(id)})
    pet = Pet(*selected.values())
    return render_template("edit.html", pet=pet)


@app.route("/edit/<id>/put", methods=["POST"])
def pet_manage_edit(id):
    """This will be the update pet page output"""
    selected = mongo.db.pets.find_one_or_404({"_id": ObjectId(id)})

    pet_data = selected["data"]
    image_name = selected["image"]
    if request.files["myfile"]:
        pet_photo = request.files["myfile"]
        image_name = ''.join(random.sample(
            string.ascii_letters+string.digits, 20)) + pet_photo.filename
        pet_data = pet_photo.read()

    update_selected = {"$set": {
        # the following object will replace that pet
        "name": request.form.get("pet_name"),
        "gender": request.form.get("pet_gender"),
        "species": request.form.get("species"),
        "age": request.form.get("pet_age"),
        "description": request.form.get("pet_description"),
        # these two are for the image information:
        "image": image_name,
        "data": pet_data
    }}

    mongo.db.pets.update_one(selected, update_selected)

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
