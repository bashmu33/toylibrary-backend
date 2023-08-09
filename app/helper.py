from flask import abort, make_response, jsonify
from app import db
from datetime import datetime, timedelta
from app.models.transaction import Transaction
from app.models.toy import Toy
from app.models.user import User
from vonage import Client, Sms
from datetime import datetime, timedelta

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({'message':f'{cls.__name__} {model_id} invalid'}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({'message':f'{cls.__name__} {model_id} not found'}, 404))
    
    return model


def remove_expired_reservations():
    four_days_ago = datetime.now().date() - timedelta(days=4)
    transactions_to_delete = Transaction.query.filter(
    Transaction.checkout_date.is_(None), Transaction.reserve_date <= four_days_ago
    ).all()


    for transaction in transactions_to_delete:
        #makes toy abailable again after 4 days
        toy = Toy.query.get(transaction.toy_id)
        toy.toy_status = "available"
        db.session.delete(transaction)

    db.session.commit()

def validate_user_by_firebase_uid(firebase_uid):
    try:
        # Print a message before attempting to establish the database connection
        print("Attempting to establish database connection...")

        user = User.query.filter_by(firebase_uid=firebase_uid).first()

        # Print a message after attempting to establish the database connection
        print("Database connection established.")

        if not user:
            print("User not found for firebase_uid:", firebase_uid)
            abort(make_response({'message': 'User not found'}, 404))

        return user
    except Exception as e:
        # Print any exceptions that occur during the process
        print("Exception occurred:", e)
        raise e


# def send_due_date_sms(user_phone_number, api_key, api_secret, vonage_number):
#     client = Client(key=api_key, secret=api_secret)
#     due_date = datetime.now().date() + timedelta(days=2)
#     message = f"Reminder: Your toy is due on {due_date}. Please return it on time."

#     sms = Sms(client=client)
#     response = sms.send_message({
#         'from': vonage_number,
#         'to': user_phone_number,
#         'text': message
#     })

#     return response



