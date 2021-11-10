from flask import current_app as app


class Cart:
    def __init__(self, user_id, product_id, seller_id, quantity, coupon_code):
        #self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.seller_id = seller_id
        self.quantity = quantity
        self.coupon_code = coupon_code

    @staticmethod
    def get_cart_uid(user_id):
        rows = app.db.execute('''
SELECT user_id, product_id, seller_id, quantity, coupon_code
FROM Cart_Items
WHERE user_id = :user_id
''',
                              user_id=user_id)
        return [Cart(*row) for row in rows]
        #return Product(*(rows[0])) if rows is not None else None