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
    
    @staticmethod
    def add_purchases(u_id, their_purchases):
        for prod in their_purchases:
            try:
                app.db.execute("""
INSERT INTO Purchases(order_id, product_id, seller_ID_2, buyer_id, time_purchased, quantity, fulfilled_status)
VALUES(:oid, :pid, :sid, :user_id, :date, :quantity, 'TRUE')
""",
                                oid = 7, #what to do about order id?
                                user_id = u_id,
                                date = '9/10/21 13:12', #how to make a current time stamp?
                                pid = prod.product_id, 
                                sid = prod.seller_id,
                                quantity = prod.quantity)
            except:
                print("error")
        return