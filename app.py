import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.secret_key = '7764d031a1424bf8b12357f7ebb05681'
app.config["MONGO_DBNAME"] = os.getenv("MONGO_DBNAME")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

# Site Routes
@app.route("/")
def home():

    content = {
        "title": "Home",
        "files": "home"
    }
    return render_template("home.html", **content)

@app.route("/builds")
def builds():
    
    return render_template("builds.html", builds=mongo.db.builds.find())

@app.route("/contact_us")
def contact():

    return render_template("contact.html", **content)

@app.route("/register", methods=['GET', 'POST'])
def register():
    
    return render_template("register.html", **content)

@app.route("/login", methods=['POST', 'GET'])
def login():
    
    if request.method == 'POST':

        pass

    return render_template("login.html", **content)

@app.route("/logout")
def logout():
    
    pass

# CRUD Routes

# Create a Record
@app.route("/create_record")
def create_record():
    bodykit = mongo.db.bodykit.find()
    engine = mongo.db.engine.find()
    running = mongo.db.runninggear.find()
    interior = mongo.db.interior.find()

    return render_template("create.html", bodykit=bodykit, engine=engine, running=running, interior=interior)

# Insert Record into DB
@app.route("/insert_record", methods=["POST"])
def insert_record():
    builds = mongo.db.builds
    builds.insert_one(request.form.to_dict())

    return redirect(url_for('builds'))

# View a Record
@app.route("/view/<build_id>")
def view_record(build_id):
    build = mongo.db.builds.find_one({
        "_id": ObjectId(build_id)
    })

    return render_template("view.html", builds=build)

# Edit a Record
@app.route("/edit/<build_id>")
def edit_record(build_id):
    build = mongo.db.builds.find_one({
        "_id": ObjectId(build_id)
    })

    bodykit = mongo.db.bodykit.find()
    engine = mongo.db.engine.find()
    running = mongo.db.runninggear.find()
    interior = mongo.db.interior.find()

    return render_template("edit.html", builds=build, bodykit=bodykit, engine=engine, running=running, interior=interior)

# Update a Record
@app.route("/update_record")
def update_record():

    pass

# Delete a record 
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