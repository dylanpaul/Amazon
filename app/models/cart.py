from flask import current_app as app


class Cart:
    def __init__(self, user_id, product_id, seller_id, quantity):
        #self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.seller_id = seller_id
        self.quantity = quantity

    @staticmethod
    def get_cart_uid(u_id):
        rows = app.db.execute('''
SELECT c.user_id, c.product_id, c.seller_id, c.quantity, p.name, u.firstname, u.lastname, p.price, p.image, p.inventory
FROM Cart_Items as c, Products as p, Users as u
WHERE c.user_id = :user_id
AND c.seller_id = p.seller_id
AND p.id = c.product_id
AND p.seller_id = u.id
AND c.seller_id = u.id
''',
                              user_id=u_id)
        #for row in rows:
         #   print(row)
        return [row for row in rows]
        #return [Cart(*row) for row in rows]
        #return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def add(pid, sid, user_id, quant):
        try:
            app.db.execute("""
INSERT INTO Cart_Items(user_id, product_id, seller_id, quantity)
VALUES(:user_id, :pid, :sid, :quantity)
""",
                                user_id = user_id,
                                pid = pid,
                                sid = sid,
                                quantity = quant
                                )
        except:
            print("error")
        return 
    
    @staticmethod
    def clear(u_id):
        try:
            app.db.execute("""
delete from cart_items where user_id = :user_id
""",
                                user_id = u_id)
        except:
            print("error")
        return
    
    @staticmethod
    def remove(u_id, p_id, s_id):
        try:
            app.db.execute("""
delete from cart_items where user_id = :user_id and product_id = :pid and seller_id = :sid
""",
                                user_id = u_id,
                                pid = p_id,
                                sid = s_id)
        except:
            print("error")
        return

    @staticmethod
    def update_quantity(uid, pid, sid, quantity):
        try:
            app.db.execute("""
UPDATE Cart_Items
SET quantity = :quant
WHERE user_id = :user_id AND product_id = :prod_id AND seller_id = :sell_id
""",
                                quant = quantity,
                                prod_id = pid,
                                sell_id = sid,
                                user_id = uid)
        except:
            print("error")
        return

    @staticmethod
    def get_total_price(uid):
        try:
            row_prices = app.db.execute("""
SELECT (p.price * c.quantity) as row_price
FROM Products as p, Cart_Items as c
WHERE c.user_id = :user_id AND c.product_id = p.id AND c.seller_id = p.seller_id
""",
                                user_id = uid)
        except:
            print("error")
        
        total = 0
        for price in row_prices:
            total = total + price[0]

        return total

    @staticmethod
    def check_quantities(uid):
        status = True
        try:
            check = app.db.execute("""
SELECT *
FROM Products as p, Cart_Items as c
WHERE c.user_id = :user_id AND c.product_id = p.id AND c.seller_id = p.seller_id AND c.quantity > p.inventory
""",
                                user_id = uid)
        except:
            print("error")

        if(len(check) > 0):
            status = False

        return status

    @staticmethod
    def check_balance(balance, price):
        if(balance>=price):
            return True
        else:
            return False