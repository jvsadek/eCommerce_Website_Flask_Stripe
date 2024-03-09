from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from wtforms.validators import DataRequired, URL
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
import csv
import os
from random import randint
import stripe



app = Flask(__name__)
app.config['SECRET_KEY'] = 'FLASK_KEY'
app.config['STRIPE_PUBLIC_KEY'] = 'YOUR_STRIPE_PUBLIC_KEY'
app.config['STRIPE_SECRET_KEY'] = 'YOUR_STRIPE_SECRET_KEY'
stripe.api_key = app.config['STRIPE_SECRET_KEY']

# app.config['SECRET_KEY']=  os.environ.get('FLASK_KEY')
Bootstrap5(app)

# login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, './instance/store.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Transcation(db.Model):
    __tablename__ = "transcations"
    id = db.Column(db.Integer, primary_key=True)
    billing_first_name= db.Column(db.String(250), nullable=False)
    billing_last_name = db.Column(db.String(250), nullable=False)
    billing_email = db.Column(db.String(250), nullable=False)
    billing_address = db.Column(db.String(250), nullable=False)
    billing_city = db.Column(db.String(250), nullable=False)
    billing_country = db.Column(db.String(250), nullable=False)
    billing_zip_code = db.Column(db.String(250), nullable=False)
    billing_tel = db.Column(db.String(250), nullable=False)
    shipping_first_name = db.Column(db.String(250), nullable=True)
    shipping_last_name = db.Column(db.String(250), nullable=True)
    shipping_email = db.Column(db.String(250), nullable=True)
    shipping_address = db.Column(db.String(250), nullable=True)
    shipping_city = db.Column(db.String(250), nullable=True)
    shipping_country = db.Column(db.String(250), nullable=True)
    shipping_zip_code = db.Column(db.String(250), nullable=True)
    shipping_tel = db.Column(db.String(250), nullable=True)
    order_notes = db.Column(db.String(250), nullable=True)
    order_value = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    transaction_user = relationship("User", back_populates="transactions")

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), unique=False, nullable=False)
    product_image = db.Column(db.String(250), nullable=False)
    product_category = db.Column(db.String(250), nullable=False)
    product_price = db.Column(db.Integer, nullable=False)
    product_old_price = db.Column(db.Integer, nullable=False)
    product_currency = db.Column(db.String(250), nullable=False)
    product_rating = db.Column(db.Integer, primary_key=False)

class Checkout(db.Model):
    __tablename__ = "checkouts"
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), unique=False, nullable=False)
    product_image = db.Column(db.String(250), nullable=False)
    product_category = db.Column(db.String(250), nullable=False)
    product_price = db.Column(db.Integer, nullable=False)
    product_old_price = db.Column(db.Integer, nullable=False)
    product_currency = db.Column(db.String(250), nullable=False)
    product_rating = db.Column(db.Integer, primary_key=False)

class Wishlist(db.Model):
    __tablename__ = "wishes"
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(250), unique=False, nullable=False)
    product_image = db.Column(db.String(250), nullable=False)
    product_category = db.Column(db.String(250), nullable=False)
    product_price = db.Column(db.Integer, nullable=False)
    product_old_price = db.Column(db.Integer, nullable=False)
    product_currency = db.Column(db.String(250), nullable=False)
    product_rating = db.Column(db.Integer, primary_key=False)



class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    transactions = relationship("Transcation", back_populates="transaction_user")

# Create an admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function

@app.route("/")
def home():
    result = db.session.execute(db.select(Product))
    products = result.scalars().all()
    result_checkout = db.session.execute(db.select(Checkout))
    products_checkout = result_checkout.scalars().all()
    result_wishlist = db.session.execute(db.select(Wishlist))
    product_wishlist = result_wishlist.scalars().all()

    return render_template("index_rev1.html", all_products=products, checkout_products=products_checkout,wished_products=product_wishlist, randint = randint,
                           current_user=current_user)

@app.route("/product")
def product():
    return render_template("product.html", current_user=current_user)

@app.route("/store")
def store():
    return render_template("store.html")


@app.route("/checkout/<int:product_id>", methods=["GET", "POST"])
def product_checkout(product_id):
    product = db.get_or_404(Product, product_id)
    print(product_checkout)
    product_to_checkout = Checkout(
                    product_name= product.product_name,
                    product_image = product.product_image,
                    product_category = product.product_category,
                    product_price = product.product_price,
                    product_old_price = product.product_old_price,
                    product_currency = product.product_currency,
                    product_rating = product.product_rating)
    db.session.add(product_to_checkout)
    db.session.commit()
    if request.method == 'POST':
        return redirect(url_for("home"))
    # return render_template("checkout.html")

