import os
from flask import (
    Flask, render_template, redirect, request, url_for, flash, jsonify, Markup)
from flask_login import (
        LoginManager,
        UserMixin,
        current_user,
        login_user,
        login_required,
        logout_user
    )
from flask_pymongo import PyMongo
import bcrypt
from bson.objectid import ObjectId
from utils import votes

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.secret_key = os.getenv("SECERT_KEY")
app.config["MONGO_DBNAME"] = os.getenv("MONGO_DBNAME")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)


# Classes
class User(UserMixin):
    """User Class as defined by flask-login"""
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
        return self.email

    @staticmethod
    def validate_login(password, password_hash):
        password_check = bcrypt.checkpw(password.encode('utf-8'),
                                        password_hash.encode('utf-8'))
        return password_check


@login_manager.user_loader
def load_user(email):
    u = mongo.db.users.find_one({'email': email})
    if not u:
        return None
    return User(u['email'], u['username'], u['_id'])


@app.route("/")
def home():
    """Route to Home Page"""
    return render_template("home.html")


@app.route("/builds")
def builds():
    """Route to builds page, shows all public builds"""
    builds = mongo.db.builds

    users_builds = builds.find({'visibility': 'Public'})

    return render_template("builds.html", builds=users_builds)


@app.route("/build/user/<user_id>")
@login_required
def my_builds(user_id):
    """Route to users builds page, all builds (public or private)"""
    build_count = mongo.db.builds.count_documents({
                                                  'author': ObjectId(user_id)})

    if build_count > 0:
        users_builds = mongo.db.builds.find({'author': ObjectId(user_id)})
    else:
        users_builds = False

    return render_template("my_builds.html", builds=users_builds)


