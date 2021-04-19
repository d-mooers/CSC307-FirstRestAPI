from flask import Flask, request, jsonify
from flask_cors import CORS
import json

import random
from model_mongodb import User
app = Flask(__name__)
CORS(app)

users = { 'users_list' : []}
@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        search_username = request.args.get('name')
        search_job = request.args.get('job')
        if search_username and search_job:
            users = User().find_by_name_job(search_username, search_job)
        elif search_username:  # updated for db_access
            users = User().find_by_name(search_username)
        elif search_job:
            users = User().find_by_job(search_job)
        else:  # updated for db_access
            users = User().find_all()
        return {"users_list": users}
    elif request.method == 'POST':
        userToAdd = request.get_json()
        # updated for db_access
        # make DB request to add user
        newUser = User(userToAdd)
        newUser.save()
        resp = jsonify(newUser), 201
        return resp


@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
    if request.method == 'GET':
       # update for db access
        user = User({"_id": id})
        if user.reload():
            return user
        else:
            return jsonify({"error": "User not found"}), 404
    elif request.method == 'DELETE':
        toRemove = User({"_id": id})
        resp = toRemove.remove()
        if resp.deleted_count == 1:
            return jsonify({}), 204
        return jsonify({"error": "User not found"}), 404