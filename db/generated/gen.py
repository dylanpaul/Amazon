from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 550
num_products = 2000
num_purchases = 2000
num_coupons = 2000
num_sellers = 500

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

#need id, email, pass, first, last
def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            writer.writerow([uid, email, password, firstname, lastname])
        print(f'{num_users} generated')
    return

#id
def gen_coupons(num_coupons):
    coupons = []
    with open('Coupons.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Coupons...', end=' ', flush=True)
        for id in range(num_products):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            coupon_code = fake.license_plate() #use license plate random generators as coupon code
            coupons.append(coupon_code)
            discount = f'{str(fake.random_int(max=0))}.{fake.random_int(min=1, max=20):02}'
            writer.writerow([coupon_code, discount])
        print(f'{num_coupons} generated')
    return coupons


#need id, name, seller_id, description, category, inventory,available(t or f), price, coupon_code
def gen_products(num_products, coupons):
    available_pids = []
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            temp = []
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            seller_id = fake.random_int(max=499) #for now just 500 sellers!
            description = fake.sentence(nb_words=4)[:-1] #random description
            category = fake.color_name() #using this as category generator for now
            inventory = f'{str(fake.random_int(max=100))}' #max amount of inventory 100 for now
            coupon_code = fake.random_element(elements=coupons) #use license plate random generators as coupon code
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                temp.append(pid)
                temp.append(seller_id)
                available_pids.append(temp)
            writer.writerow([pid, name, seller_id, description, category, inventory, available, price, coupon_code])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


#id
def gen_sellers(num_sellers):
    with open('Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        for id in range(num_sellers):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            seller_id = id #for now just 500 sellers!
            writer.writerow([seller_id])
        print(f'{num_sellers} generated')
    return


#need orderid, prodid, sellerid, buyerid, time_purchased, quantity, fulfilled status(t or f)
def gen_purchases(num_purchases, available_pids):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            hold = fake.random_element(elements=available_pids)
            bid = fake.random_int(min=0, max=num_users-1)
            pid = hold[0]
            seller_id = hold[1]
            quantity = f'{str(fake.random_int(min=1, max=4))}' #for now just 4 max quantity 
            time_purchased = fake.date_time()
            fulfilled = fake.random_element(elements=('true', 'false'))
            writer.writerow([id, pid, seller_id, bid, time_purchased, quantity, fulfilled])
        print(f'{num_purchases} generated')
    return


gen_users(num_users)
coupons = gen_coupons(num_coupons)
available_pids = gen_products(num_products, coupons)
gen_sellers(num_sellers)
gen_purchases(num_purchases, available_pids)