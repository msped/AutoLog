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
    
    builds = mongo.db.builds
    builds_average_cost = builds.aggregate([
        {
            '$group': {
                '_id': 'null',
                'average_build_cost': {
                    '$avg': '$total'
                }
            }
        }
    ])


    return render_template("builds.html", builds=mongo.db.builds.find(), builds_average_cost=list(builds_average_cost))

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

    users_Array = ['Mattex',]

    record = {
        'build_name': request.form.get('build_name'),
        'total': float(request.form.get('total')),
        'car': {
            'make': request.form.get('make'),
            'model': request.form.get('model'),
            'trim': request.form.get('trim'),
            'year': request.form.get('year'),
            'price': request.form.get('price')
        },
        'votes':{
            'like': {
                'count': 1,
                'users_liked': users_Array
            },
            'dislike': {
                'count': 0,
                'users_disliked': []
            }
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

    builds = mongo.db.builds
    bodykit = mongo.db.bodykit.find()
    engine = mongo.db.engine.find()
    running = mongo.db.runninggear.find()
    interior = mongo.db.interior.find()

    #Check for if user has liked the build already 
    liked_length = int(len(build['votes']['like']['users_liked']))

    liked_by = []

    for x in range(0, liked_length):
        user_in_like = build['votes']['like']['users_liked'][x]
        liked_by.append(user_in_like)

    if 'Mattex' in liked_by: 
        user_liked = True
    else:
        user_liked = False

    disliked_length = int(len(build['votes']['dislike']['users_disliked']))

    disliked_by = []

    for x in range(0, disliked_length):
        user_in_dislike = build['votes']['dislike']['users_disliked'][x]
        disliked_by.append(user_in_dislike)

    if 'Mattex' in disliked_by: 
        user_disliked = True
    else:
        user_disliked = False

    return render_template("view.html", build=build, bodykit=bodykit, engine=engine, running=running, interior=interior, user_liked=user_liked, user_disliked=user_disliked)

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
@app.route("/update_record/<build_id>", methods=['POST'])
def update_record(build_id):
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

    # Update in Mongo
    builds.update({"_id": ObjectId(build_id)}, record)  

    return redirect(url_for('view_record', build_id=build_id))

# Delete a record 
@app.route("/delete_record/<build_id>")
def delete_record(build_id):
    mongo.db.builds.remove({
        '_id': ObjectId(build_id)
    })
    return redirect(url_for('builds'))

# Votes 
@app.route('/like_build/<build_id>', methods=['POST'])
def like_build(build_id):
    build = mongo.db.builds

    current_build = mongo.db.builds.find_one({
        "_id": ObjectId(build_id)
    })

    array_length = int(len(current_build['votes']['like']['users_liked']))

    liked_by = []

    for x in range(0, array_length):
        user = current_build['votes']['like']['users_liked'][x]
        liked_by.append(user)

    if 'Currrent User' in liked_by:
        result = True 

    else: 
        likes_number = current_build['votes']['like']['count']

        result = likes_number + 1 

        build.update_one({"_id": ObjectId(build_id)}, {'$set': {'votes.like.count': result}}) 
        build.update_one({"_id": ObjectId(build_id)}, {'$push': {'votes.like.users_liked': 'Mattex'}}) 

    return str(result)

@app.route('/dislike_build/<build_id>', methods=['POST'])
def dislike_build(build_id):
    build = mongo.db.builds

    current_build = mongo.db.builds.find_one({
        "_id": ObjectId(build_id)
    })

    array_length = int(len(current_build['votes']['dislike']['users_disliked']))

    disliked_by = []

    for x in range(0, array_length):
        user = current_build['votes']['dislike']['users_disliked'][x]
        disliked_by.append(user)

    if 'Currrent User' in disliked_by:
        result = True 

    else: 
        dislikes_number = current_build['votes']['dislike']['count']

        result = dislikes_number + 1

        build.update_one({"_id": ObjectId(build_id)}, {'$set': {'votes.dislike.count': result}}) 
        build.update_one({"_id": ObjectId(build_id)}, {'$push': {'votes.dislike.users_disliked': 'Mattex'}}) 

    return str(result)

# Sort on Likes and Price
@app.route('/sort_likes', methods=['POST'])
def sort_likes():

    builds = mongo.db.builds

    sort_option = request.form.get('sort_by_likes')

    if sort_option == "high_to_low":
        sort_results = builds.aggregate(
            [
                {'$sort' : {'votes.like.count': -1}}
            ]
        )

    if sort_option == "low_to_high":
        sort_results = builds.aggregate(
            [
                {'$sort' : {'votes.like.count': 1}}
            ]
        )

    builds_average_cost = builds.aggregate([
        {
            '$group': {
                '_id': 'null',
                'average_build_cost': {
                    '$avg': '$total'
                }
            }
        }
    ])

    return render_template('builds.html', builds=sort_results, builds_average_cost=list(builds_average_cost))

@app.route('/sort_price', methods=['POST'])
def sort_prices():

    builds = mongo.db.builds

    sort_option = request.form.get('sort_by_price')

    if sort_option == "high_to_low":
        sort_results = builds.aggregate(
            [
                {'$sort' : {'total': -1}}
            ]
        )

    if sort_option == "low_to_high":
        sort_results = builds.aggregate(
            [
                {'$sort' : {'total': 1}}
            ]
        )

    builds_average_cost = builds.aggregate([
        {
            '$group': {
                '_id': 'null',
                'average_build_cost': {
                    '$avg': '$total'
                }
            }
        }
    ])

    return render_template('builds.html', builds=sort_results, builds_average_cost=list(builds_average_cost))

##if __name__ == '__main__':
    ##app.run(host=os.environ.get('IP'),
    ##    port=int(os.environ.get('PORT')),
    ##    debug=True)

if __name__ == '__main__':
    app.run(debug=True)