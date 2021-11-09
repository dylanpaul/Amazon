from flask import current_app as app


class Product:
    def __init__(self, id, name, seller_id, description, category, inventory, available, price, coupon_code):
        #self.id = id
        self.id = id
        self.name = name
        self.seller_id = seller_id
        self.description = description
        self.category = category
        self.inventory = inventory
        self.available = available
        self.price = price
        self.coupon_code = coupon_code

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, seller_id, description, category, inventory, available, price, coupon_code
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, seller_id, description, category, inventory, available, price, coupon_code
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]
