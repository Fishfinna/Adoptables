from flask import Flask, request, jsonify, render_template, redirect
import requests
import json
from python.app import App


app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("homepage.html", pets=App().pets)


@app.route("/info")
def infopage():
    return render_template("info.html")


@app.route("/adopt/<id>")
def petpage(id):
    select = App().get_by_id(id)
    return render_template("pet.html", pet=select)


@app.route("/remove/<id>", methods=["GET", "POST"])
def delete_pet(id):
    App().delete_by_id(id)
    return redirect("/")


@app.route("/add")
def addpet():
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
