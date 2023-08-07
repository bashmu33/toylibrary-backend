from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from .helper import validate_model
from app.models.user import User
from app.models.toy import Toy
from app.models.transaction import Transaction

toys_bp = Blueprint('toys', __name__, url_prefix='/toys')

#GET ALL TOYS
@toys_bp.route('', methods=['GET'])
def get_all_toys():
    name_query = request.args.get("toy_name")
    if name_query:
        toys = Toy.query.filter_by(toy_name = name_query)
    else:
        toys = Toy.query.all()
    results = [toy.to_dict() for toy in toys]
    return jsonify(results), 200

#GET ONE TOY
@toys_bp.route('/<toy_id>', methods=['GET'])
def get_one_toy(toy_id):
    toy = validate_model(Toy, toy_id)

    return jsonify(toy.to_dict())

# #GET TOYS BY NAME
# @toys_bp.route('', methods=["GET"])
# def get_toy_by_name():
#     name_query = request.args.get("toy_name")
#     if name_query:
#         toys = Toy.query.filter_by(toy_name = name_query)
#     results = [toy.to_dict() for toy in toys]
#     return jsonify(results), 200

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
@toys_bp.route('/<toy_id>/confirm_delete', methods=['DELETE'])
def confirm_delete_toy(toy_id):
    toy = validate_model(Toy, toy_id)

    try:
        # Update associated transactions with toy_id set to null
        transactions_to_update = Transaction.query.filter_by(toy_id=toy_id).all()
        for transaction in transactions_to_update:
            transaction.toy_id = None

        # Now delete the toy
        db.session.delete(toy)
        
        # Commit changes
        db.session.commit()

        return jsonify({'message': 'Toy has been deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
