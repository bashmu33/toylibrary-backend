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


#Delete a reservation
@transactions_bp.route('/<user_id>/remove_reservation/<toy_id>', methods=['DELETE'])
def remove_reservation(user_id, toy_id):
    transaction = Transaction.query.filter_by(user_id=user_id, toy_id=toy_id, checkout_date=None).first()

    if not transaction:
        return jsonify({'message': 'Reservation not found for the specified user and toy'}), 404

    toy = Toy.query.get(toy_id)

    if toy.toy_status == "checked_out":
        return jsonify({'message': f'Toy with ID {toy_id} is currently checked out and the reservation cannot be removed'}), 400

    try:
        db.session.delete(transaction)
        toy.toy_status = "available"  # Change the toy status to "available"
        db.session.commit()
        return jsonify({'message': 'Reservation has been removed successfully'}), 200
    except Exception as e:
        abort(make_response({'details': str(e)}, 500))


#return a toy route
@transactions_bp.route('/return_toy/<toy_id>', methods=['POST'])
def return_toy(toy_id):
    try:
        transaction = Transaction.query.filter(
            Transaction.toy_id == toy_id,
            Transaction.checkout_date.isnot(None),
            Transaction.return_date.is_(None)
        ).first()

        if not transaction:
            return jsonify({'message': 'Transaction not found for the specified toy'}), 404

        transaction.return_date = date.today()
        toy = Toy.query.get(toy_id)
        toy.toy_status = "available"

        db.session.commit()

        return jsonify({'message': 'Toy has been returned successfully and is now available for others to reserve/checkout'}), 200
    except Exception as e:
        db.session.rollback()
        abort(make_response({'details': str(e)}, 500))



#get all transactions by user
@transactions_bp.route('/user/<user_id>', methods=['GET'])
def get_transactions_by_user(user_id):
    user = validate_model(User, user_id)

    
    transactions = Transaction.query.filter_by(user_id=user_id).all()


    transactions_response = []
    for transaction in transactions:
        toy = Toy.query.get(transaction.toy_id)
        status = 'reserved' if transaction.reserve_date else 'checked_out'
        transaction_info = {
            'transaction_id': transaction.transaction_id,
            'toy_id': toy.toy_id,
            'toy_name': toy.toy_name,
            'status': status,
            'reserve_date': transaction.reserve_date,
            'checkout_date': transaction.checkout_date,
            'due_date': transaction.due_date,
            'return_date': transaction.return_date,
            'overdue_fines': transaction.overdue_fines,
        }
        transactions_response.append(transaction_info)

    return jsonify(transactions_response)

#DELETES ALL TRANSACTIONS!!
@transactions_bp.route('/delete_all', methods=['DELETE'])
def delete_all_transactions():
    try:
        # Get all transactions and delete them
        transactions = Transaction.query.all()
        Transaction.query.delete()

        # Update toy statuses to "available" for transactions with valid toy_id
        for transaction in transactions:
            if transaction.toy_id is not None:
                toy = Toy.query.get(transaction.toy_id)
                toy.toy_status = "available"

        db.session.commit()

        return jsonify({'message': 'All transactions have been deleted, and toy statuses set to "available" successfully'}), 200
    except Exception as e:
        db.session.rollback()
        abort(make_response({'details': str(e)}, 500))



#REMOVES ALL RESERVATIONS!!!
@transactions_bp.route('/remove_all_reservations', methods=['POST'])
def remove_all_reservations():
    try:
        # Get all reservations
        reservations = Transaction.query.filter_by(checkout_date=None).all()

        # Update toy statuses to "available" for reservations
        for reservation in reservations:
            toy = Toy.query.get(reservation.toy_id)
            toy.toy_status = "available"

        db.session.commit()

        return jsonify({'message': 'Toy statuses for all reservations have been set to "available" successfully'}), 200
    except Exception as e:
        db.session.rollback()
        abort(make_response({'details': str(e)}, 500))

@transactions_bp.route('/user/<user_id>/checkouts', methods=['GET'])
def get_user_checkouts(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).filter(Transaction.checkout_date != None).all()
    checkouts = [transaction.to_dict() for transaction in transactions]
    return jsonify(checkouts), 200

@transactions_bp.route('/user/<user_id>/reservations', methods=['GET'])
def get_user_reservations(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id, checkout_date=None).all()
    reservations = [transaction.to_dict() for transaction in transactions]
    return jsonify(reservations), 200


