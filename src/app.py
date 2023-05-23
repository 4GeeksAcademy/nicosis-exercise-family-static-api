"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)

# 1 GET /members
@app.route('/members', methods=['GET'])
def get_members():

    members = jackson_family.get_all_members()
    return jsonify('pediste un get', members), 200

# 2 GET /member/<int:member_id>
@app.route('/members/<int:member_id>', methods=['GET'])
def get_member_id(member_id):

    member = jackson_family.get_member(member_id)
    return jsonify('pediste un get por ID', member), 200

# 3 POST /member
@app.route('/members', methods=['POST'])
def add_member():

    response_body = request.get_json()
    jackson_family.add_member(response_body)
    print(response_body)
    return jsonify('has hecho un post', response_body), 200

# 4 DELETE /member/<int:member_id>

@app.route('/members/<int:member_id>', methods=['DELETE'])
def del_member(member_id):
    deleted_member = jackson_family.get_member(member_id)

    if deleted_member is None:
       return jsonify({'error': f'no existe el id: {member_id}'}), 400

    jackson_family.delete_member(member_id)
    return jsonify({'msg': f'has borrado el member: {member_id}'}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

# para trabajar desde la terminal
    personas = [
        {
            "first_name": "John",
            "age": 33,
            "lucky_numbers": [7, 13, 22]
        },
        {
            "first_name": "Jane",
            "age": 35,
            "lucky_numbers": [10, 14, 3]
        },
        {
            "first_name": "Jimmy",
            "age": 5,
            "lucky_numbers": [1]
        }
    ]

    for p in personas:
        jackson_family.add_member(p)
