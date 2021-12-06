from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from app.models.seller import Seller
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.user import User


from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField(_l('First Name'), validators=[DataRequired()])
    lastname = StringField(_l('Last Name'), validators=[DataRequired()])
    address = StringField(_l('Address'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    seller = StringField(_l('Seller'), validators=[DataRequired()])                                    
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
        #print(form.email.data, form.password.data, form.firstname.data, form.lastname.data

        id1 = User.get_all() + 1

        if User.register(id1,
                         form.email.data,
                         form.address.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data):
            flash('Congratulations, you are now a registered user!')
            if form.seller.data.lower() == 'y' or form.seller.data.lower() == 'yes':
                Seller.register(id1)
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))



class NameForm(FlaskForm):
    firstname = StringField(_l('firstname')) #validators=[DataRequired()])
    lastname = StringField(_l('lastname')) #validators=[DataRequired()])
    submit = SubmitField(_l('Update'))

@bp.route('/edit_name/<uid>', methods=['GET', 'POST'])
def edit_name(uid):
    form = NameForm()
    if form.validate_on_submit():
        User.update_firstname(uid, form.firstname.data)
        User.update_lastname(uid, form.lastname.data)
        return redirect(url_for('index.customer'))
    return render_template('edit_name.html', title = 'Update Name', form = form)
                           #eller = sell)


class EmailForm(FlaskForm):
    email = StringField(_l('email'), validators=[DataRequired()])
    submit = SubmitField(_l('Update'))

@bp.route('/edit_email/<uid>', methods=['GET', 'POST'])
def edit_email(uid):
    form = EmailForm()
    if form.validate_on_submit():
        email = form.email.data
        print(email)
        if User.email_exists(email) == False:
            print(User.email_exists(email))
            User.update_email(uid, email)
        else:
            print(User.email_exists(email))
            flash('Email already exists')
        return redirect(url_for('index.customer'))
    return render_template('edit_email.html', title = 'Update Email', form = form)
                           #eller = sell)


class BalanceForm(FlaskForm):
    balance = DecimalField(_l('balance'), validators=[DataRequired()])
    submit = SubmitField(_l('Withdraw'))

@bp.route('/edit_balance/<uid>', methods=['GET', 'POST'])
def withdraw_balance(uid):
    form = BalanceForm()
    amount = User.get_balance(uid)[0][0]
    if form.validate_on_submit():
        if  form.balance.data <= amount and form.balance.data > 0:
            User.update_balance(uid, amount - form.balance.data)
            return redirect(url_for('index.customer'))
        elif form.balance.data > amount:
            message = "Withdrawing more than you have"
            return render_template('balance_withdraw_error.html', error = message)
        else:
            message = "Invalid quantity value"
            return render_template('balance_withdraw_error.html', error = message)
    return render_template('withdraw_balance.html', title = 'Add or Withdraw from Balance', form = form, balance = amount)


class BalanceForm1(FlaskForm):
    balance = DecimalField(_l('balance'), validators=[DataRequired()])
    submit = SubmitField(_l('Add'))

@bp.route('/add_balance/<uid>', methods=['GET', 'POST'])
def add_balance(uid):
    form = BalanceForm1()
    amount = User.get_balance(uid)[0][0]
    if form.validate_on_submit():
        if  form.balance.data > 0:
            User.add_balance(uid, amount + form.balance.data)
            return redirect(url_for('index.customer'))
        elif form.balance.data > amount:
            message = "Adding negative amount!"
            return render_template('balance_withdraw_error.html', error = message)
        else:
            message = "Invalid quantity value"
            return render_template('balance_withdraw_error.html', error = message)
    return render_template('add_balance.html', title = 'Add or Withdraw from Balance', form = form, balance = amount)


class AddyForm(FlaskForm):
    address = StringField(_l('Address'), validators=[DataRequired()])
    submit = SubmitField(_l('Update'))

@bp.route('/edit_addy/<uid>', methods=['GET', 'POST'])
def edit_addy(uid):
    form = AddyForm()
    if form.validate_on_submit():
        User.update_address(uid, form.address.data)
        return redirect(url_for('index.customer'))
    return render_template('edit_address.html', title = 'Update Address', form = form)
                          
