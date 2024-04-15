"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

__CONTENT_TYPE= {'Content-Type': 'application/json'}

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
jackson_family.add_member( {"id": jackson_family._generateId(), "name": "John", "age": 33, "lucky_numbers": [7, 13, 22]} )
jackson_family.add_member( {"id": jackson_family._generateId(), "name": "Jane", "age": 35, "lucky_numbers": [10, 14, 3]} )
jackson_family.add_member( {"id": jackson_family._generateId(), "name": "Jimmy", "age": 5, "lucky_numbers": [1]} )

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

############################################################ GET /members
@app.route('/members', methods=['GET'])
def handle_members_get():
    return jsonify(jackson_family.get_all_members()), 200, __CONTENT_TYPE

############################################################ GET /member/<int:id>
@app.route('/member/<int:id>', methods=['GET'])
def handler_member_get(id):
    try:
        member= jackson_family.get_member(id)
        if member[0] != -1:
            return jsonify(member[1]), 200, __CONTENT_TYPE
        else:
            return jsonify({"ERROR": "wrong info"}), 400, __CONTENT_TYPE
    except:
        return jsonify({"ERROR": "server error"}), 500, __CONTENT_TYPE

############################################################ POST /member
@app.route('/member', methods=['POST'])
def handler_member_post():
    try:
        data= request.get_json()
        if data:
            jackson_family.add_member(data)
            return data, 200, __CONTENT_TYPE
        else:
            return jsonify({"ERROR": "wrong info"}), 400, __CONTENT_TYPE
    except:
        return jsonify({"ERROR": "server error"}), 500, __CONTENT_TYPE


############################################################ DELETE /member/<int:id>
@app.route('/member/<int:id>', methods=['DELETE'])
def handler_member_delete(id):
    try:
        result= jackson_family.delete_member(id)
        if result:
            return jsonify({"done": True}), 200, __CONTENT_TYPE
        else:
            return jsonify({"ERROR": "wrong info"}), 400, __CONTENT_TYPE
    except:
        return jsonify({"ERROR": "server error"}), 500, __CONTENT_TYPE

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
