from flask import current_app as app


class Purchase:
    def __init__(self, order_id, product_id, seller_ID_2, buyer_id, time_purchased, quantity, fulfilled_status):
        self.order_id = order_id
        self.product_id= product_id
        self.seller_ID_2 = seller_ID_2
        self.buyer_id = buyer_id
        self.time_purchased = time_purchased
        self.quantity = quantity
        self.fulfilled_status = fulfilled_status


    @staticmethod
    def get(buyer_id):
        rows = app.db.execute('''
SELECT order_id, product_id, seller_ID_2, buyer_id, time_purchased, quantity, fulfilled_status
FROM Purchases
WHERE buyer_id = :buyer_id
''',
                              buyer_id=buyer_id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(buyer_id, since):
        rows = app.db.execute('''
SELECT order_id, product_id, seller_ID_2, buyer_id, time_purchased, quantity, fulfilled_status
FROM Purchases
WHERE buyer_id = :buyer_id
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              buyer_id=buyer_id,
                              since=since)
        return [Purchase(*row) for row in rows]