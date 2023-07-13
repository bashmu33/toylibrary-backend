from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from .helper import validate_model
from app.models.user import User
from app.models.toy import Toy
from datetime import datetime, timedelta




users_bp = Blueprint('users', __name__, url_prefix='/users')

# @users_bp.route('', methods=['GET'])
# def get_all_users():
#     users = User.query.all()

#     users_response = [user.to_dict() for user in users]

#     return jsonify(users_response)

# @users_bp.route('/<user_id>', methods=['GET'])
# def get_one_user(user_id):
#     user = validate_model(User, user_id)

#     return jsonify(user.to_dict())

# @users_bp.route('/<user_id>/holds', methods=['GET'])
# def get_user_holds(user_id):
#     user = validate_model(User, user_id)
#     holds = user.toys_on_hold

#     holds_response = [toy.to_dict() for toy in holds]

#     return jsonify(holds_response)

# @users_bp.route('/<user_id>/checked_out', methods=['GET'])
# def get_user_checked_out_toys(user_id):
#     user = validate_model(User, user_id)
#     checked_out_toys = user.checked_out_toys

#     checked_out_toys_response = [toy.to_dict() for toy in checked_out_toys]

#     return jsonify(checked_out_toys_response)

# @users_bp.route('/<user_id>/checked_out_history', methods=['GET'])
# def get_user_checked_out_history(user_id):
#     user = validate_model(User, user_id)
#     checked_out_history = user.checked_out_history

#     checked_out_history_response = [history.to_dict() for history in checked_out_history]

#     return jsonify(checked_out_history_response)

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

@users_bp.route('/<int:user_id>/check_out/<int:toy_id>', methods=['POST'])
def check_out_toy(user_id, toy_id):
    user = User.query.get(user_id)
    toy = Toy.query.get(toy_id)

    if user and toy:
        if toy.checked_out_by_user_id is None and toy.toy_status != 'checked_out':
            if len(user.toys_checked_out) < 4:
                toy.checked_out_by_user_id = user.user_id
                toy.toy_status = 'checked_out'

                # Calculate due date as 4 weeks from the check-out date
                check_out_date = datetime.now().date()
                due_date = check_out_date + timedelta(weeks=4)

                db.session.commit()

                return jsonify({
                    'message': 'Toy checked out successfully.',
                    'check_out_date': check_out_date,
                    'due_date': due_date
                })
            else:
                return jsonify({'message': 'User has reached the maximum limit of checked-out toys.'}), 400
        else:
            return jsonify({'message': 'The toy is already checked out.'}), 400
    else:
        return jsonify({'message': 'Invalid user or toy.'}), 400
    
@users_bp.route('/<int:user_id>/toys_checked_out', methods=['GET'])
def get_toys_checked_out_by_user(user_id):
    user = User.query.get(user_id)

    if user:
        toys_checked_out = user.toys_checked_out
        toy_list = [toy.to_dict() for toy in toys_checked_out]
        return jsonify({'toys_checked_out': toy_list})
    else:
        return jsonify({'message': 'Invalid user.'}), 400














