from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from bson import Binary, Code
import json
from jinja2 import Template
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "secretkey"
app.config['MONGO_URI'] = "mongodb+srv://varghese123:varghese123@cluster0-yqune.mongodb.net/clubManage?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route('/')
def Index():
    clubs = list(mongo.db.club.find())
    resp = loads(dumps(clubs))
    return render_template("index.html", data = resp)

@app.route("/insert",methods=['POST'])
def insert():
    # _json = request.json
    _name = request.form['name']
    _description = request.form['description']
    _category = request.form['category']
    _visibility = request.form['visibility']

    if _name and _description and _category and _visibility and request.method == "POST":
        mongo.db.club.insert(
            {
                'name':_name,
                'description':_description,
                'category':_category,
                'visibility':_visibility
                }
            )
        flash("Data Inserted Successfully")
        # resp.status_code = 200
        return redirect(url_for('Index'))

    else:
        return not_found()

@app.route('/update', methods = ['GET', 'POST'])
def update():

    _id = request.form['id']
    _name = request.form['name']
    _description = request.form['description']
    _category = request.form['category']
    _visibility = request.form['visibility']

    mongo.db.club.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
    {'$set':{'name':_name,'description':_description, 'category':_category, 'visibility':_visibility}})

    flash("Record Updated Successfully")
    return redirect(url_for('Index'))


@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    mongo.db.club.delete_one({'_id':ObjectId(id)})
    flash("Record Deleted Successfully")
 
    return redirect(url_for('Index'))


@app.errorhandler(404)
def not_found(error = None):
    message = {
        'status':404,
        'message':'Not Found'+request.url
    }
    resp = jsonify(message)

    resp.status_code = 404

    return resp      

if __name__ == "__main__":
    app.run(debug=True)