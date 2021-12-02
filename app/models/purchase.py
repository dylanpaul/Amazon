from flask import current_app as app


class Purchase:
    def __init__(self, id, product_id, seller_ID_2, buyer_id, time_purchased, quantity, fulfilled_status):
        self.id = id
        self.product_id= product_id
        self.seller_ID_2 = seller_ID_2
        self.buyer_id = buyer_id
        self.time_purchased = time_purchased
        self.quantity = quantity
        self.fulfilled_status = fulfilled_status

    @staticmethod
    def get(buyer_id):
        rows = app.db.execute('''
SELECT id, product_id, seller_ID_2, buyer_id, time_purchased, quantity, fulfilled_status
FROM Purchases
WHERE buyer_id = :buyer_id
''',
                              buyer_id=buyer_id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(buyer_id, since):
        rows = app.db.execute('''
SELECT pu.id, pu.product_id, pu.seller_ID_2, pu.buyer_id, pu.time_purchased, pu.quantity, pu.fulfilled_status, pr.name
FROM Purchases as pu, Products as pr
WHERE buyer_id = :buyer_id
AND pr.id = pu.product_id
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              buyer_id=buyer_id,
                              since=since)
        return [row for row in rows]
        #return [Purchase(*row) for row in rows]
    
    @staticmethod
    def add_purchases(u_id, their_purchases):
        for prod in their_purchases:
            try:
                rows = app.db.execute("""
INSERT INTO Purchases(product_id, seller_ID_2, buyer_id, time_purchased, quantity, fulfilled_status)
VALUES(:pid, :sid, :user_id, current_timestamp, :quantity, 'TRUE')
RETURNING id
""",
                                #oid = id, #what to do about order id?
                                user_id = u_id,
                                #date = datetime.now(), #current_timestamp, #'9/10/21 13:12', #how to make a current time stamp?
                                pid = prod.product_id, 
                                sid = prod.seller_id,
                                quantity = prod.quantity)
            
            except:
                print("error")
        #id = rows[0][0]
        return
        #id = rows[0][0]
    
    @staticmethod
    def decrement_stock(their_purchase):
        for prod in their_purchase:
            print((prod.inventory - prod.quantity))
            try:
                app.db.execute("""
UPDATE Products
SET inventory = :new_val
WHERE seller_id = :sell_id AND id = :prod_id
""",            
                                new_val = (prod.inventory - prod.quantity),
                                sell_id = prod.seller_id,
                                prod_id = prod.product_id)
            except:
                print("error")
        return
