from flask import Flask, request, jsonify
app = Flask(__name__)

users = { 
   'users_list' :
   [
      { 
         'id' : 'xyz789',
         'name' : 'Charlie',
         'job': 'Janitor',
      },
      {
         'id' : 'abc123', 
         'name': 'Mac',
         'job': 'Bouncer',
      },
      {
         'id' : 'ppp222', 
         'name': 'Mac',
         'job': 'Professor',
      }, 
      {
         'id' : 'yat999', 
         'name': 'Dee',
         'job': 'Aspring actress',
      },
      {
         'id' : 'zap555', 
         'name': 'Dennis',
         'job': 'Bartender',
      }
   ]
}

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        name = request.args.get('name')
        job = request.args.get('job')
        if name and job:
            matching = list(filter(lambda p : p["name"] == name and p['job'] == job,
                                   users["users_list"]))
            return {'users_list': matching}
        elif name :
            matching = list(filter(lambda p : p["name"] == name,
                                   users["users_list"]))
            return {'users_list': matching}
        return users
    elif request.method == 'POST':
        newUser = request.get_json()
        users['users_list'].append(newUser)
        resp = jsonify(success=True)
        return resp

@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
    if request.method == 'GET':
        if id :
            for user in users['users_list']:
                if user['id'] == id:
                    return user
            return {}
        return users
    elif request.method == 'DELETE':
        if id :
            users['users_list'] = list(filter(lambda p : p['id'] != id, 
                                         users['users_list']))
            resp = jsonify(success=True)
            return resp
        resp = jsonify(success=False)
        resp.status_code = 401
        return resp