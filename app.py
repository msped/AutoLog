import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.secret_key = '7764d031a1424bf8b12357f7ebb05681'
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
    return render_template("builds.html", **content, builds=builds.mongo.db.builds.find())

@app.route("/contact_us")
def contact():

    content = {
        "title": "Contact Us",
        "files": "contact"
    }
    return render_template("contact.html", **content)

@app.route("/register", methods=['GET', 'POST'])
def register():
    
    content = {
        "title": "Register",
        "files": "register"
    }
    return render_template("register.html", **content)

@app.route("/login", methods=['POST', 'GET'])
def login():
    
    if request.method == 'POST':

        pass

    content = {
        "title": "Login",
        "files": "login"
    }
    return render_template("login.html", **content)

@app.route("/logout")
def logout():
    
    pass

@app.route("/edit/<build_id>")
def edit_record(build_id):
    build = mongo.db.builds.find_one({
        "_id": ObjectId(build_id)
    })
    content = {
        "title": "Edit a Build",
        "files": "edit"
    }
    return render_template("edit.html", **content, builds=build)

## CRUD Routes

@app.route("/create_record")
def create_record():
    bodykit = mongo.db.bodykit.find()
    engine = mongo.db.engine.find()
    running = mongo.db.runninggear.find()
    interior = mongo.db.interior.find()

    content = {
        "title": "Create a Build",
        "files": "create"
    }
    return render_template("create.html", **content, bodykit=bodykit, engine=engine, running=running, interior=interior)

@app.route("/insert_record", methods=["POST"])
def insert_record():
    builds = mongo.db.builds
    builds.insert_one(request.form.to_dict())

    redirect(url_for('builds'))

@app.route("/update_record")
def update_record():

    pass

@app.route("/delete_record/<build_id>")
def delete_record(build_id):
    mongo.db.builds.remove({
        '_id': ObjectId(build_id)
    })
    return redirect(url_for('builds'))

##if __name__ == '__main__':
    ##app.run(host=os.environ.get('IP'),
    ##    port=int(os.environ.get('PORT')),
    ##    debug=True)

if __name__ == '__main__':
    app.run(debug=True)