from flask import Flask, render_template, session, request, redirect, url_for, flash, Response
from flask_pymongo import PyMongo
import pymongo
import pymongo.errors
from bson import json_util
from bson.objectid import ObjectId
import bcrypt
import json
import os
import datetime
from collections import Counter

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/book"
app.config["SECRET_KEY"] = b'\xcb\xe8\xff\x88I\xeb\r\x0084&\xca~\xb7\x075\xef\xb2\x16\x95\xe2MLR'
mongo = PyMongo(app)

# Session(app)

with app.app_context():
    mongo.db.users.create_index("username", unique=True)
    app.secret_key = b'\xcb\xe8\xff\x88I\xeb\r\x0084&\xca~\xb7\x075\xef\xb2\x16\x95\xe2MLR'


@app.route('/', methods=['GET'])
def index():
    # Hashing password
    hash_pw = bcrypt.hashpw("hellothereakira".encode("utf-8"), bcrypt.gensalt(10))
    print(bcrypt.checkpw("hellothereakira".encode("utf-8"), hash_pw))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        get_username = mongo.db.users.find_one({'username': request.form['username']})
        if bcrypt.checkpw(request.form['password'].encode("utf-8"), get_username['password']):
            session['user'] = request.form['username']
            session['login'] = True
            return redirect(url_for('dashboard'))
        else:
            return "wrong"
        # hash_password = bcrypt.hashpw(request.form['password'].encode("utf-8"), bcrypt.gensalt(10))
    else:
        return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout_user():
    session.pop('user', None)
    session.pop('login', False)
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    if 'login' in session:
        products = mongo.db.products.find({})
        transaction = mongo.db.transaction.find({})
        return render_template('dashboard.html', user=session['user'], products=products, transactions=transaction)
    else:
        return redirect(url_for('login_user'))


@app.route('/api/products/all', methods=['GET'])
def products_all():
    # TODO: move api key to .env or json file
    API_KEY_VALUE = 'test'
    auth = request.headers.get('x-api-key')
    if auth == API_KEY_VALUE:
        if mongo.db.products.count() > 0:
            products = mongo.db.products.find({})
            return Response(json_util.dumps({
                "data": products,
                "status": 200
            }), mimetype='application/json', status=200)
        else:
            return Response(json_util.dumps({
                "message": "No content available.",
                "status": 203
            }), mimetype='application/json', status=203)

    return Response(json_util.dumps({
            "message": "Invalid API key",
            "status": 403
        }), mimetype='application/json', status=403)


@app.route('/create/product', methods=['POST'])
def create_product():
    if 'login' in session:
        if request.method == 'POST':
            mongo.db.products.insert({
                "name": request.form['name'],
                "quantity": int(request.form['quantity']),
                "price": float(request.form['price']),
                "description": request.form['description'],
                "currency": request.form['currency']
            })
            return redirect(url_for('dashboard'))
    return Response(json_util.dumps({
            "message": "Forbidden",
            "status": 401
        }), mimetype='application/json', status=401)


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    error = None
    if request.method == 'POST':
        if request.form['password'] == request.form['confirm_password']:
            try:
                hash_password = bcrypt.hashpw(request.form['password'].encode("utf-8"), bcrypt.gensalt(10))
                mongo.db.users.insert({"username": request.form["username"], "password": hash_password})
                return "Success"
            except pymongo.errors.DuplicateKeyError:
                error = "Please choose a unique username!"
                flash(error)
                return render_template('register.html', error=error)
        else:
            error = "The password you type in does not match"
            flash(error)
            return render_template('register.html', error=error)
    else:
        return render_template('register.html', error=error)


@app.route('/shop', methods=['GET'])
def shop():
    products = mongo.db.products.find({})
    return render_template('shop.html', products=products)


# TODO: Implement purchase method. Break down dashboard page
@app.route('/dashboard/purchases', methods=['GET', 'POST'])
def purchases():
    pass


# TODO: Implement products method. Break down dashboard page
@app.route('/dashboard/products', methods=['GET', 'POST'])
def products():
    pass


@app.route('/checkout', methods=['POST'])
def checkout():
    if request.method == 'POST':
        data = request.get_json()
        get_id_array = []
        counts = dict()
        # Get only id
        for product in data['cart']:
            get_id_array.append(product['name'])

        for i in get_id_array:
            counts[i] = counts.get(i, 0) + 1
        print(counts)
        # mongo.db.transaction.insert({
        #     "profile": session['login'] and session['user'] or "Guest",
        #     "cart": data['cart'],
        #     "total": float(data['price'])
        # })
        for item in data['cart']:
            checkout_list = list(mongo.db.products.find({'_id': ObjectId(item['id'])}))
            for val in checkout_list:
                if val['quantity'] > 0:
                    pass
                    # mongo.db.products.find_one_and_update(
                    #     {'_id': ObjectId(item['id'])},
                    #     {"$inc": {"quantity": -1}}
                    # )
                # TODO: Implement a message to warn the user that the product is out of stock
                else:
                    print("Out of stock")
        return redirect(url_for('dashboard'))


# app.route('/blog/<post>')
@app.route('/blog', methods=['GET'])
def show_post():
    # data = mongo.db.post.insert({"name": "My first post " + post, "date": datetime.datetime.now()})
    # list_post = mongo.db.post.find()
    # print(list_post[0]['_id'])
    return render_template('blog.html')


if __name__ == "__main__":
    app.run(debug=True)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
