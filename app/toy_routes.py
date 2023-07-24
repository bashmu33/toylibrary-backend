from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from .helper import validate_model
from app.models.user import User
from app.models.toy import Toy

toys_bp = Blueprint('toys', __name__, url_prefix='/toys')

#GET ALL TOYS
@toys_bp.route('', methods=['GET'])
def get_all_toys():
    toys = Toy.query.all()

    toys_response = [toy.to_dict() for toy in toys]

    return jsonify(toys_response)

#GET ONE TOY
@toys_bp.route('/<toy_id>', methods=['GET'])
def get_one_toy(toy_id):
    toy = validate_model(Toy, toy_id)

    return jsonify(toy.to_dict())

#CREATE A NEW TOY
@toys_bp.route('', methods=['POST'])
def create_toy():
    request_body = request.get_json()
    try:
        new_toy = Toy(**request_body)
        db.session.add(new_toy)
        db.session.commit()
        return make_response({'new_toy': new_toy.to_dict()}, 201)
    except KeyError as e:
        abort(make_response({'details': f'Missing field: {str(e)}'}, 400))
    except Exception as e:
        abort(make_response({'details': str(e)}, 400))

#DELETE A TOY FROM THE DATABASE
@toys_bp.route('/<toy_id>', methods=['DELETE'])
def delete_toy(toy_id):
    toy = validate_model(Toy, toy_id)

    try:
        db.session.delete(toy)
        db.session.commit()
        return jsonify({'message': f'Toy with ID {toy_id} has been deleted successfully'}), 200
    except Exception as e:
        abort(make_response({'details': str(e)}, 500))