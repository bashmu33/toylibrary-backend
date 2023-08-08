from app import db
from datetime import date, datetime, timedelta

class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    checkout_date = db.Column(db.Date, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    return_date = db.Column(db.Date, nullable=True)
    reserve_date = db.Column(db.Date, nullable=True)
    overdue_fines = db.Column(db.Float, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    toy_id = db.Column(db.Integer, db.ForeignKey('toy.toy_id'), nullable=True)


    def to_dict(self):
        # Convert dates to strings or return None if they are None
        checkout_date_str = self.checkout_date.strftime('%Y-%m-%d') if self.checkout_date else None
        due_date_str = self.due_date.strftime('%Y-%m-%d') if self.due_date else None
        return_date_str = self.return_date.strftime('%Y-%m-%d') if self.return_date else None
        reserve_date_str = self.reserve_date.strftime('%Y-%m-%d') if self.reserve_date else None

        reserve_status = 'reserved' if self.reserve_date and not self.checkout_date else None

        # Calculate overdue fines 
        overdue_fines = 0.0
        if self.checkout_date and self.return_date and self.return_date > self.due_date:
            days_overdue = (self.return_date - self.due_date).days
            overdue_fines = 0.25 * days_overdue

        return {
            'transaction_id': self.transaction_id,
            'checkout_date': checkout_date_str,
            'due_date': due_date_str,
            'return_date': return_date_str,
            'reserve_date': reserve_date_str,
            'overdue_fines': overdue_fines,
            'user_id': self.user_id,
            'toy_id': self.toy_id,
            'reserve_status': reserve_status
        }




