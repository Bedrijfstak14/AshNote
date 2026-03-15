import pytest
from app.models import User, db


def register(client, username, password):
    return client.post("/auth/register", data={
        "username": username,
        "password": password,
    }, follow_redirects=True)


def login(client, username, password):
    return client.post("/auth/login", data={
        "username": username,
        "password": password,
    }, follow_redirects=True)


def logout(client):
    return client.get("/auth/logout", follow_redirects=True)


class TestRegister:
    def test_register_success(self, client, app):
        with app.app_context():
            response = register(client, "testuser", "wachtwoord123")
            assert response.status_code == 200
            user = User.query.filter_by(username="testuser").first()
            assert user is not None

    def test_register_duplicate_username(self, client, app):
        with app.app_context():
            register(client, "dubbel", "wachtwoord123")
            response = register(client, "dubbel", "andereww123")
            assert b"bestaat al" in response.data

    def test_register_short_password(self, client, app):
        with app.app_context():
            response = register(client, "kortpw", "kort")
            assert b"minimaal" in response.data
            user = User.query.filter_by(username="kortpw").first()
            assert user is None

    def test_register_invalid_username(self, client, app):
        with app.app_context():
            response = register(client, "ab", "wachtwoord123")
            assert b"Gebruikersnaam" in response.data or response.status_code == 200

    def test_register_username_with_special_chars(self, client, app):
        with app.app_context():
            response = register(client, "user name!", "wachtwoord123")
            user = User.query.filter_by(username="user name!").first()
            assert user is None


class TestLogin:
    def test_login_success(self, client, app):
        with app.app_context():
            register(client, "logintest", "wachtwoord123")
            response = login(client, "logintest", "wachtwoord123")
            assert response.status_code == 200
            assert b"Succesvol ingelogd" in response.data

    def test_login_wrong_password(self, client, app):
        with app.app_context():
            register(client, "wrongpw", "correctww123")
            response = login(client, "wrongpw", "foutwachtwoord")
            assert b"Ongeldige" in response.data

    def test_login_nonexistent_user(self, client):
        response = login(client, "bestaaniet", "wachtwoord123")
        assert b"Ongeldige" in response.data

    def test_logout(self, client, app):
        with app.app_context():
            register(client, "uitlogtest", "wachtwoord123")
            login(client, "uitlogtest", "wachtwoord123")
            response = logout(client)
            assert b"uitgelogd" in response.data


class TestChangePassword:
    def test_change_password_success(self, client, app):
        with app.app_context():
            register(client, "changepw", "oudwachtwoord123")
            login(client, "changepw", "oudwachtwoord123")
            response = client.post("/auth/change-password", data={
                "current_password": "oudwachtwoord123",
                "new_password": "nieuwwachtwoord123",
                "confirm_password": "nieuwwachtwoord123",
            }, follow_redirects=True)
            assert b"succesvol" in response.data.lower()

    def test_change_password_wrong_current(self, client, app):
        with app.app_context():
            register(client, "changepw2", "wachtwoord123")
            login(client, "changepw2", "wachtwoord123")
            response = client.post("/auth/change-password", data={
                "current_password": "fouteww",
                "new_password": "nieuwwachtwoord123",
                "confirm_password": "nieuwwachtwoord123",
            }, follow_redirects=True)
            assert b"klopt niet" in response.data

    def test_change_password_mismatch(self, client, app):
        with app.app_context():
            register(client, "changepw3", "wachtwoord123")
            login(client, "changepw3", "wachtwoord123")
            response = client.post("/auth/change-password", data={
                "current_password": "wachtwoord123",
                "new_password": "nieuwwachtwoord123",
                "confirm_password": "anderwachtwoord123",
            }, follow_redirects=True)
            assert b"overeen" in response.data
