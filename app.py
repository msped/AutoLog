import os
import json
from flask import Flask, render_template, redirect, request, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
from flask_pymongo import PyMongo
import bcrypt
from bson.objectid import ObjectId

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.secret_key = '7764d031a1424bf8b12357f7ebb05681'
app.config["MONGO_DBNAME"] = os.getenv("MONGO_DBNAME")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)


# Classes
class User(UserMixin):

    def __init__(self, email, username, user_id):
        self.email = email
        self.username = username
        self._id = user_id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self._id

    @staticmethod
    def validate_login(password, password_hash):
        password_check = bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        return password_check


@login_manager.user_loader
def load_user(email):
    u = mongo.db.users.find_one({'email': email})
    if not u:
        return None
    return User(u['email'], u['username'], u['_id'])


# Site Routes
@app.route("/")
def home():
    return render_template("home.html")


# All public builds
@app.route("/builds")
def builds():
    builds = mongo.db.builds

    users_builds = builds.find({'visibility': 'Public'})

    return render_template("builds.html", builds=users_builds)


# Users builds
@app.route("/builds/<user_id>")
@login_required
def my_builds(user_id):
    builds = mongo.db.builds
    builds_average_cost = builds.aggregate([
        {
            '$group': {
                '_id': '$author',
                'average_build_cost': {
                    '$avg': '$total'
                }
            }
        }
    ])

    users_builds = builds.find({'author': ObjectId(user_id)})

    return render_template("my_builds.html", builds=users_builds, builds_average_cost=list(builds_average_cost))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email_exists = mongo.db.users.find_one({'email': request.form.get('email')})
        if email_exists is None:
            password = request.form.get('password')
            confirm_password = request.form.get('confirm-password')
            if password == confirm_password:
                hashed_pwd = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt())
                mongo.db.users.insert_one({
                    'username': request.form.get('username'),
                    'email': request.form.get('email'),
                    'password': hashed_pwd.decode('utf-8')
                })
                flash('Account created!', category='success')
                return redirect(url_for('login'))
        else:
            flash('User already exists', category="danger")        
        return redirect(url_for('register'))       
    return render_template("register.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = mongo.db.users.find_one({'email': request.form.get('email')})
        if user is not None:
            if str(user['email']) == str(request.form.get('email')):
                if User.validate_login(request.form.get('password'), user['password']):
                    user_obj = User(user['email'], user['username'])
                    login_user(user_obj)
                    flash("Logged in successfully", category='success')
                    return redirect(url_for('builds'))
                else:
                    flash("Incorrect E-mail/Password", category='danger')
            else: 
                flash("Incorrect E-mail/Password", category='danger')
        else:
            flash("Incorrect E-mail/Password", category='danger')
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out Successfully', category='success')
    return redirect(url_for('login'))

# CRUD Routes


# Create a Record
@app.route("/build/new", methods=['POST', 'GET'])
@login_required
def create_record():
    exterior = mongo.db.exterior.find()
    engine = mongo.db.engine.find()
    running = mongo.db.runninggear.find()
    interior = mongo.db.interior.find()

    if request.method == 'POST':
        builds = mongo.db.builds

        users = [str(current_user.email), ]

        record = {
            'author': current_user._id,
            'build_name': request.form.get('build_name'),
            'total': float(request.form.get('total')),
            'visibility': request.form.get('visibility'),
            'car': {
                'make': request.form.get('make'),
                'model': request.form.get('model'),
                'trim': request.form.get('trim'),
                'year': request.form.get('year'),
                'price': float(request.form.get('price'))
            },
            'votes': {
                'like': {
                    'count': 1,
                    'users_liked': users
                },
                'dislike': {
                    'count': 0,
                    'users_disliked': []
                }
            },
        }

    # Adds exterior collection to record
        exterior_dict = []
        for item in exterior:
            if request.form.get('exterior_'+item["part_id"]+'_product') is not None:
                exterior_dict.append({
                    item["part_id"]: {
                        'product': request.form.get('exterior_'+item["part_id"]+'_product'),
                        'link': request.form.get('exterior_'+item["part_id"]+'_link'),
                        'price': float(request.form.get('exterior_'+item["part_id"]+'_price'))
                    }
                })

        record.update({'exterior': exterior_dict})

        # Adds Engine collection to record
        engine_dict = []
        for item in engine:
            if request.form.get('engine_'+item["part_id"]+'_product') is not None:
                engine_dict.append({
                    item["part_id"]: {
                        'product': request.form.get('engine_'+item["part_id"]+'_product'),
                        'link': request.form.get('engine_'+item["part_id"]+'_link'),
                        'price': float(request.form.get('engine_'+item["part_id"]+'_price'))
                    }
                })

        record.update({'engine': engine_dict})

        # Adds Running Gear collection to record
        running_dict = []
        for item in running:
            if request.form.get('running_'+item["part_id"]+'_product') is not None:
                running_dict.append({
                    item["part_id"]: {
                        'product': request.form.get('running_'+item["part_id"]+'_product'),
                        'link': request.form.get('running_'+item["part_id"]+'_link'),
                        'price': float(request.form.get('running_'+item["part_id"]+'_price'))
                    }
                })

        record.update({'running': running_dict})

        # Adds Interior collection to record
        interior_dict = []
        for item in interior:
            if request.form.get('interior_'+item["part_id"]+'_product') is not None:
                interior_dict.append({
                    item["part_id"]: {
                        'product': request.form.get('interior_'+item["part_id"]+'_product'),
                        'link': request.form.get('interior_'+item["part_id"]+'_link'),
                        'price': float(request.form.get('interior_'+item["part_id"]+'_price'))
                    }
                })

        record.update({'interior': interior_dict})
        builds.insert_one(record)
        flash('Build Created', category='success')
        return redirect(url_for('builds'))

    return render_template("create.html", exterior=exterior, engine=engine, running=running, interior=interior)


# View a Record
@app.route("/build/<build_id>")
def view_record(build_id):
    build = mongo.db.builds.find_one({
        "_id": ObjectId(build_id)
    })

    exterior = mongo.db.exterior.find()
    engine = mongo.db.engine.find()
    running = mongo.db.runninggear.find()
    interior = mongo.db.interior.find()

    # Check for if user has liked the build already
    if current_user.is_authenticated: 
        liked_length = int(len(build['votes']['like']['users_liked']))

        liked_by = []

        for x in range(0, liked_length):
            user_in_like = build['votes']['like']['users_liked'][x]
            liked_by.append(user_in_like)

        if str(current_user.email) in liked_by: 
            user_liked = True
        else:
            user_liked = False

        disliked_length = int(len(build['votes']['dislike']['users_disliked']))

        disliked_by = []

        for x in range(0, disliked_length):
            user_in_dislike = build['votes']['dislike']['users_disliked'][x]
            disliked_by.append(user_in_dislike)

        if str(current_user.email) in disliked_by: 
            user_disliked = True
        else:
            user_disliked = False
    else: 
        user_liked = True
        user_disliked = True

    return render_template("view.html", build=build, exterior=exterior, engine=engine, running=running, interior=interior, user_liked=user_liked, user_disliked=user_disliked)


# Edit a Record
@app.route("/build/<build_id>/edit", methods=['POST', 'GET'])
@login_required
def edit_record(build_id):

    if request.method == 'POST':
        builds = mongo.db.builds

        exterior = mongo.db.exterior.find()
        engine = mongo.db.engine.find()
        running = mongo.db.runninggear.find()
        interior = mongo.db.interior.find()

        record = {
            'total': float(request.form.get('total')),
            'visibility': request.form.get('visibility'),
            'car': {
                'make': request.form.get('make'),
                'model': request.form.get('model'),
                'trim': request.form.get('trim'),
                'year': request.form.get('year'),
                'price': float(request.form.get('price'))
            },
        }

        # Adds exterior collection to record
        exterior_dict = []
        for item in exterior:
            if request.form.get('exterior_'+item["part_id"]+'_product') is not None:
                exterior_dict.update({
                    item["part_id"]: {
                        'product': request.form.get('exterior_'+item["part_id"]+'_product'),
                        'link': request.form.get('exterior_'+item["part_id"]+'_link'),
                        'price': float(request.form.get('exterior_'+item["part_id"]+'_price'))
                    }
                })

        record.update({'exterior': exterior_dict})

        # Adds Engine collection to record
        engine_dict = []
        for item in engine:
            if request.form.get('engine_'+item["part_id"]+'_product') is not None:
                engine_dict.update({
                    item["part_id"]: {
                        'product': request.form.get('engine_'+item["part_id"]+'_product'),
                        'link': request.form.get('engine_'+item["part_id"]+'_link'),
                        'price': float(request.form.get('engine_'+item["part_id"]+'_price'))
                    }
                })

        record.update({'engine': engine_dict})

        # Adds Running Gear collection to record
        running_dict = []
        for item in running:
            if request.form.get('running_'+item["part_id"]+'_product') is not None:
                running_dict.update({
                    item["part_id"]: {
                        'product': request.form.get('running_'+item["part_id"]+'_product'),
                        'link': request.form.get('running_'+item["part_id"]+'_link'),
                        'price': float(request.form.get('running_'+item["part_id"]+'_price'))
                    }
                })

        record.update({'running': running_dict})

        # Adds Interior collection to record
        interior_dict = []
        for item in interior:
            if request.form.get('interior_'+item["part_id"]+'_product') is not None:
                interior_dict.update({
                    item["part_id"]: {
                        'product': request.form.get('interior_'+item["part_id"]+'_product'),
                        'link': request.form.get('interior_'+item["part_id"]+'_link'),
                        'price': float(request.form.get('interior_'+item["part_id"]+'_price'))
                    }
                })

        record.update({'interior': interior_dict})

        # Update in Mongo
        builds.update({"_id": ObjectId(build_id)}, {'$set': record}) 
        flash('Build Updated', category='warning')
        return redirect(url_for('view_record', build_id=build_id))

    build = mongo.db.builds.find_one({
        "_id": ObjectId(build_id)
    })

    exterior = mongo.db.exterior.find()
    engine = mongo.db.engine.find()
    running = mongo.db.runninggear.find()
    interior = mongo.db.interior.find()

    return render_template("edit.html", build=build, exterior=list(exterior), engine=list(engine), running=list(running), interior=list(interior))


# Delete a record
@app.route("/build/<build_id>")
@login_required
def delete_record(build_id):
    mongo.db.builds.remove({
        '_id': ObjectId(build_id)
    })
    flash('Build Deleted', category='danger')
    return redirect(url_for('builds'))


# Votes
@app.route('/build/like/<build_id>', methods=['POST'])
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

    if current_user.email in liked_by:
        result = True 

    else: 
        likes_number = current_build['votes']['like']['count']

        result = likes_number + 1 

        build.update_one({"_id": ObjectId(build_id)}, {'$set': {'votes.like.count': result}}) 
        build.update_one({"_id": ObjectId(build_id)}, {'$push': {'votes.like.users_liked': str(current_user.email)}}) 

    return str(result)


@app.route('/build/dislike/<build_id>', methods=['POST'])
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

    if current_user.email in disliked_by:
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
                {'$sort': {'votes.like.count': -1}}
            ]
        )

    if sort_option == "low_to_high":
        sort_results = builds.aggregate(
            [
                {'$sort': {'votes.like.count': 1}}
            ]
        )

    builds_average_cost = builds.aggregate([
        {
            '$group': {
                '_id': '$author',
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
                '_id': '$author',
                'average_build_cost': {
                    '$avg': '$total'
                }
            }
        }
    ])

    return render_template('builds.html', builds=sort_results, builds_average_cost=list(builds_average_cost))


@app.route('/get_cars')
def get_cars():

    builds = mongo.db.builds

    get_cars = builds.find({'author': current_user._id})

    buildData = []

    for item in get_cars:
        buildData.append({
            'make': item['car']['make'],
            'total': str(item['total'])
        })

    return jsonify(buildData)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=False)

##if __name__ == '__main__':
##    app.run(debug=True)