from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases)

@bp.route('/product/<pid>')
def product(pid):
    # get the product info for one product
    product1 = Product.get(pid)
    # render the page by adding information to the index.html file
    return render_template('product.html',
                           prod = product1)

@bp.route('/cart/<pid>/<sid>/<cid>')
def cart(pid,sid,cid):
    #get cart for one user
    print(pid,sid,cid)
    if current_user.is_authenticated:
        print("here?3")
        Cart.add(int(pid),int(sid),cid,current_user.id)
        cart1 = Cart.get_cart_uid(current_user.id)
    return render_template('cart.html',
                           cart_things = cart1)


