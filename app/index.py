from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask import request
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired
from flask_babel import _, lazy_gettext as _l

from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart
from .models.user import User
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('index', __name__)


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
    return render_template('index.html',
                           avail_products=products)
                           #purchase_history=purchases)

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
    coupon_code = StringField(_l('Coupon Code'), validators=[DataRequired()])
    submit = SubmitField(_l('Add'))


@bp.route('/edit_inventory/<sid>', methods=['GET', 'POST'])
def edit_inventory(sid):
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
        form.inventory.data, True, form.price.data, form.coupon_code.data)
        return redirect(url_for('index.customer'))
    return render_template('edit_inventory.html', title = 'Add Product', form = form)
                           #eller = sell)

""""
class RegistrationForm(FlaskForm):
    firstname = StringField(_l('First Name'), validators=[DataRequired()])
    lastname = StringField(_l('Last Name'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError(_('Already a user with this email.'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)
"""
