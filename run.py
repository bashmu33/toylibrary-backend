from dotenv import load_dotenv
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, Transaction
from twilio.rest import Client
import os


load_dotenv()

# Initialize the Flask app
app = create_app()


with app.app_context():
   
    twilio_client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))

    # Define the function to send SMS notifications
    def send_sms_notification(phone_number, message):
    # Check if the phone number starts with "+1"
        if not phone_number.startswith("+1"):
            phone_number_with_country_code = '+1' + phone_number
        else:
            phone_number_with_country_code = phone_number
        
        try:
            twilio_client.messages.create(
                body=message,
                from_=os.environ.get('TWILIO_PHONE_NUMBER'),
                to=phone_number_with_country_code  # Use the phone number with country code
            )
            print("SMS notification sent successfully.")
        except Exception as e:
            print(f"Error sending SMS notification: {str(e)}")

    # Define the function to send due date notifications
    def send_due_date_notifications():
        print("Checking due date notifications...")

        due_date_limit = datetime.now().date()
        # due_date_limit = today + timedelta(days=2)

        transactions_to_notify = Transaction.query.filter_by(due_date=due_date_limit).all()

        for transaction in transactions_to_notify:
            user = User.query.get(transaction.user_id)
            if user and user.phone_number:
                print(f"Sending due date notification to {user.phone_number}")
                send_sms_notification(user.phone_number, f"Hi {user.first_name}, this is a reminder that your toy is due in 2 days. Please return it on time. - The FW Toy Library")

    print("Starting the script...")

    # Call the function to send due date notifications
    send_due_date_notifications()






#TEST the functions BELOW

# from dotenv import load_dotenv
# load_dotenv()

# # Initialize the Flask app
# app = create_app()

# # Initialize Twilio client
# twilio_client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))

# # Define the function to send SMS notifications
# def send_sms_notification(phone_number, message):
#     # Add "+1" country code to the phone number
#     phone_number_with_country_code = '+1' + phone_number
    
#     try:
#         twilio_client.messages.create(
#             body=message,
#             from_=os.environ.get('TWILIO_PHONE_NUMBER'),
#             to=phone_number_with_country_code
#         )
#         print("SMS notification sent successfully.")
#     except Exception as e:
#         print(f"Error sending SMS notification: {str(e)}")

# # Define the function to send a test notification immediately
# def send_test_notification():
#     test_phone_number = '2602417093'  # Replace with your test phone number
#     test_message = "This is a test notification for immediate testing."

#     send_sms_notification(test_phone_number, test_message)

# # Call the send_test_notification function to send the immediate test notification
# send_test_notification()




#ANOTHER TEST....#


# from twilio.rest import Client
# import os
# from dotenv import load_dotenv


# load_dotenv()

# # Retrieve Twilio credentials from environment variables
# account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
# auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
# twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')

# # Initialize Twilio client
# client = Client(account_sid, auth_token)

# # Define recipient phone number
# recipient_phone_number = '+12602417093'  # Replace with the recipient phone number you want to use

# # Send a test message
# message = client.messages.create(
#     from_=twilio_phone_number,
#     body='This is a test message from Twilio.',
#     to=recipient_phone_number
# )

# print(message.sid)