@app.route("/checkout_delete/<int:product_id>", methods=["GET", "POST"])
def checkout_delete(product_id):
    product = db.get_or_404(Checkout, product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/wishlist/<int:product_id>", methods=["GET", "POST"])
def product_wish(product_id):
    product = db.get_or_404(Product, product_id)
    # print(product_wish)
    product_to_wish = Wishlist(
                    product_name= product.product_name,
                    product_image = product.product_image,
                    product_category = product.product_category,
                    product_price = product.product_price,
                    product_old_price = product.product_old_price,
                    product_currency = product.product_currency,
                    product_rating = product.product_rating)
    db.session.add(product_to_wish)
    db.session.commit()
    return redirect(url_for("home"))
    # return render_template("checkout.html")

@app.route("/wishlist_delete/<int:product_id>", methods=["GET", "POST"])
def wishlist_delete(product_id):
    product = db.get_or_404(Wishlist, product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/move_to_chart/", methods=["GET", "POST"])
def move_to_chart():
    result = db.session.execute(db.select(Wishlist))
    wished_products = result.scalars().all()
    for product in wished_products:
        product_to_checkout = Checkout(
            product_name=product.product_name,
            product_image=product.product_image,
            product_category=product.product_category,
            product_price=product.product_price,
            product_old_price=product.product_old_price,
            product_currency=product.product_currency,
            product_rating=product.product_rating)
        db.session.add(product_to_checkout)
        db.session.commit()
        product_del = db.get_or_404(Wishlist, product.id)
        db.session.delete(product_del)
        db.session.commit()
    return redirect(url_for('home'))



@app.route("/transaction/<int:transaction_value>", methods=["GET", "POST"])
def transaction(transaction_value):
    if request.method == 'POST':
        print(request.form.get('terms_and_conditions'))
        print(request.form.get('place_order'))
        if request.form.get('place_order') and request.form.get('terms_and_conditions'):
            if request.form.get('place_order') and request.form.get('create-account'):
                # Check if user email is already present in the database.
                result = db.session.execute(db.select(User).where(User.email == request.form["billing-email"]))
                user = result.scalar()
                if user:
                    # User already exists
                    flash("You've already signed up with that email, log in instead!")
                    return redirect(url_for('checkout', total_checkout=transaction_value))

                hash_and_salted_password = generate_password_hash(
                    request.form["password"],
                    method='pbkdf2:sha256',
                    salt_length=8
                )
                new_user = User(
                    email=request.form["billing-email"],
                    name=request.form["billing-first-name"],
                    password=hash_and_salted_password,
                )
                db.session.add(new_user)
                db.session.commit()
                # This line will authenticate the user with Flask-Login
                login_user(new_user)
            new_transaction = Transcation(
                billing_first_name= request.form["billing-first-name"],
                billing_last_name = request.form["billing-last-name"],
                billing_email = request.form["billing-email"],
                billing_address = request.form["billing-address"],
                billing_city = request.form["billing-city"],
                billing_country = request.form["billing-country"],
                billing_zip_code = request.form["billing-zip-code"],
                billing_tel = request.form["billing-tel"],
                shipping_first_name = request.form["shipping-first-name"],
                shipping_last_name = request.form["shipping-last-name"],
                shipping_email = request.form["shipping-email"],
                shipping_address = request.form["shipping-address"],
                shipping_city = request.form["shipping-city"],
                shipping_country = request.form["shipping-country"],
                shipping_zip_code = request.form["shipping-zip-code"],
                shipping_tel = request.form["shipping-tel"],
                order_notes = request.form["order-notes"],
                order_value = transaction_value,
            )
            db.session.add(new_transaction)
            db.session.commit()
            return redirect(url_for('stripe_pay', price=transaction_value))

        else:
            flash("Please accept our terms and conditions to proceed!")
            return redirect(url_for('checkout', total_checkout=transaction_value))

@app.route("/stripe_pay/<int:price>", methods=["GET", "POST"])
def stripe_pay(price):
    print(price)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
              "price_data": {
                "currency": "usd",
                "product_data": {"name": "e-commerce-shopping"},
                "unit_amount": price*100,
                "tax_behavior": "exclusive",
              },
              "adjustable_quantity": {"enabled": False},
              "quantity": 1,
            },

        ],
        mode='payment',
        success_url=url_for('success_transacation', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('checkout', total_checkout=price,_external=True ),
    )
    # return {
    #     'checkout_session_id': session['id'],
    #     'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    # }
    return redirect(session.url, code=303)

@app.route("/success_transacation/", methods=["GET", "POST"])
def success_transacation():
    result = db.session.execute(db.select(Checkout))
    bought_products = result.scalars().all()
    for product in bought_products:
        product_del = db.get_or_404(Checkout, product.id)
        db.session.delete(product_del)
        db.session.commit()
    return redirect(url_for('home'))



@app.route("/checkout_cart/<int:total_checkout>", methods=["GET", "POST"])
def checkout(total_checkout):
    result_checkout = db.session.execute(db.select(Checkout))
    products_checkout = result_checkout.scalars().all()
    total_checkout_value = total_checkout
    print(total_checkout_value)
    return render_template("checkout.html", checkout_products=products_checkout, total_checkout=total_checkout_value, current_user=current_user )

@app.route("/blank")
def blank():
    return render_template("blank.html", current_user=current_user)

@app.route('/login', methods=["GET", "POST"])
def login():
    # form = LoginForm()
    if request.form.get('login'):
        email = request.form["email"],
        password = request.form["password"],
        result = db.session.execute(db.select(User).where(User.email == email[0]))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password[0]):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))

    return render_template("login.html", current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for(''))



if __name__ == '__main__':
    app.run(debug=True, port=5002)
