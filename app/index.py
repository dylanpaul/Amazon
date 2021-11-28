from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask import request
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FloatField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, InputRequired
from flask_babel import _, lazy_gettext as _l

from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart
from .models.user import User
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('index', __name__)

categs = ""

@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    # find the products current user has bought:
    #if current_user.is_authenticated:
     #   purchases = Purchase.get_all_by_uid_since(
      #      current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    #else:
     #   purchases = None
    # render the page by adding information to the index.html file
    cats = Product.get_categories(True)
    p = ['Low to High', 'High to Low']
    return render_template('index.html',
                           avail_products=products,
                           categories = cats,
                           prices = p)
                           #purchase_history=purchases)

@bp.route('/category', methods=['GET', 'POST'])
def category():
    select = request.form.get('cat')
    #print(select)
    products = Product.get_cat(select)
    categs = select
    #print(categs)
    cats = Product.get_categories()
    p = ['Low to High', 'High to Low']
    #products = Product.get_all(True)
    return render_template('index.html',
                           avail_products=products,
                           categories = cats,
                           prices = p)
    return(str(select))


@bp.route('/price', methods=['GET', 'POST'])
def price():
    select = request.form.get('price')
    #print(categs)
    products = Product.get_cat_price()
    cats = Product.get_categories()
    p = ["Low to High", "High to Low"]
    #products = Product.get_all(True)
    return render_template('index.html',
                           avail_products=products,
                           categories = cats,
                           prices = p)
    return(str(select))


# @bp.route('/delete_product/<sid>')
# def delete_product(sid):
#     products = Product.get_seller_info(sid)
#     return render_template('delete_product.html', products = products)

# @bp.route('/test/<sid>', methods=['GET', 'POST'])
# def test(sid):
#     select = request.form.get('product')
#     #print(select)
#     Product.delete(sid, select)
#     return redirect(url_for('index.customer'))
#     return(str(select))



@bp.route('/customer')
def customer():
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        user_info = User.get(current_user.id)
    #seller1 = 0
    #if Seller.get(current_user.id) != None:
        #seller1 = 1
    seller1 = Product.get_seller_info(current_user.id)
    return render_template('customer.html',
                           purchase_history=purchases,
                           user1 = user_info,
                           seller = seller1)

@bp.route('/product/<pid>')
def product(pid):
    # get the product info for one product
    product1 = Product.get(pid)
    #seller_name = User.get(product1.seller_id)
    # render the page by adding information to the index.html file
    return render_template('product.html',
                           prod = product1)
                           #name = seller_name)

@bp.route('/cart/<pid>/<sid>/<cid>')
def cart(pid,sid,cid):
    #get cart for one user
    if current_user.is_authenticated:
        Cart.add(int(pid),int(sid),cid,current_user.id)
        cart1 = Cart.get_cart_uid(current_user.id)
    return render_template('cart.html',
                           cart_things = cart1)

@bp.route('/checkout')
def checkout():
    if current_user.is_authenticated:
        their_purchase = Cart.get_cart_uid(current_user.id)
        Purchase.add_purchases(current_user.id, their_purchase)
        Cart.clear(current_user.id)
    return render_template('checkout.html')

@bp.route('/remove/<pid>/<sid>')
def remove(pid,sid):
    if current_user.is_authenticated:
        Cart.remove(current_user.id, pid, sid)
        new_cart = Cart.get_cart_uid(current_user.id)
    return render_template('cart.html',
                           cart_things = new_cart)


@bp.route('/seller/<sid>')
def seller_info(sid):
    seller1 = Product.get_seller_info(sid)
    return render_template('seller.html',
                           seller = seller1)


