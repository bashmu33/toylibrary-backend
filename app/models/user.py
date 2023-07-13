from app import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    date_of_birth = db.Column(db.Date)
    email = db.Column(db.String)
    phone_number = db.Column(db.String)
    address = db.Column(db.String, nullable=True)
    pin = db.Column(db.Integer)
    toys_checked_out = db.relationship('Toy', backref='user', lazy=True, cascade="all, delete-orphan")  # One-to-many relationship

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.strftime('%Y-%m-%d'),
            'email': self.email,
            'phone_number': self.phone_number,
            'address': self.address
        }

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            username=data_dict['username'],
            first_name=data_dict['first_name'],
            last_name=data_dict['last_name'],
            date_of_birth=data_dict['date_of_birth'],
            email=data_dict['email'],
            phone_number=data_dict['phone_number'],
            address=data_dict.get('address'),
            pin=data_dict['pin']
        )

