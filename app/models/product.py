from flask import current_app as app


class Product:
    def __init__(self, id, name, seller_id, description, category, inventory, available, price, image):
        #self.id = id
        self.id = id
        self.name = name
        self.seller_id = seller_id
        self.description = description
        self.category = category
        self.inventory = inventory
        self.available = available
        self.price = price
        self.image = image

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT p.id, p.name, p.seller_id, p.description, p.category, p.inventory, p.available, p.price, p.image, u.firstname, u.lastname
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
SELECT id, name, seller_id, description, category, inventory, available, price, image
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_seller_info(sid):
        rows = app.db.execute('''
SELECT p.id, p.name, p.seller_id, p.inventory, p.available, p.price, p.image, u.firstname, u.lastname
FROM Products as p, Users as u
WHERE p.seller_id = :sid
AND u.id = p.seller_id
''',
                              sid= sid)
        return [row for row in rows]
        #return [Product(*row) for row in rows] if rows is not None else None

    @staticmethod
    def add_product(id, name, sid, description, category, inventory, available, price, image):
        #try:
        
        rows = app.db.execute("""
INSERT INTO Products(id, name, seller_id, description, category, inventory, available, price, image)
VALUES(:id1, :name, :seller_id, :description, :category, :inventory, :available, :price, :image)
RETURNING id
""",
                                
                                id1 = id,
                                name = name,
                                seller_id = sid,
                                description = description,
                                category = category,
                                inventory = inventory,
                                available = available,
                                price = price,
                                image = image
                                )
                                    
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
SELECT id, name, seller_id, description, category, inventory, available, price, image
FROM Products
WHERE category = :category
AND available = :av
''',
                              category=category,
                              av = True)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_price_low():
        rows = app.db.execute('''
SELECT id, name, seller_id, description, category, inventory, available, price, image
FROM Products
WHERE available = :av
ORDER BY price
''',
                              av = True)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_price_high():
        rows = app.db.execute('''
SELECT id, name, seller_id, description, category, inventory, available, price, image
FROM Products
WHERE available = :av
ORDER BY price DESC
''',
                              av = True)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_inv(pid, sid):
        inventory = app.db.execute("""
SELECT inventory 
FROM Products
WHERE id = :prod_id AND seller_id = :sell_id
""",
                                prod_id = pid,
                                sell_id = sid)
        return inventory

    @staticmethod
    def get_count():
        rows = app.db.execute("""
SELECT COUNT(*)
FROM Products
""",
                              )
        return rows[0][0]



    @staticmethod
    def get_name(id):
       name = app.db.execute('''
SELECT name  
FROM Products
WHERE id = :pid
''',
                            pid = id)
       return name[0][0]

    @staticmethod
    def get_shared(name):
       rows = app.db.execute('''
SELECT p.id, p.name, p.seller_id, p.description, p.category, p.inventory, p.available, p.price, p.image, u.firstname, u.lastname
FROM Products as p, Users as u
WHERE p.name = :n
AND p.seller_id = u.id
''',                          
                           n = name)
       return rows


    @staticmethod
    def search(search):
        search1 = search + "%"
        search2 = "%" + search + "%"
        rows = app.db.execute('''
SELECT id, name, seller_id, description, category, inventory, available, price, image
FROM Products
WHERE name LIKE :search1
OR name LIKE :search2
''',
                                search1 = search1,
                                search2 = search2)
        return [Product(*row) for row in rows]


#   @staticmethod
#WHERE category = :category
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
