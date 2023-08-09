from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from .helper import validate_model, send_due_date_sms
from app.models.user import User
from app.models.toy import Toy
from app.models.transaction import Transaction
from datetime import date, datetime
from vonage import Client, Sms
from dotenv import load_dotenv
import os

load_dotenv()

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



#return a toy 
@transactions_bp.route('/<transaction_id>/return_toy', methods=['POST'])
def return_toy(transaction_id):
    transaction = validate_model(Transaction, transaction_id)

    if not transaction.checkout_date:
        return jsonify({'message': 'This toy was not checked out and cannot be returned'}), 400

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


def send_due_date_sms(user_phone_number):
    client = Client(key='your_api_key', secret='your_api_secret')  # Replace with your Vonage API credentials

    due_date = datetime.now().date() + timedelta(days=2)
    message = f"Reminder: Your toy is due on {due_date}. Please return it on time."

    sms = Sms(client=client)
    response = sms.send_message({
        'from': 'YourVonageNumber',
        'to': user_phone_number,
        'text': message
    })
print(response) 


@transactions_bp.route('/<transaction_id>/send_due_date_notification', methods=['POST'])
def send_due_date_notification(transaction_id):
    transaction = validate_model(Transaction, transaction_id)
    user = User.query.get(transaction.user_id)

    # Load Vonage API credentials from environment variables
    vonage_api_key = os.environ.get('VONAGE_API_KEY')  # Replace with your actual environment variable names
    vonage_api_secret = os.environ.get('VONAGE_API_SECRET')
    vonage_number = os.environ.get('YOUR_VONAGE_NUMBER')

    # Assuming user_phone_number is a valid phone number stored in the user table
    send_due_date_sms(user.phone_number, vonage_api_key, vonage_api_secret, vonage_number)

    return jsonify({'message': 'Due date notification sent'}), 200
