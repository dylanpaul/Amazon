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
SELECT p.id, p.name, p.seller_id, p.description, p.category, p.inventory, p.available, p.price, p.coupon_code, u.firstname, u.lastname
FROM Products as p, Users as u
WHERE p.id = :id
AND p.seller_id = u.id
''',
                              id=id)
        return [row for row in rows]
        #return [Product(*row) for row in rows]
        #return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, seller_id, description, category, inventory, available, price, coupon_code
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_seller_info(sid):
        rows = app.db.execute('''
SELECT p.id, p.name, p.seller_id, p.inventory, p.available, p.price, p.coupon_code, u.firstname, u.lastname
FROM Products as p, Users as u
WHERE p.seller_id = :sid
AND u.id = p.seller_id
''',
                              sid= sid)
        return [row for row in rows]
        #return [Product(*row) for row in rows] if rows is not None else None

    @staticmethod
    def add_product(name, sid, description, category, inventory, available, price, coupon_code):
        #try:
        print("here?")
        rows = app.db.execute("""
INSERT INTO Products(name, seller_id, description, category, inventory, available, price, coupon_code)
VALUES(:name, :seller_id, :description, :category, :inventory, :available, :price, :coupon_code)
RETURNING id
""",
                                name = name,
                                seller_id = sid,
                                description = description,
                                category = category,
                                inventory = inventory,
                                available = available,
                                price = price,
                                coupon_code = coupon_code)
                                    
            #except:
             #   print("error")
        #id = rows[0][0]
        #for row in rows:
           # print(row)
        return id
        #id = rows[0][0]

    @staticmethod
    def delete(sid, product_name):
        try:
            app.db.execute("""
delete from products where name = :pname and seller_id = :sid
""",
                                pname = product_name,
                                sid = sid)
        except:
            print("error")
        return

    @staticmethod
    def delete_pid(pid):
        try:
            app.db.execute("""
delete from products where id = :pid;
delete from cart_items where product_id = :pid
""",
                                pid = pid)
        except:
            print("error")
        return
    

    @staticmethod
    def update_inventory(sid, pid, inv):
        try:
            app.db.execute("""
UPDATE products
SET inventory = :inventory
WHERE id = :pid AND seller_id = :sid
""",
                             pid = pid,
                             sid = sid,
                             inventory = inv)
        except:
            print("error")
        return



    @staticmethod
    def update_price(pid, price):
        try:
            app.db.execute("""
UPDATE products
SET price = :price
WHERE id = :pid
""",
                             pid = pid,
                             price = price)
        except:
            print("error")
        return


    @staticmethod
    def update_available(pid, avail):
        try:
            app.db.execute("""
UPDATE products
SET available = :available
WHERE id = :pid
""",
                             pid = pid,
                             available = avail)
        except:
            print("error")
        return

    @staticmethod
    def get_categories(available=True):
        rows = app.db.execute("""
SELECT category 
FROM Products
GROUP BY category
""",
                                available = available)           
        return [row for row in rows]


    @staticmethod
    def get_cat(category):
        rows = app.db.execute('''
SELECT id, name, seller_id, description, category, inventory, available, price, coupon_code
FROM Products
WHERE category = :category
''',
                              category=category)
        return [Product(*row) for row in rows]


#   @staticmethod
#  def get_unique(available=True):
        #rows = app.db.execute('''
#SELECT DISTINCT id, name, category
#FROM Products
#WHERE available = :available
#''',
 #                             available=available)
  #      return [Product(*row) for row in rows]
    
   # @staticmethod
  #  def get_price_range(available=True):
   #     rows = app.db.execute('''
#SELECT DISTINCT id, MIN(price) as min, MAX(price) as max
#FROM Products
#WHERE available = :available
#GROUP BY id
#''',
 #                             available=available)
 #       return [Product(*row) for row in rows]
