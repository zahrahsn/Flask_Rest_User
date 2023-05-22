import os
import unittest
from pathlib import Path

os.environ['DB_URL'] = 'sqlite:///test.db'
from app import app
from models import User, db, PhoneNumber,Email


def create_test_phone(user_id=1):
    phone = PhoneNumber()
    phone.number = '1234567890'
    phone.user_id = user_id
    return phone

def create_test_email(user_id=1):
    email = Email()
    email.email = 'john@example.com'
    email.user_id = user_id
    return email


def create_test_user():
    user = User()
    user.firstName = 'John'
    user.lastName = 'Doe'
    return user


class TestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    @classmethod
    def tearDownClass(cls):
        test_db_path = os.path.join(Path(__file__).parent, 'instance', 'test.db')
        os.remove(test_db_path)

    def test_add_user(self):
        user_data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'emails': [{'email': 'john@example.com'}],
            'phoneNumbers': [{'number': '1234567890'}]
        }
        response = self.client.post('/users', json=user_data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['firstName'], user_data['firstName'])
        self.assertEqual(data['lastName'], user_data['lastName'])
        self.assertEqual(data['emails'][0]['email'], user_data['emails'][0]['email'])
        self.assertEqual(data['phoneNumbers'][0]['number'], user_data['phoneNumbers'][0]['number'])

    def test_get_user(self):
        user = create_test_user()
        with app.app_context():
            db.session.add(user)
            db.session.commit()
            response = self.client.get(f'/users/{user.id}')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['firstName'], user.firstName)
            self.assertEqual(data['lastName'], user.lastName)

    def test_get_users(self):
        user = create_test_user()
        with app.app_context():
            db.session.add(user)
            db.session.commit()
            response = self.client.get(f'/users/{user.id}')
            self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        user = create_test_user()
        with app.app_context():
            db.session.add(user)
            db.session.commit()
            response = self.client.delete(f'users/{user.id}')
            self.assertEqual(response.status_code, 200)
            self.assertTrue('User deleted successfully' in response.text)

    def test_add_phone(self):
        user = create_test_user()
        with app.app_context():
            db.session.add(user)
            db.session.commit()
            id = user.id
            phone_data = {
                'number': '12345678',

            }
            response = self.client.post(f'/user/{id}/phone/add', json=phone_data)
            data = response.get_json()
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['number'], phone_data['number'])

    def test_edit_phone(self):
        user = create_test_user()
        with app.app_context():
            db.session.add(user)
            db.session.commit()
            phone = create_test_phone(user_id=user.id)
            db.session.add(phone)
            db.session.commit()
            new_phone_number = '9876543210'
            phone_data = {'number': new_phone_number}
            response = self.client.put(f"/user/{phone.user_id}/phone/edit/{phone.id}", json=phone_data)
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['number'], new_phone_number)
            db.session.refresh(phone)
            self.assertEqual(phone.number, new_phone_number)

    def test_delete_phone(self):
        user = create_test_user()
        with app.app_context():
            db.session.add(user)
            db.session.commit()
            phone = create_test_phone(user_id=user.id)
            db.session.add(phone)
            db.session.commit()
            response = self.client.delete(f'/user/{user.id}/phone/delete/{phone.id}')
            self.assertEqual(response.status_code, 200)
            self.assertTrue("Phone Number deleted successfully" in response.text)


    def test_add_email(self):
        user = create_test_user()
        with app.app_context():
            db.session.add(user)
            db.session.commit()
            id = user.id
            email_data = {
                'email': '12@gmail.com',

            }
            response = self.client.post(f'/user/{id}/email/add', json=email_data)
            data = response.get_json()
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['email'], email_data['email'])

    def test_edit_emai(self):
        user = create_test_user()
        with app.app_context():
            db.session.add(user)
            db.session.commit()
            email = create_test_email(user_id=user.id)
            db.session.add(email)
            db.session.commit()
            new_email = 'jd@gmail.com'
            email_data = {'email': new_email}
            response = self.client.put(f"/user/{email.user_id}/email/edit/{email.id}", json=email_data)
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['email'], new_email)
            db.session.refresh(email)
            self.assertEqual(email.email, new_email)

    def test_delete_email(self):
        user = create_test_user()
        with app.app_context():
            db.session.add(user)
            db.session.commit()
            email = create_test_email(user_id=user.id)
            db.session.add(email)
            db.session.commit()
            response = self.client.delete(f'/user/{user.id}/email/delete/{email.id}')
            self.assertEqual(response.status_code, 200)
            self.assertTrue("Email Address deleted successfully" in response.text)