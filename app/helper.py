from flask import abort, make_response, jsonify
from app import db
from datetime import datetime, timedelta
from app.models.transaction import Transaction
from app.models.toy import Toy
from app.models.user import User


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

        user = User.query.filter_by(firebase_uid=firebase_uid).first()

        if not user:
            print("User not found for firebase_uid:", firebase_uid)
            abort(make_response({'message': 'User not found'}, 404))

        return user
    except Exception as e:
        
        print("Exception occurred:", e)
        raise e