@app.route("/register", methods=['GET', 'POST'])
def register():
    """Route to Regsiter page, also handles registration via POST"""
    if current_user.is_authenticated:
        return redirect(url_for('builds'))
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            user = mongo.db.users.count_documents({'email': email})
            if user > 0:
                flash_message = Markup(
                    'User already exists, <a href="/login"' +
                    'class="alert-link">Login here.</a>')
                flash(flash_message, category="danger")
            else:
                username = request.form.get('username')
                user = mongo.db.users.count_documents({'username': username})
                if user > 0:
                    flash('Username already exists.', category='danger')
                    return redirect(url_for('register'))
                else:
                    password = request.form.get('password')
                    confirm_password = request.form.get('confirm-password')
                    if password == confirm_password:
                        hashed_pwd = bcrypt.hashpw(
                                password=password.encode('utf-8'),
                                salt=bcrypt.gensalt()
                            )
                        mongo.db.users.insert_one({
                            'username': request.form.get('username'),
                            'email': request.form.get('email'),
                            'password': hashed_pwd.decode('utf-8')
                        })
                        flash('Account created!', category='success')
                        return redirect(url_for('login'))
                    else:
                        flash('Passwords did not match', category='danger')
            return redirect(url_for('register'))
    return render_template("register.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    """Route to Login Page, also handles login via POST"""
    if current_user.is_authenticated:
        return redirect(url_for('builds'))
    else:
        if request.method == 'POST':
            user = mongo.db.users.find_one({'email':
                                            request.form.get('email')})
            if user is not None:
                if str(user['email']) == str(request.form.get('email')):
                    if User.validate_login(request.form.get('password'),
                                           user['password']):
                        user_obj = User(user['email'],
                                        user['username'], user['_id'])
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
    """Logout user"""
    logout_user()
    flash('Logged out Successfully', category='success')
    return redirect(url_for('login'))


@app.route("/build/new", methods=['POST', 'GET'])
@login_required
def create_record():
    """Route to create a new build,
    also handle the database record creation via POST"""
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
            product = request.form.get('exterior_'+item["part_id"]+'_product')
            if product is not None:
                exterior_dict.append({
                    item["part_id"]: {
                        'product': product,
                        'link': request.form.get(
                                'exterior_'+item["part_id"]+'_link'
                            ),
                        'price': float(request.form.get(
                                'exterior_'+item["part_id"]+'_price'
                            ))
                    }
                })

        record.update({'exterior': exterior_dict})

        # Adds Engine collection to record
        engine_dict = []
        for item in engine:
            product = request.form.get('engine_'+item["part_id"]+'_product')
            if product is not None:
                engine_dict.append({
                    item["part_id"]: {
                        'product': product,
                        'link': request.form.get(
                                'engine_'+item["part_id"]+'_link'
                            ),
                        'price': float(request.form.get(
                                'engine_'+item["part_id"]+'_price'
                            ))
                    }
                })

        record.update({'engine': engine_dict})

        # Adds Running Gear collection to record
        running_dict = []
        for item in running:
            product = request.form.get('running_'+item["part_id"]+'_product')
            if product is not None:
                running_dict.append({
                    item["part_id"]: {
                        'product': product,
                        'link': request.form.get(
                                'running_'+item["part_id"]+'_link'
                            ),
                        'price': float(request.form.get(
                                'running_'+item["part_id"]+'_price'
                            ))
                    }
                })

        record.update({'running': running_dict})

        # Adds Interior collection to record
        interior_dict = []
        for item in interior:
            product = request.form.get('interior_'+item["part_id"]+'_product')
            if product is not None:
                interior_dict.append({
                    item["part_id"]: {
                        'product': product,
                        'link': request.form.get(
                                'interior_'+item["part_id"]+'_link'
                            ),
                        'price': float(request.form.get(
                                'interior_'+item["part_id"]+'_price'
                            ))
                    }
                })

        record.update({'interior': interior_dict})
        builds.insert_one(record)
        flash('Build Created', category='success')
        return redirect(url_for('builds'))

    return render_template("create.html", exterior=exterior, engine=engine,
                           running=running, interior=interior)


@app.route("/build/<build_id>")
def view_record(build_id):
    """Route to view a builds base on build_id"""
    build = mongo.db.builds.find_one({
        "_id": ObjectId(build_id)
    })

    exterior = mongo.db.exterior.find()
    engine = mongo.db.engine.find()
    running = mongo.db.runninggear.find()
    interior = mongo.db.interior.find()

    # Check for if user has liked the build already
    if current_user.is_authenticated:
        user_liked = votes(current_user.email,
                           build['votes']['like']['users_liked'])

        user_disliked = votes(
                              current_user.email,
                              build['votes']['dislike']['users_disliked'])
    else:
        user_liked = True
        user_disliked = True

    return render_template("view.html", build=build, exterior=exterior,
                           engine=engine, running=running, interior=interior,
                           user_liked=user_liked, user_disliked=user_disliked)


@app.route("/build/<build_id>/edit", methods=['POST', 'GET'])
@login_required
def edit_record(build_id):
    """Route to edit page, based on build_id
    Also handles the updating of the database via POST"""
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
            product = request.form.get('exterior_'+item["part_id"]+'_product')
            if product is not None:
                exterior_dict.append({
                    item["part_id"]: {
                        'product': product,
                        'link': request.form.get(
                                'exterior_'+item["part_id"]+'_link'
                            ),
                        'price': float(request.form.get(
                                'exterior_'+item["part_id"]+'_price'
                            ))
                    }
                })

        record.update({'exterior': exterior_dict})

        # Adds Engine collection to record
        engine_dict = []
        for item in engine:
            product = request.form.get('engine_'+item["part_id"]+'_product')
            if product is not None:
                engine_dict.append({
                    item["part_id"]: {
                        'product': product,
                        'link': request.form.get(
                                'engine_'+item["part_id"]+'_link'
                            ),
                        'price': float(request.form.get(
                                'engine_'+item["part_id"]+'_price'
                            ))
                    }
                })

        record.update({'engine': engine_dict})

        # Adds Running Gear collection to record
        running_dict = []
        for item in running:
            product = request.form.get('running_'+item["part_id"]+'_product')
            if product is not None:
                running_dict.append({
                    item["part_id"]: {
                        'product': product,
                        'link': request.form.get(
                                'running_'+item["part_id"]+'_link'
                            ),
                        'price': float(request.form.get(
                                'running_'+item["part_id"]+'_price'
                            ))
                    }
                })

        record.update({'running': running_dict})

        # Adds Interior collection to record
        interior_dict = []
        for item in interior:
            product = request.form.get('interior_'+item["part_id"]+'_product')
            if product is not None:
                interior_dict.append({
                    item["part_id"]: {
                        'product': product,
                        'link': request.form.get(
                                'interior_'+item["part_id"]+'_link'
                            ),
                        'price': float(request.form.get(
                                'interior_'+item["part_id"]+'_price'
                            ))
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

    if str(build['author']) != str(current_user._id):
        flash("Whoops, this isn't your build!", category="danger")
        return redirect(url_for('builds'))

    exterior = mongo.db.exterior.find()
    engine = mongo.db.engine.find()
    running = mongo.db.runninggear.find()
    interior = mongo.db.interior.find()

    return render_template("edit.html", build=build, exterior=list(exterior),
                           engine=list(engine), running=list(running),
                           interior=list(interior))


@app.route("/build/<build_id>/delete")
@login_required
def delete_record(build_id):
    """Deletes a build using build_id"""
    build = mongo.db.builds.find_one({'_id': ObjectId(build_id)})

    if str(build['author']) != str(current_user._id):
        flash("Whoops, this isn't your build!", category="danger")
        return redirect(url_for('builds'))

    mongo.db.builds.remove({
        '_id': ObjectId(build_id)
    })
    flash('Build Deleted', category='danger')
    return redirect(url_for('builds'))


@app.route('/build/like/<build_id>', methods=['POST'])
def like_build(build_id):
    """Updates database to show a user has liked a build along with storing
    users email to stop multiple likes by one user. Return vote amount for AJAX
    response to update to most current likes"""
    build = mongo.db.builds

    current_build = build.find_one({
        "_id": ObjectId(build_id)
    })

    liked_by = list(current_build['votes']['like']['users_liked'])

    if current_user.email in liked_by:
        result = True

    else:
        likes_number = current_build['votes']['like']['count']

        result = likes_number + 1

        build.update_one({"_id": ObjectId(build_id)},
                         {'$set': {'votes.like.count': result}})
        build.update_one({"_id": ObjectId(build_id)},
                         {'$push': {'votes.like.users_liked':
                          str(current_user.email)}})

    return str(result)


@app.route('/build/dislike/<build_id>', methods=['POST'])
def dislike_build(build_id):
    """Updates database to show a user has disliked a build along with storing
    users email to stop multiple likes by one user. Return vote amount for AJAX
    response to update to most current dislikes"""
    build = mongo.db.builds

    current_build = mongo.db.builds.find_one({
        "_id": ObjectId(build_id)
    })

    disliked_by = list(current_build['votes']['dislike']['users_disliked'])

    if current_user.email in disliked_by:
        result = True

    else:
        dislikes_number = current_build['votes']['dislike']['count']

        result = dislikes_number + 1

        build.update_one({"_id": ObjectId(build_id)},
                         {'$set': {'votes.dislike.count': result}})
        build.update_one({"_id": ObjectId(build_id)},
                         {'$push': {'votes.dislike.users_disliked':
                          current_user.email}})

    return str(result)


@app.route('/sort_likes', methods=['POST'])
def sort_likes():
    """Sorts builds by likes, high to low and low to high"""
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

    return render_template('builds.html', builds=sort_results)


@app.route('/sort_price', methods=['POST'])
def sort_prices():
    """Sorts builds by price, high to low and low to high"""
    builds = mongo.db.builds

    sort_option = request.form.get('sort_by_price')

    if sort_option == "high_to_low":
        sort_results = builds.aggregate(
            [
                {'$sort': {'total': -1}}
            ]
        )

    if sort_option == "low_to_high":
        sort_results = builds.aggregate(
            [
                {'$sort': {'total': 1}}
            ]
        )

    return render_template('builds.html', builds=sort_results)


@app.route('/get_cars')
def get_cars():
    """Get database information for DC/D3 graph"""
    builds = mongo.db.builds

    get_cars = builds.find({'author': current_user._id})

    buildData = {}

    for item in get_cars:
        buildData.update({
            'make': item['car']['make'],
            'total': str(item['total'])
        })

    return jsonify(buildData)

# if __name__ == '__main__':
#     app.run(host=os.environ.get('IP'),
#             port=int(os.environ.get('PORT')),
#             debug=False)

if __name__ == '__main__':
    app.run(debug=True)
