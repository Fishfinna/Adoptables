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


if __name__ == "__main__":
    app.run(debug=True)
