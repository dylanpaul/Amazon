from flask import current_app as app
from .user import User

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
    def get_order_by_uid_since(ids, buyer_id):
        rows = []
        for id1 in ids:
            print(id1)
            try:
                row = app.db.execute("""
SELECT pu.id, COUNT(pu.quantity) as c, SUM(pr.price) as total
FROM Purchases as pu, Products as pr
WHERE buyer_id = :buyer_id
AND pu.id = :id
AND pr.id = pu.product_id
GROUP BY pu.id
""",
                              buyer_id = buyer_id,
                              id = id1)
            except:
                print("error")
            rows.append(row[0])
        return rows

    @staticmethod
    def get_time(buyer_id, since):
        rows = app.db.execute('''
SELECT pu.id, pu.time_purchased
FROM Purchases as pu
WHERE buyer_id = :buyer_id
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              buyer_id=buyer_id,
                              since=since)
        return [row for row in rows]

# pu.time_purchased, pu.fulfilled_status,
        #return [Purchase(*row) for row in rows]




#     @staticmethod
#     def ids_ordered_time(buyer_id, since):
#         rows = app.db.execute('''
# SELECT pu.buyer_id, pu.time_purchased
# FROM Purchases as pu, Products as pr
# WHERE buyer_id = :buyer_id
# AND pr.id = pu.product_id
# AND time_purchased >= :since
# ORDER BY time_purchased DESC
# ''',
#                               buyer_id=buyer_id,
#                               since=since)
#         return [row for row in rows]
#         #return [Purchase(*row) for row in rows]


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
    def add_purchases(id, u_id, their_purchases):
        for prod in their_purchases:
            try:
                rows = app.db.execute("""
INSERT INTO Purchases(id, product_id, seller_ID_2, buyer_id, time_purchased, quantity, fulfilled_status)
VALUES(:id, :pid, :sid, :user_id, current_timestamp, :quantity, 'FALSE')
RETURNING id
""",
                                #oid = id, #what to do about order id?
                                id = id,
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

    @staticmethod
    def get_seller(seller_id):
        rows = app.db.execute('''
SELECT id, product_id, seller_ID_2, buyer_id, time_purchased, quantity, fulfilled_status
FROM Purchases
WHERE seller_ID_2 = :seller_id
ORDER BY time_purchased DESC
''',
                              seller_id=seller_id)
        return [row for row in rows]

    @staticmethod
    def get_seller_products(seller_id):
        rows = app.db.execute('''
SELECT p.id, p.product_id, p.seller_ID_2, p.buyer_id, p.time_purchased, p.quantity, p.fulfilled_status, pr.name
FROM Purchases as p, Products as pr
WHERE seller_ID_2 = :seller_id
AND p.product_id = pr.id
ORDER BY time_purchased DESC
''',
                              seller_id=seller_id)
        return [row for row in rows]
        #return Purchase(*(rows[0])) if rows else None


    @staticmethod
    def get_users(seller_id):
        rows = app.db.execute('''
SELECT buyer_id
FROM Purchases
WHERE seller_ID_2 = :seller_id
ORDER BY time_purchased DESC
''',
                                seller_id=seller_id)
        return [row[0] for row in rows]


    @staticmethod
    def make_unavailable():
        try:
            app.db.execute("""
UPDATE Products
SET available = :f
WHERE inventory = :zero
""",            
                                f = False,
                                zero = 0)
        except:
            print("error")
        print("end of try")
        return


    @staticmethod
    def update_user_balance(uid, balance, cost):
        try:
                app.db.execute("""
UPDATE Users
SET balance = :new_val
WHERE id = :user_id
""",            
                                new_val = (balance - cost),
                                user_id = uid)
        except:
                print("error")
        return


    @staticmethod
    def update_seller_balances(their_purchase):
        print(their_purchase)
        for prod in their_purchase:
            print(prod)
            old_bal = User.get_balance(prod.seller_id)[0][0]
            try:
                app.db.execute("""
UPDATE Users
SET balance = :new_bal
WHERE id = :seller_id
""",
                               new_bal = old_bal + (prod.quantity * prod.price),
                               seller_id = prod.seller_id)  
            except:
                   print("error")
        return

    @staticmethod
    def edit_fufil(pid):
        print(pid)
        try:
            rows = app.db.execute('''
UPDATE Purchases
SET fulfilled_status = :val
WHERE id = :pid
''',
                               val = 'TRUE',
                               pid=pid)
        except:
                print("error")
        return

    @staticmethod
    def get_size():
        rows = app.db.execute("""
SELECT COUNT(*)
FROM Purchases
""",
                              )
        return rows[0][0]
    
    @staticmethod
    def get_order(oid):
        rows = app.db.execute('''
SELECT prod.name, pur.product_id, u.id, u.firstname, u.lastname, pur.time_purchased, prod.price, pur.quantity, pur.fulfilled_status
FROM Purchases as pur, Users as u, Products as prod
WHERE pur.id = :purid
AND pur.product_id = prod.id
AND u.id = pur.seller_ID_2
''',
                            purid = oid)
        return rows