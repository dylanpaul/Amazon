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
SELECT user_id, product_id, seller_id, quantity, coupon_code
FROM Cart_Items
WHERE user_id = :user_id
''',
                              user_id=u_id)
        return [Cart(*row) for row in rows]
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