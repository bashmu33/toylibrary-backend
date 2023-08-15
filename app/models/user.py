from app import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firebase_uid = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    date_of_birth = db.Column(db.Date)
    email = db.Column(db.String)
    phone_number = db.Column(db.String)
    transactions = db.relationship('Transaction', backref='user', lazy=True)



    def to_dict(self):
        return {
            'user_id': self.user_id,
            'firebase_uid': self.firebase_uid,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.strftime('%Y-%m-%d'),
            'email': self.email,
            'phone_number': self.phone_number,
        }

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            firebase_uid=data_dict['firebase_uid'],
            first_name=data_dict['first_name'],
            last_name=data_dict['last_name'],
            date_of_birth=data_dict['date_of_birth'],
            email=data_dict['email'],
            phone_number=data_dict['phone_number'],
        )