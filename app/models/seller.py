from flask import current_app as app


class Seller:
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(seller_id):
        rows = app.db.execute('''
SELECT id
FROM Seller
WHERE seller_id = :seller_id
''',
                              seller_id=seller_id)
        return Seller(*(rows[0])) if rows else None