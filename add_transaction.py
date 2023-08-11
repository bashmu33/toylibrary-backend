from dotenv import load_dotenv
load_dotenv()

from app import create_app, db  # Import the create_app function and db object
from app.models import Transaction  # Import the necessary model
from datetime import datetime

app = create_app()  # Initialize the Flask app
app.app_context().push()  # Push the app context

# Rest of your code to add the transaction
checkout_date = datetime.now().date()
due_date = datetime.now().date()  
user_id = 35 
toy_id = 44  

# Create a new transaction instance
new_transaction = Transaction(
    checkout_date=checkout_date,
    due_date=due_date,
    user_id=user_id,
    toy_id=toy_id
)

# Add the new transaction to the database session and commit
db.session.add(new_transaction)
db.session.commit()

print("Transaction added successfully.")
