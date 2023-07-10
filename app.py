import os

from flask import Flask, request
from flask_restful import Resource, Api

from models import db, User, PhoneNumber, Email
from schemas import UserSchema, PhoneSchema, EmailSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class App:

    def __init__(self, db_url):
        self.app, self.api = self.create_app(db_url)
        self.create_routes()

    def create_app(self, db_url):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        with app.app_context():
            db.create_all()
        api = Api(app)
        return app, api

    def create_routes(self):
        self.api.add_resource(UsersApi, "/users", endpoint='add_user', methods=['POST'])
        self.api.add_resource(UsersApi, '/users/<int:id>', endpoint='get_user', methods=['GET'])
        self.api.add_resource(UsersApi, '/users', endpoint='get_users', methods=['GET'])
        self.api.add_resource(UsersApi, "/users/<int:user_id>", endpoint='delete_user', methods=['DELETE'])
        self.api.add_resource(UserPhone, "/user/<int:user_id>/phone/add", endpoint='add', methods=['POST'])
        self.api.add_resource(
            UserPhone,
            "/user/<int:user_id>/phone/edit/<int:phone_id>",
            endpoint='edit',
            methods=['PUT']
        )
        self.api.add_resource(
            UserPhone,
            "/user/<int:user_id>/phone/delete/<int:phone_id>",
            endpoint='delete',
            methods=['DELETE']
        )
        self.api.add_resource(UserEmail, "/user/<int:user_id>/email/add", endpoint='add_email', methods=['POST'])
        self.api.add_resource(
            UserEmail,
            "/user/<int:user_id>/email/edit/<int:email_id>",
            endpoint='edit_email',
            methods=['PUT']
        )
        self.api.add_resource(
            UserEmail,
            "/user/<int:user_id>/email/delete/<int:email_id>",
            endpoint='delete_email',
            methods=['DELETE']
        )
        # I add it now
        self.api.add_resource(UserPhone, "/user/<int:user_id>/phone", endpoint='get_phone', methods=['GET'])
        self.api.add_resource(UsersApi, "/users/<int:user_id>/edit", endpoint='update_user', methods=['PUT'])


class UsersApi(Resource):
    def get(self, id=None):
        if id:
            user = User.query.get_or_404(id)
            return user_schema.dump(user)
        else:
            args = request.args.to_dict()
            users = User.query.filter_by(**args)
            return users_schema.dump(users)

    def post(self):
        data = request.get_json()
        user_dict = user_schema.load(data)
        user_obj = User.factory(**user_dict)
        db.session.add(user_obj)
        db.session.commit()

        # Return response
        return user_schema.dump(user_dict), 201

    def delete(self, user_id):
        user_obj = User.query.get_or_404(user_id)
        db.session.delete(user_obj)
        db.session.commit()
        return "User deleted successfully", 200

    # I add it now
    def put(self, user_id):
        data = request.get_json()
        user_dict = user_schema.load(data)
        user_obj = User.query.get_or_404(user_id)
        for ph in user_obj.phoneNumbers:
            db.session.delete(ph)
        for em in user_obj.emails:
            db.session.delete(em)
        user_obj.firstName = user_dict['firstName']
        user_obj.lastName = user_dict['lastName']
        phone_obj = []
        for v in user_dict['phoneNumbers']:
            phone = PhoneNumber()
            phone.number = v['number']
            phone.user_id = user_id
            phone_obj.append(phone)

        email_obj = []
        for v in user_dict['emails']:
            email = Email()
            email.email = v['email']
            email.user_id = user_id
            email_obj.append(email)
        # db.session.add(user_obj)
        db.session.add_all(phone_obj)
        db.session.add_all(email_obj)
        db.session.commit()
        return user_schema.dump(user_obj), 200


class UserPhone(Resource):
    def post(self, user_id):
        data = request.get_json()

        phone_schema = PhoneSchema()
        phone_dict = phone_schema.load(data)
        phone_obj = PhoneNumber()
        phone_obj.number = phone_dict['number']
        phone_obj.user_id = user_id

        db.session.add(phone_obj)
        db.session.commit()
        return phone_schema.dump(phone_obj), 201

    def put(self, user_id, phone_id):
        data = request.get_json()
        phone_schema = PhoneSchema()
        phone_dict = phone_schema.load(data)
        phone_obj = PhoneNumber.query.get_or_404(phone_id)
        phone_obj.number = phone_dict['number']
        db.session.add(phone_obj)
        db.session.commit()
        return phone_schema.dump(phone_obj), 200

    def delete(self, user_id, phone_id):
        phone_obj = PhoneNumber.query.get_or_404(phone_id)
        db.session.delete(phone_obj)
        db.session.commit()
        return "Phone Number deleted successfully", 200

    # I add it now
    def get(self, user_id):
        phone_obj = PhoneNumber.query.filter_by(user_id=user_id)
        phone_schema = PhoneSchema(many=True)
        return phone_schema.dump(phone_obj)


class UserEmail(Resource):
    def post(self, user_id):
        data = request.get_json()
        email_schema = EmailSchema()
        email_dict = email_schema.load(data)
        email_obj = Email()
        email_obj.email = email_dict['email']
        email_obj.user_id = user_id

        db.session.add(email_obj)
        db.session.commit()
        return email_schema.dump(email_obj), 201

    def put(self, user_id, email_id):
        data = request.get_json()
        email_schema = EmailSchema()
        email_dict = email_schema.load(data)
        email_obj = Email.query.get_or_404(email_id)
        email_obj.email = email_dict['email']
        db.session.add(email_obj)
        db.session.commit()
        return email_schema.dump(email_obj), 200

    def delete(self, user_id, email_id):
        email_obj = Email.query.get_or_404(email_id)
        db.session.delete(email_obj)
        db.session.commit()
        return "Email Address deleted successfully", 200


if __name__ == '__main__':
    perseus = App('sqlite:///perdb.db')
    perseus.app.run(
        debug=os.getenv('DEBUG', False),
        host=os.getenv('HOST', '0.0.0.0'),
        port=os.getenv('PORT', 8000)
    )
