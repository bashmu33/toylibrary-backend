from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from .helper import validate_model, remove_expired_reservations
from app.models.user import User
from app.models.toy import Toy
from app.models.transaction import Transaction
from datetime import date, datetime, timedelta


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

#reserve a toy
@users_bp.route('/<user_id>/reserve/<toy_id>', methods=['POST'])
def reserve_toy(user_id, toy_id):
    user = validate_model(User, user_id)
    toy = validate_model(Toy, toy_id)

    if toy.toy_status == "checked_out":
        return jsonify({'message': f'Toy with ID {toy_id} is currently checked out and unavailable for reservation'}), 400
    elif toy.toy_status == "reserved":
        return jsonify({'message': f'Toy with ID {toy_id} is already reserved and unavailable for reservation'}), 400

    new_transaction = Transaction(user_id=user_id, toy_id=toy_id, reserve_date=datetime.now().date())
    db.session.add(new_transaction)

    toy.toy_status = "reserved"
    db.session.commit()

    return jsonify({'message': f'Toy with ID {toy_id} has been reserved by user with ID {user_id}'}), 200

#check out a toy
@users_bp.route('/<user_id>/checkout/<toy_id>', methods=['POST'])
def checkout_toy(user_id, toy_id):
    user = validate_model(User, user_id)
    toy = validate_model(Toy, toy_id)

    if toy.toy_status == "checked_out":
        return jsonify({'message': f'Toy with ID {toy_id} is already checked out'}), 400

    if toy.toy_status == "available":
        #Checking out toy
        checkout_date = datetime.now().date()
        due_date = checkout_date + timedelta(days=28)
        new_transaction = Transaction(user_id=user_id, toy_id=toy_id, checkout_date=checkout_date, due_date=due_date)
        db.session.add(new_transaction)
        toy.toy_status = "checked_out"
    else:
        #check if toy is reserved here
        existing_reservation = Transaction.query.filter_by(user_id=user_id, toy_id=toy_id, checkout_date=None).first()
        if existing_reservation:
            existing_reservation.checkout_date = datetime.now().date()
            existing_reservation.due_date = existing_reservation.checkout_date + timedelta(days=28)
            toy.toy_status = "checked_out"
        else:
            # below the toy is reserved by a different user so it cant be checked out
            return jsonify({'message': f'Toy with ID {toy_id} is reserved by another user'}), 400

    db.session.commit()

    return jsonify({'message': f'Toy with ID {toy_id} has been checked out by user with ID {user_id}'}), 200

#get all fines
@users_bp.route('/<user_id>/fines', methods=['GET'])
def calculate_fines(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    fines = 0.0
    for transaction in user.transactions:
        if transaction.checkout_date and transaction.return_date and isinstance(transaction.return_date, date):
            due_date = date.fromisoformat(transaction.due_date) if isinstance(transaction.due_date, str) else transaction.due_date
            if transaction.return_date > due_date:
                days_overdue = (transaction.return_date - due_date).days
                fines += 0.25 * days_overdue

    return jsonify({'user_id': user_id, 'fines': fines})




