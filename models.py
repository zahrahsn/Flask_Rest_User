from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class PhoneNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"PhoneNumber(id = {self.id}, number = {self.number}, user_id = {self.user_id})"


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Email(id={self.id} ,email={self.email},user_id={self.user_id})"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastName = db.Column(db.String(100), nullable=False)
    firstName = db.Column(db.String(100), nullable=False)
    emails = db.relationship('Email', backref='user', cascade='all, delete-orphan')
    phoneNumbers = db.relationship('PhoneNumber', backref='user', cascade='all, delete-orphan')

    @staticmethod
    def factory(**kwargs):
        return User(
            firstName=kwargs.get('firstName'),
            lastName=kwargs.get('lastName'),
            emails=list(map(lambda x: Email(email=x['email']), kwargs.get('emails'))),
            phoneNumbers=list(map(lambda x: PhoneNumber(number=x['number']), kwargs.get('phoneNumbers')))
        )

    def __repr__(self):
        return f"User(id={self.id},lastName={self.lastName},firstName={self.firstName})"
