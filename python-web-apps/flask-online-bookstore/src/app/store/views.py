from flask import request, jsonify, Blueprint, flash, url_for, redirect, session
import json
from app import db, app
from app.models import Book, Category, Order
from flask import render_template
from PIL import Image 
import os 
from werkzeug.utils import secure_filename 
from flask_login import login_required, current_user

from app.store.forms import ProductForm, CategoryForm, CheckoutForm
from app.auth.auth_controller import role_required, forbid_admin_route


store = Blueprint('store', __name__, template_folder='templates') 

@store.route('/') 
@store.route('/home') 
def home(): 
    return render_template('home.html') 

@store.route('/book/<id>') 
def book(id): 
    book = Book.query.get_or_404(id) 
    return render_template('store/book.html', book=book)  

@store.route('/books') 
@store.route('/books/<int:page>') 
def books(page=1):
    per_page = 3  # Number of products per page
    books = Book.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('store/books.html', books=books)
 
@store.route('/book-create', methods=['GET', 'POST']) 
@role_required('admin')
def create_book(): 
    form = ProductForm()
 
    if form.validate_on_submit(): 
        name = form.name.data 
        price = form.price.data 
        category = Category.query.get_or_404( form.category.data ) 
        image = form.image.data  

        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Open the image using Pillow
            img = Image.open(image)
            
            # Resize the image to a desired size (e.g., maximum width of 800px)
            max_width = 400
            img.thumbnail((max_width, max_width))

            # Save the resized image
            img.save(image_path)
 
        book = Book(name, price, category, filename) 
        db.session.add(book) 
        db.session.commit() 
        flash('The book %s has been created' % name, 'success') 
        return redirect(url_for('store.book', id=book.id)) 
 
    if form.errors: 
        flash(form.errors, 'danger') 
 
    return render_template('store/book-create.html', form=form) 

@store.route('/category-create', methods=['GET', 'POST']) 
@role_required('admin')
def create_category(): 
    form = CategoryForm() 
 
    if form.validate_on_submit(): 
        name = form.name.data 
        category = Category(name) 
        db.session.add(category) 
        db.session.commit() 
        flash('The category %s has been created' % name, 
           'success') 
        return redirect(url_for('store.category', id=category.id)) 
 
    if form.errors: 
        flash(form.errors, "danger") 
 
    return render_template('store/category-create.html', form=form)

@store.route('/category/<id>') 
def category(id): 
    category = Category.query.get_or_404(id) 
    return render_template('store/category.html', category=category) 
 
 
@store.route('/categories') 
def categories(): 
    categories = Category.query.all() 
    return render_template('store/categories.html', 
       categories=categories) 




# Cart
class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def clear_cart(self):
        self.items = []

    def get_cart_items(self):
        return self.items

    def to_dict(self):
        return {'items': self.items}
    
    # TODO: Comanda de salvat in baza de date ca Order automat
    # Metoda.
    # La nivelul clientului trebuie sa existe o comanda de genul acesta
    # Transfer in ordin nou si golirea carutului
    # Trebuie in Session Bean

    @classmethod
    def from_dict(cls, cart_dict):
        cart = cls()
        cart.items = cart_dict.get('items', [])
        return cart


# Routes
@store.route('/add_to_cart/<int:book_id>', methods=['POST'])
@forbid_admin_route
def add_to_cart(book_id):
    # Retrieve the cart from the session or create a new one if it doesn't exist
    cart_dict = session.get('cart', {})
    cart = Cart.from_dict(cart_dict)

    book = Book.query.get_or_404(book_id)

    cart.add_item(book.id)

    session['cart'] = cart.to_dict()

    flash(f'Book {book.name} added to the cart', 'success')
    return redirect(url_for('store.books'))


@store.route('/view_cart')
@forbid_admin_route
def view_cart():
    # Retrieve the cart from the session or create a new one if it doesn't exist
    cart_dict = session.get('cart', {})
    cart = Cart.from_dict(cart_dict)

    # Retrieve book details based on cart items
    books = [get_book(book_id) for book_id in cart.get_cart_items()]

    return render_template('store/cart.html', cart=cart.get_cart_items(), books=books, get_book=get_book, calculate_total_price=calculate_total_price)



@store.route('/clear_cart')
def clear_cart():
    # Clear the cart in the session
    session.pop('cart', None)

    flash('Successfully cleared cart!', 'success')

    return redirect(url_for('store.home'))



# Checkout
@store.route('/checkout', methods=['GET', 'POST'])
# Corespunde unui Session Bean
# Session bean nu exista ca si componenta in Flask
@login_required
def checkout():
    form = CheckoutForm()

    if form.validate_on_submit():
        # Access the cart from the session
        
        cart_dict = session.get('cart', {})
        cart = Cart.from_dict(cart_dict)

        cart_items = cart_dict.get('items', []) 

        # Calculate the total price based on the items in the cart
        book_prices =  [Book.query.get(book_id).price for book_id in cart_items]

        # Calculate total price
        total_price = sum(book_prices)

        order = Order(name = form.full_name.data, email = form.email.data, address = form.address.data, city = form.city.data, user_id = current_user.id , price =  total_price, items = json.dumps(cart.to_dict()) )
        print(order)

        db.session.add(order)
        db.session.commit()
        flash('Order successfully placed!', 'success')
       

        flash('Checkout successful!', 'success')
        session.pop('cart', None)
        return redirect(url_for('store.home'))

    return render_template('store/checkout.html', form=form)


@store.route("/orders", methods=["GET", "POST"])
@role_required("admin")
def orders():
    all_orders = Order.query.all()
    return render_template("store/orders.html", orders=all_orders)















# UTILITIES

def get_book(book_id):
    return Book.query.get_or_404(book_id)

def calculate_total_price(cart):
    # Retrieve book prices based on the book IDs in the cart
    book_prices = [Book.query.get(book_id).price for book_id in cart]

    # Calculate the total price
    total_price = sum(book_prices)

    return total_price

def calculate_total_checkout_price(cart):
    items = "HERE" # Load a json instead or I don't know 
    book_prices = [Book.query.get(book_id).price * quantity for book_id, quantity in items.items()]
    total_price = sum(book_prices)
    return total_price