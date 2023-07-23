from app import db
from datetime import datetime, timedelta

class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    checkout_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    reserve_date = db.Column(db.Date)
    overdue_fines = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    toy_id = db.Column(db.Integer, db.ForeignKey('toy.toy_id'), nullable=False)


    def to_dict(self):
        due_date = (self.checkout_date + timedelta(weeks=4)).strftime('%Y-%m-%d') if self.checkout_date else None
        reserve_status = 'reserved' if self.reserve_date and not self.checkout_date else None

        # Calculate overdue fines 
        overdue_fines = 0.0
        if self.checkout_date and self.return_date and self.return_date > due_date:
            days_overdue = (self.return_date - due_date).days
            overdue_fines = 0.25 * days_overdue

        return {
            'transaction_id': self.transaction_id,
            'checkout_date': self.checkout_date.strftime('%Y-%m-%d') if self.checkout_date else None,
            'due_date': due_date,
            'return_date': self.return_date.strftime('%Y-%m-%d') if self.return_date else None,
            'reserve_date': self.reserve_date.strftime('%Y-%m-%d') if self.reserve_date else None,
            'overdue_fines': overdue_fines,
            'user_id': self.user_id,
            'toy_id': self.toy_id,
            'reserve_status': reserve_status
        }
