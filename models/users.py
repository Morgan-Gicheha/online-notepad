from main import db
from werkzeug.security import check_password_hash

class Users(db.Model):
    """this class stores all registered users"""
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(20))
    email = db.Column(db.String(80),nullable=False)
    password = db.Column(db.String(),nullable=False)
    todo_ = db.relationship("Todo", backref="user")

    # commit to db

    def create(self):
        db.session.add(self)
        db.session.commit()

    # checking if email exists
    @classmethod
    def  email_checker(cls,email):
        email_checker= cls.query.filter_by(email=email).first()
        if email_checker:
            return email_checker
            return True
        else:
            return False

    # checking password as per email entered
    @classmethod
    def password_checker(cls,email,password):
        password_check= cls.query.filter_by(email=email).first()
        if password_check and check_password_hash(password_check.password,password):
            return True
        else:
            return False

