import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.getenv("MONGO_DBNAME")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

## Site Routes
@app.route("/")
def home():

    content = {
        "title": "Home",
        "files": "home"
    }
    return render_template("home.html", **content)

@app.route("/builds")
def builds():

    content = {
        "title": "Builds",
        "files": "builds"
    }
    ##return render_template("builds.hmtl", content)
    pass

@app.route("/contact_us")
def contact():

    content = {
        "title": "Contact Us",
        "files": "contact"
    }
    ##return render_template("contact.hmtl", content)
    pass

@app.route("/register")
def register():

    content = {
        "title": "Register",
        "files": "register"
    }
    ##return render_template("register.hmtl", content)
    pass

@app.route("/login")
def login():

    content = {
        "title": "Login",
        "files": "login"
    }
    ##return render_template("register.hmtl", content)
    pass

## CRUD Routes



##if __name__ == '__main__':
    ##app.run(host=os.environ.get('IP'),
    ##    port=int(os.environ.get('PORT')),
    ##    debug=True)

if __name__ == '__main__':
    app.run(debug=True)