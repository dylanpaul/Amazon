from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, addy, firstname, lastname, balance):
        self.id = id
        self.email = email
        self.addy = addy
        self.firstname = firstname
        self.lastname = lastname
        self.balance = balance

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, addy, firstname, lastname, balance
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(id1, email, addy, password, firstname, lastname):
        try:
            #print(email)
            rows = app.db.execute("""
INSERT INTO Users(id, email, addy, password, firstname, lastname, balance)
VALUES(:id, :email, :addy, :password, :firstname, :lastname, 0)
RETURNING id
""",
                                  email=email,
                                  addy = addy,
                                  password=generate_password_hash(password),
                                  firstname=firstname,
                                  lastname=lastname,
                                  id = id1)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and
            # reporting needed
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, addy, firstname, lastname, balance
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None

    @staticmethod
    def update_firstname(uid, firstname):
        try:
            app.db.execute("""
UPDATE Users
SET firstname = :firstname 
WHERE id = :uid
""",
                             uid = uid,
                             firstname = firstname)
        except:
            print("error")
        return

    @staticmethod
    def update_lastname(uid, lastname):
        try:
            app.db.execute("""
UPDATE Users
SET lastname = :lastname 
WHERE id = :uid
""",
                             uid = uid,
                             lastname = lastname)
        except:
            print("error")
        return

    @staticmethod
    def update_email(uid, email):
        try:
            app.db.execute("""
UPDATE Users
SET email = :email 
WHERE id = :uid
""",
                             uid = uid,
                             email = email)
        except:
            print("error")
        return

    @staticmethod
    def update_address(uid, address):
        try:
            app.db.execute("""
UPDATE Users
SET addy = :address 
WHERE id = :uid
""",
                             uid = uid,
                             address = address)
        except:
            print("error")
        return

    @staticmethod
    def update_balance(uid, balance1):
        try:
            app.db.execute("""
UPDATE Users
SET balance = :balance1 
WHERE id = :uid
""",
                             uid = uid,
                             balance1 = balance1)
        except:
            print("error")
        return

    @staticmethod
    def add_balance(uid, balance1):
        try:
            app.db.execute("""
UPDATE Users
SET balance = :balance1 
WHERE id = :uid
""",
                             uid = uid,
                             balance1 = balance1)
        except:
            print("error")
        return


    @staticmethod
    def get_balance(id):
        rows = app.db.execute("""
SELECT balance
FROM Users
WHERE id = :id
""",
                              id=id)
        return rows

    @staticmethod
    def get_all():
        rows = app.db.execute("""
SELECT COUNT(*)
FROM Users
""",
                              )
        return rows[0][0]

    @staticmethod
    def get_users(id2):
        rows = app.db.execute("""
SELECT id, email, addy, firstname, lastname, balance
FROM Users
WHERE id = :id
""",
                                id=id2)
        return rows