import pytest
from app import App
from models import User, db, PhoneNumber, Email


@pytest.fixture()
def app():
    app = App('sqlite:///:memory:').app
    app.config.update({"TESTING": True})
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def test_user():
    return User(firstName='John', lastName='Doe')


@pytest.fixture()
def test_phone(user_id=1):
    return PhoneNumber(number='1234567890', user_id=user_id)


@pytest.fixture()
def test_email(user_id=1):
    return Email(email='john@example.com', user_id=user_id)


def test_add_user(client):
    user_data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'emails': [{'email': 'john@example.com'}],
        'phoneNumbers': [{'number': '1234567890'}]
    }
    response = client.post('/users', json=user_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['firstName'] == user_data['firstName']
    assert data['lastName'] == user_data['lastName']
    assert data['emails'][0]['email'] == user_data['emails'][0]['email']
    assert data['phoneNumbers'][0]['number'] == user_data['phoneNumbers'][0]['number']


def test_get_user(app, test_user, client):
    with app.app_context():
        db.session.add(test_user)
        db.session.commit()
        response = client.get(f'/users/{test_user.id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['firstName'] == test_user.firstName
        assert data['lastName'] == test_user.lastName


def test_get_users(app, test_user, client):
    with app.app_context():
        db.session.add(test_user)
        db.session.commit()
        response = client.get(f'/users')
        assert response.status_code == 200
        assert len(response.json) == 1


def test_delete_user(app, test_user, client):
    with app.app_context():
        db.session.add(test_user)
        db.session.commit()
        response = client.delete(f'users/{test_user.id}')
        assert response.status_code == 200
        assert 'User deleted successfully' in response.text


def test_add_phone(app, test_user, client):
    with app.app_context():
        db.session.add(test_user)
        db.session.commit()
        user_id = test_user.id
        phone_data = {'number': '12345678'}
        response = client.post(f'/user/{user_id}/phone/add', json=phone_data)
        data = response.get_json()
        assert response.status_code == 201
        assert data['number'] == phone_data['number']


def test_edit_phone(app, test_user, test_phone, client):
    with app.app_context():
        db.session.add_all([test_user, test_phone])
        db.session.commit()
        new_phone_number = '9876543210'
        phone_data = {'number': new_phone_number}
        response = client.put(f"/user/{test_phone.user_id}/phone/edit/{test_phone.id}", json=phone_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data['number'] == new_phone_number
        db.session.refresh(test_phone)
        assert test_phone.number == new_phone_number


def test_delete_phone(app, test_user, test_phone, client):
    with app.app_context():
        db.session.add_all([test_user, test_phone])
        db.session.commit()
        response = client.delete(f'/user/{test_user.id}/phone/delete/{test_phone.id}')
        assert response.status_code == 200
        assert "Phone Number deleted successfully" in response.text


def test_add_email(app, test_user, test_email, client):
    with app.app_context():
        db.session.add_all([test_user, test_email])
        db.session.commit()
        user_id = test_user.id
        email_data = {'email': '12@gmail.com'}
        response = client.post(f'/user/{user_id}/email/add', json=email_data)
        data = response.get_json()
        assert response.status_code == 201
        assert data['email'] == email_data['email']


def test_edit_emai(app, test_user, test_email, client):
    with app.app_context():
        db.session.add_all([test_user, test_email])
        db.session.commit()
        new_email = 'jd@gmail.com'
        email_data = {'email': new_email}
        response = client.put(f"/user/{test_email.user_id}/email/edit/{test_email.id}", json=email_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data['email'] == new_email
        db.session.refresh(test_email)
        assert test_email.email == new_email


def test_delete_email(app, test_user, test_email, client):
    with app.app_context():
        db.session.add_all([test_user, test_email])
        db.session.commit()
        response = client.delete(f'/user/{test_user.id}/email/delete/{test_email.id}')
        assert response.status_code == 200
        assert "Email Address deleted successfully" in response.text


def test_edit_user(app, test_user, client, test_phone, test_email):
    with app.app_context():
        db.session.add_all([test_user, test_email, test_phone])
        db.session.commit()
        updated_user = {
            'firstName': 'Jon',
            'lastName': 'Doe',
            'phoneNumbers': [{'number': '00000000'}],
            'emails': [{'email': 'john@email.com'}]}

        response = client.put(f'/users/{test_user.id}/edit', json=updated_user)
        assert response.status_code == 200
        data = response.get_json()
        assert data['emails'][0]['email'] == updated_user['emails'][0]['email']
        assert data['phoneNumbers'][0]['number'] == updated_user['phoneNumbers'][0]['number']
        assert data['firstName'] == updated_user['firstName']
        assert data['lastName'] == updated_user['lastName']




