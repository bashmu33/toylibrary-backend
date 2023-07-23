from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from .helper import validate_model, remove_expired_reservations
from app.models.user import User
from app.models.toy import Toy
from app.models.transaction import Transaction
from datetime import datetime, timedelta


users_bp = Blueprint('users', __name__, url_prefix='/users')



#GET ALL USERS
@users_bp.route('', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_response = [user.to_dict() for user in users]
    return jsonify(users_response)

#GET ONE USER
@users_bp.route('/<user_id>', methods=['GET'])
def get_one_user(user_id):
    user = validate_model(User, user_id)
    return jsonify(user.to_dict())


#CREATE A NEW USER
@users_bp.route('', methods=['POST'])
def create_user():
    request_body = request.get_json()
    try:
        new_user = User.from_dict(request_body)
        db.session.add(new_user)
        db.session.commit()
        return make_response({'new_user': new_user.to_dict()}, 201)
    except KeyError as e:
        abort(make_response({'details': f'Missing field: {str(e)}'}, 400))
    except Exception as e:
        abort(make_response({'details': str(e)}, 400))


@users_bp.route('/<user_id>/reserve/<toy_id>', methods=['POST'])
def reserve_toy(user_id, toy_id):
    user = validate_model(User, user_id)
    toy = validate_model(Toy, toy_id)

    if toy.toy_status != "available":
        return jsonify({'message': f'Toy with ID {toy_id} is not available for reservation'}), 400

    new_transaction = Transaction(user_id=user_id, toy_id=toy_id, reserve_date=datetime.now().date())
    db.session.add(new_transaction)

    toy.toy_status = "unavailable"
    db.session.commit()

    return jsonify({'message': f'Toy with ID {toy_id} has been reserved by user with ID {user_id}'}), 200


@users_bp.route('/<user_id>/return/<transaction_id>', methods=['POST'])
def return_toy(user_id, transaction_id):
    user = validate_model(User, user_id)
    transaction = validate_model(Transaction, transaction_id)

    if transaction.user_id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    if not transaction.checkout_date or transaction.return_date:
        return jsonify({'message': 'Invalid operation. Toy is either not checked out or already returned.'}), 400

    transaction.return_date = datetime.now().date()
    db.session.commit()

    # Update the toy status 
    toy = Toy.query.get(transaction.toy_id)
    toy.toy_status = "available"
    db.session.commit()

    return jsonify({'message': f'Toy with ID {transaction.toy_id} has been returned by User with ID {user_id}'}), 200


