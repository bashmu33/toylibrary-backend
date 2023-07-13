from app import db

class Toy(db.Model):
    toy_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    toy_name = db.Column(db.String)
    description = db.Column(db.String, nullable=True)
    age_category = db.Column(db.String, nullable=True)
    toy_status = db.Column(db.String, default=None)
    toy_hold_number = db.Column(db.Integer, default=0)
    toy_image = db.Column(db.String, nullable=True)
    checked_out_by_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True) 


    def to_dict(self):
        return {
            'toy_id': self.toy_id,
            'toy_name': self.toy_name,
            'description': self.description,
            'age_category': self.age_category,
            'toy_status': self.toy_status,
            'toy_image': self.toy_image
        }

