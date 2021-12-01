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
    def get_cart_uid(u_id):
        rows = app.db.execute('''
SELECT c.user_id, c.product_id, c.seller_id, c.quantity, c.coupon_code, p.name, u.firstname, u.lastname
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
    def add(pid, sid, cid, user_id):
        try:
            app.db.execute("""
INSERT INTO Cart_Items(user_id, product_id, seller_id, quantity, coupon_code)
VALUES(:user_id, :pid, :sid, 1, :cid)
""",
                                user_id = user_id,
                                pid = pid,
                                sid = sid,
                                cid= cid)
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
