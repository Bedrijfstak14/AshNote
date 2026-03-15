import pytest
from app.models import User, Cigar, db


def register_and_login(client, app, username="cigaruser", password="wachtwoord123"):
    with app.app_context():
        client.post("/auth/register", data={"username": username, "password": password})
    client.post("/auth/login", data={"username": username, "password": password})


def add_cigar(client, name="Cohiba Siglo", rating=8, price=15.0):
    return client.post("/add", data={
        "name": name,
        "rating": str(rating),
        "origin_country": "Cuba",
        "purchase_location": "La Casa del Habano",
        "price": str(price),
        "remarks": "Uitstekend",
    }, follow_redirects=True)


class TestCigarValidation:
    def test_add_cigar_success(self, client, app):
        register_and_login(client, app, "addtest")
        with app.app_context():
            response = add_cigar(client)
            assert response.status_code == 200
            cigar = Cigar.query.filter_by(name="Cohiba Siglo").first()
            assert cigar is not None

    def test_add_cigar_missing_name(self, client, app):
        register_and_login(client, app, "noname")
        response = client.post("/add", data={
            "name": "",
            "rating": "7",
            "price": "10.0",
        }, follow_redirects=True)
        assert b"verplicht" in response.data

    def test_add_cigar_invalid_rating_too_high(self, client, app):
        register_and_login(client, app, "highrating")
        response = client.post("/add", data={
            "name": "Testcigaar",
            "rating": "11",
            "price": "10.0",
        }, follow_redirects=True)
        assert b"1 en 10" in response.data

    def test_add_cigar_invalid_rating_zero(self, client, app):
        register_and_login(client, app, "zerorating")
        response = client.post("/add", data={
            "name": "Testcigaar",
            "rating": "0",
            "price": "10.0",
        }, follow_redirects=True)
        assert b"1 en 10" in response.data

    def test_add_cigar_negative_price(self, client, app):
        register_and_login(client, app, "negprice")
        response = client.post("/add", data={
            "name": "Testcigaar",
            "rating": "5",
            "price": "-10",
        }, follow_redirects=True)
        assert b"Prijs" in response.data

    def test_add_cigar_price_too_high(self, client, app):
        register_and_login(client, app, "highprice")
        response = client.post("/add", data={
            "name": "Testcigaar",
            "rating": "5",
            "price": "200000",
        }, follow_redirects=True)
        assert b"Prijs" in response.data


class TestCigarOwnership:
    def test_user_cannot_edit_other_user_cigar(self, client, app):
        """Gebruiker mag geen sigaar van een andere gebruiker bewerken."""
        # Gebruiker 1 voegt sigaar toe
        register_and_login(client, app, "owner1")
        with app.app_context():
            add_cigar(client, name="Owners Cigar")
            cigar = Cigar.query.filter_by(name="Owners Cigar").first()
            cigar_id = cigar.id

        # Gebruiker 2 probeert de sigaar te bewerken
        client.get("/auth/logout")
        register_and_login(client, app, "attacker1")
        response = client.post(f"/edit/{cigar_id}", data={
            "name": "Gestolen sigaar",
            "rating": "1",
            "price": "0",
        }, follow_redirects=True)
        assert response.status_code == 404

    def test_user_cannot_delete_other_user_cigar(self, client, app):
        """Gebruiker mag geen sigaar van een andere gebruiker verwijderen."""
        register_and_login(client, app, "owner2")
        with app.app_context():
            add_cigar(client, name="Owners Cigar 2")
            cigar = Cigar.query.filter_by(name="Owners Cigar 2").first()
            cigar_id = cigar.id

        client.get("/auth/logout")
        register_and_login(client, app, "attacker2")
        response = client.post(f"/delete/{cigar_id}", follow_redirects=True)
        assert response.status_code == 404


class TestAuthRequired:
    def test_index_requires_login(self, client):
        client.get("/auth/logout")
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 302
        assert "/auth/login" in response.headers["Location"]

    def test_add_requires_login(self, client):
        client.get("/auth/logout")
        response = client.get("/add", follow_redirects=False)
        assert response.status_code == 302

    def test_account_requires_login(self, client):
        client.get("/auth/logout")
        response = client.get("/account", follow_redirects=False)
        assert response.status_code == 302