class AddForm(FlaskForm):
    name = StringField(_l('Name'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    category = StringField(_l('Category'), validators=[DataRequired()])
    inventory = IntegerField(_l('Inventory'), validators=[DataRequired()])
    price = FloatField(_l('price'), validators=[DataRequired()])
    #coupon_code = StringField(_l('Coupon Code'), validators=[DataRequired()])
    submit = SubmitField(_l('Add'))


@bp.route('/add_product/<sid>', methods=['GET', 'POST'])
def add_product(sid):
    #name = request.args.get("name")
    #description = request.args.get("description")
    #category = request.args.get("category")
    #inventory = request.args.get("inventory")
    #price = request.args.get("price")
    #coupon_code = request.args.get("coupon_code")
    #sell = Product.get_seller_info(sid)
    form = AddForm()
    if form.validate_on_submit():
        Product.add_product(form.name.data, sid, form.description.data, form.category.data, 
        form.inventory.data, True, form.price.data, None)
        print(Product)
        return redirect(url_for('index.customer'))
    return render_template('add_product.html', title = 'Add Product', form = form)
                           #eller = sell)


@bp.route('/delete_product/<sid>')
def delete_product(sid):
    products = Product.get_seller_info(sid)
    return render_template('delete_product.html', products = products)

@bp.route('/test/<sid>', methods=['GET', 'POST'])
def test(sid):
    select = request.form.get('product')
    #print(select)
    Product.delete(sid, select)
    return redirect(url_for('index.customer'))
    return(str(select))



class InvForm(FlaskForm):
    inventory = IntegerField(_l('Inventory'), validators=[InputRequired()])
    submit = SubmitField(_l('Add'))

@bp.route('/update_inventory/<sid>/<pid>', methods=['GET', 'POST'])
def update_inventory(sid, pid):
    form = InvForm()
    if form.validate_on_submit():
        inv = form.inventory.data
        if(inv != 0):
            print(sid, pid, inv) #techincally dont need seller_id, did incase out pid isnt working correctly
            Product.update_inventory(sid, pid, inv)
        else:
            print(sid, pid, inv) 
            Product.delete_pid(pid)
        return redirect(url_for('index.customer'))
    return render_template('update_inventory.html', title = 'Update Inventory', form = form)
                           #eller = sell)



class PriceForm(FlaskForm):
    price = FloatField(_l('price'), validators=[DataRequired()])
    submit = SubmitField(_l('Update'))

@bp.route('/edit_price/<pid>', methods=['GET', 'POST'])
def edit_price(pid):
    form = PriceForm()
    if form.validate_on_submit():
        Product.update_price(pid, form.price.data)
        return redirect(url_for('index.customer'))
    return render_template('edit_price.html', title = 'Update Price', form = form)
                           #eller = sell)



@bp.route('/edit_available/<pid>')
def edit_available(pid):
    return render_template('edit_available.html', choices = [True, False, pid])

@bp.route('/update_available/<pid>', methods=['GET', 'POST'])
def update_available(pid):
    select = request.form.get('available')
    #print(select)
    Product.update_available(pid, select)
    return redirect(url_for('index.customer'))
    return(str(select))


# class AvailForm(FlaskForm):
#     available = StringField(_l('available'), validators=[DataRequired()])
#     submit = SubmitField(_l('Update'))

# @bp.route('/edit_available/<pid>', methods=['GET', 'POST'])
# def edit_available(pid):
#     form = AvailForm()
#     if form.validate_on_submit():
#         Product.update_available(pid, form.available.data)
#         return redirect(url_for('index.customer'))
#     return render_template('edit_available.html', title = 'Update Available', form = form)
#                            #eller = sell)

#   class EditInventory(FlaskForm):
#     inventory = StringField(_l('Inventory'), validators=[DataRequired()])

# @bp.route('/edit_inventory/<pid>', methods=['GET', 'POST'])
# def edit_inventory(pid):
#     form = EditInventory()
#     if form.validate_on_submit():
#         Product.edit_inv(form.product.data)
#         return redirect(url_for('index.customer'))
#     return render_template('edit_inventory.html', 
#                             title = 'Edit Inventory', 
#                             form = form,
#                             product = )

#@bp.route('/delete_product/<sid>', methods=['POST', 'GET'])
#@bp.route('/delete_product/', methods=['POST', 'GET'])
#def delete_product(sid):
    # #products = Product.get_seller_info(sid)
    # products = Product.get_seller_info(sid)
    # pr = [(prod.name) for prod in products]
    # form = DeleteForm()
    # print(products)
    # form.product.choices = pr
    # if form.validate_on_submit():
    #     print(form.product.data)
    #     Product.delete(sid, form.product.data)
    #     return redirect(url_for('index.customer'))
    # return render_template('delete_product.html', title = 'Delete Product', form = form)
    #form = PostForm()
    # products = Product.get_seller_info(1)
    # if request.method == 'POST':
    #     select = request.form.get(products)
    # print(str(select))
    # else:
    #     return render_template('delete_product.html', products = products, form = form)
    # print('here')

#class DeleteForm(FlaskForm):
 #   product = SelectField(_l('Product'), validators=[DataRequired()])
  #  submit = SubmitField(_l('Delete'))
