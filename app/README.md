Toy Library API

The Toy Library API is a web application that allows users to manage a toy library system. It provides endpoints to perform CRUD (Create, Read, Update, Delete) operations on toys, users, and check-out history.
Features

    Add new toys to the library
    View details of a toy
    Update toy information
    Delete a toy from the library
    Register new users
    View user details
    Update user information
    Check out a toy to a user
    View current toys checked out by a user
    Return a toy

Technologies Used

    Python
    Flask - Python web framework
    SQLAlchemy - Object-relational mapping library for database access
    SQLite - Lightweight relational database management system
    Flask-RESTful - Extension for building RESTful APIs with Flask
    Flask-Migrate - Extension for handling database migrations
    Other dependencies can be found in the requirements.txt file

Installation

    Clone the repository:

bash

git clone https://github.com/your-username/toy-library-api.git

    Change to the project directory:

bash

cd toy-library-api

    Create and activate a virtual environment:

bash

python3 -m venv venv
source venv/bin/activate

    Install the dependencies:

pip install -r requirements.txt

    Initialize the database:

csharp

flask db init
flask db migrate
flask db upgrade

    Start the application:

arduino

flask run
