import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import json

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
@app.route("/insert_record", methods=['POST'])
def insert_record():
    builds = mongo.db.builds

    bodykit = mongo.db.bodykit.find()
    engine = mongo.db.engine.find()
    running = mongo.db.runninggear.find()
    interior = mongo.db.interior.find()

    record = {
        'build_name': request.form.get('build_name'),
        'total': request.form.get('total'),
        'car': {
            'make': request.form.get('make'),
            'model': request.form.get('model'),
            'trim': request.form.get('trim'),
            'year': request.form.get('year'),
            'price': request.form.get('price')
        },
    }

   # Adds Bodykit collection to record 
    bodykit_dict = {}
    for item in bodykit:
        bodykit_dict.update({
            item["part_id"]: {
            'product': request.form.get('bodykit_'+item["part_id"]+'_product'),
            'link': request.form.get('bodykit_'+item["part_id"]+'_link'),
            'price': request.form.get('bodykit_'+item["part_id"]+'_price')
            }
        })

    record.update({'bodykit': bodykit_dict})
        
    # Adds Engine collection to record 
    engine_dict = {}
    for item in engine:
        engine_dict.update({
            item["part_id"]: {
            'product': request.form.get('engine_'+item["part_id"]+'_product'),
            'link': request.form.get('engine_'+item["part_id"]+'_link'),
            'price': request.form.get('engine_'+item["part_id"]+'_price')
            }
        })

    record.update({'engine': engine_dict})

    # Adds Running Gear collection to record 
    running_dict = {}
    for item in running:
        running_dict.update({
            item["part_id"]: {
            'product': request.form.get('running_'+item["part_id"]+'_product'),
            'link': request.form.get('running_'+item["part_id"]+'_link'),
            'price': request.form.get('running_'+item["part_id"]+'_price')
            }
        })

    record.update({'running': running_dict})

    # Adds Interior collection to record 
    interior_dict = {}
    for item in interior:
        interior_dict.update({
            item["part_id"]: {
            'product': request.form.get('interior_'+item["part_id"]+'_product'),
            'link': request.form.get('interior_'+item["part_id"]+'_link'),
            'price': request.form.get('interior_'+item["part_id"]+'_price')
            }
        })

    record.update({'interior': interior_dict})
    builds.insert_one(record)

    return redirect(url_for('builds'))

# View a Record
@app.route("/view/<build_id>")
def view_record(build_id):
    build = mongo.db.builds.find_one({
        "_id": ObjectId(build_id)
    })

    bodykit = mongo.db.bodykit.find()
    engine = mongo.db.engine.find()
    running = mongo.db.runninggear.find()
    interior = mongo.db.interior.find()

    return render_template("view.html", build=build, bodykit=bodykit, engine=engine, running=running, interior=interior)

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

    return render_template("edit.html", build=build, bodykit=list(bodykit), engine=list(engine), running=list(running), interior=list(interior))

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