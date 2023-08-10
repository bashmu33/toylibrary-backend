from dotenv import load_dotenv
load_dotenv() 
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, Transaction
from twilio.rest import Client
import os

# Initialize Twilio client
twilio_client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))

# Define the function to send SMS notifications
def send_sms_notification(phone_number, message):
    # Add "+1" country code to the phone number
    phone_number_with_country_code = "+1" + phone_number
    
    try:
        twilio_client.messages.create(
            body=message,
            from_=app.config['TWILIO_PHONE_NUMBER'],
            to=phone_number_with_country_code 
        )
        print("SMS notification sent successfully.")
    except Exception as e:
        print(f"Error sending SMS notification: {str(e)}")

# Define the function to send due date notifications
def send_due_date_notifications():
    today = datetime.now().date()
    due_date_limit = today + timedelta(days=2)

    transactions_to_notify = Transaction.query.filter_by(due_date=due_date_limit).all()

    for transaction in transactions_to_notify:
        user = User.query.get(transaction.user_id)
        if user and user.phone_number:
            send_sms_notification(user.phone_number, f"Hi {user.first_name}, this is a reminder that your toy is due in 2 days. Please return it on time. - FW Toy Library")

# Set up the scheduler and start it
scheduler = BackgroundScheduler()
scheduler.add_job(send_due_date_notifications, 'interval', days=1)
scheduler.start()

# Run the Flask app
app = create_app()
if __name__ == "__main__":
    app.run()


# #TEST VERSION
# from dotenv import load_dotenv
# load_dotenv() 
# from apscheduler.schedulers.background import BackgroundScheduler
# from datetime import datetime, timedelta
# from app import create_app, db
# from app.models import User, Transaction
# from twilio.rest import Client
# import os

# app = create_app()


# twilio_client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))

# # Create a test version of send_sms_notification
# def send_sms_notification(phone_number, message):
#     # Add "+1" country code to the phone number
#     phone_number_with_country_code = "+1" + phone_number
    
#     # Update the desired phone number here
#     test_phone_number = "+12602417093"
    
#     try:
#         print(f"Sending test SMS to: {test_phone_number}")
#         print(f"Test message: {message}")
#     except Exception as e:
#         print(f"Error sending test SMS: {str(e)}")


# #
# def send_due_date_notifications():
#     today = datetime.now().date()
#     due_date_limit = today + timedelta(days=2)

#     transactions_to_notify = Transaction.query.filter_by(due_date=due_date_limit).all()

#     for transaction in transactions_to_notify:
#         user = User.query.get(transaction.user_id)
#         if user and user.phone_number:
#             send_sms_notification(user.phone_number, f"Hi {user.first_name}, this is a reminder that your toy is due in 2 days. Please return it on time. - The Toy Library")

# #trigger an immediate test notification
# with app.app_context():
#     #TEST USER
#     user = User.query.filter_by(email='test@example.com').first()
#     if not user:
#         user = User(
#             firebase_uid='test_user1',
#             first_name='Test1',
#             last_name='User1',
#             date_of_birth=datetime(2000, 1, 1),
#             email='test1@example.com',
#             phone_number='2602417093'
#         )
#         db.session.add(user)
#         db.session.commit()

#     #TEST TRANSACTION
#     due_date = datetime.now() + timedelta(minutes=5)
#     transaction = Transaction(
#         checkout_date=datetime.now(),
#         due_date=due_date,
#         user_id=user.user_id,
#         toy_id=36  # Replace with the actual toy ID from your database
#     )
#     db.session.add(transaction)
#     db.session.commit()

#     # Send test notification
#     send_sms_notification(user.phone_number, f"Hi {user.first_name}, this is a test notification for your toy that is due soon. Please return it on time. - The Toy Library")

# # Set up the scheduler and start it
# scheduler = BackgroundScheduler()
# scheduler.add_job(send_due_date_notifications, 'interval', days=1)
# scheduler.start()

# # Run the Flask app
# if __name__ == "__main__":
#     app.run()
