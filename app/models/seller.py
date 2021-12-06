from flask import current_app as app


class Seller:
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(seller_id):
        rows = app.db.execute('''
SELECT id
FROM Seller
WHERE id = :seller_id
''',
                              seller_id=seller_id)
        return Seller(*(rows[0])) if rows else None

    @staticmethod
    def register(id1):
        print("urg")
        try:
            #print(email)
            rows = app.db.execute("""
INSERT INTO Seller(id)
VALUES(:id)
RETURNING id
""",
                                  id = id1)
            id = rows[0][0]
            return Seller.get(id)
        except Exception as e:
            # likely email already in use; better error checking and
            # reporting needed
            return None