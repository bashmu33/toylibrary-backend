from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from .helper import validate_model
from app.models.user import User
from app.models.toy import Toy
from app.models.transaction import Transaction
from datetime import date, datetime

transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')

# GET ALL TRANSACTIONS
@transactions_bp.route('', methods=['GET'])
def get_all_transactions():
    transactions = Transaction.query.all()

    transactions_response = [transaction.to_dict() for transaction in transactions]

    return jsonify(transactions_response)


# DELETE A RESERVATION
@transactions_bp.route('/<user_id>/remove_reservation/<toy_id>', methods=['DELETE'])
def remove_reservation(user_id, toy_id):
    transaction = Transaction.query.filter_by(user_id=user_id, toy_id=toy_id, checkout_date=None).first()

    if not transaction:
        return jsonify({'message': 'Reservation not found for the specified user and toy'}), 404

    try:
        db.session.delete(transaction)
        toy = Toy.query.get(toy_id)
        toy.toy_status = "available"
        db.session.commit()
        return jsonify({'message': 'Reservation has been removed successfully'}), 200
    except Exception as e:
        abort(make_response({'details': str(e)}, 500))

@transactions_bp.route('/<transaction_id>/return_toy', methods=['POST'])
def return_toy(transaction_id):
    transaction = validate_model(Transaction, transaction_id)

    if transaction.return_date is not None:
        return jsonify({'message': 'This toy has already been returned'}), 400

    try:
        transaction.return_date = datetime.now().date()
        db.session.commit()

        toy = Toy.query.get(transaction.toy_id)
        toy.toy_status = "available"
        db.session.commit()

        return jsonify({'message': 'Toy has been returned successfully and is now available for others to reserve/checkout'}), 200
    except Exception as e:
        abort(make_response({'details': str(e)}, 500))

@transactions_bp.route('/user/<user_id>', methods=['GET'])
def get_transactions_by_user(user_id):
    user = validate_model(User, user_id)

    # Fetch all transactions for the user, including associated toy information
    transactions = Transaction.query.filter_by(user_id=user_id).all()

    # Prepare a response JSON containing all relevant information for each transaction
    transactions_response = []
    for transaction in transactions:
        toy = Toy.query.get(transaction.toy_id)
        status = 'reserved' if transaction.reserve_date else 'checked_out'
        transaction_info = {
            'transaction_id': transaction.transaction_id,
            'toy_id': toy.toy_id,
            'toy_name': toy.name,
            'status': status,
            'reserve_date': transaction.reserve_date,
            'checkout_date': transaction.checkout_date,
            'due_date': transaction.due_date,
            'return_date': transaction.return_date,
            'overdue_fines': transaction.overdue_fines,
        }
        transactions_response.append(transaction_info)

    return jsonify(transactions_response)
