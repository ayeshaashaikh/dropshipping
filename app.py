import os
import re
from datetime import datetime
from decimal import Decimal

import pymysql
from flask import (Flask, flash, g, jsonify, redirect, render_template,
                   request, session, url_for)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with your secret key

bcrypt = Bcrypt(app)

# Folder for uploads
UPLOAD_FOLDER = os.path.join('static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions for images and videos
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov'}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Simple Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',           # Replace with your MySQL username
    'password': '',           # Replace with your MySQL password
    'database': 'dropshipping'  # Your database name is "dropshipping"
}

# Function to get a database connection
def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

# Close the database connection at the end of the request
@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def allowed_roles(roles):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] not in roles:
                flash('Access denied. Insufficient permissions.', 'danger')
                return redirect(url_for('home'))
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

# Home Route
@app.route('/')
def home():
    return render_template('home.html')

# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email    = request.form['email']
        password = request.form['password']
        role     = request.form.get('role', 'Customer')  # Defaults to 'Customer'
        
        db = get_db()
        with db.cursor() as cursor:
            # Check if a user with the same username or email already exists
            sql = "SELECT * FROM users WHERE username = %s OR email = %s"
            cursor.execute(sql, (username, email))
            existing_user = cursor.fetchone()
        
        if existing_user:
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('register'))
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Insert the new user into the database
        with db.cursor() as cursor:
            sql = "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (username, email, hashed_password, role))
        db.commit()
        
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']
        
        db = get_db()
        with db.cursor() as cursor:
            sql = "SELECT * FROM users WHERE email = %s"
            cursor.execute(sql, (email,))
            user = cursor.fetchone()
        
        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id']  = user['id']
            session['username'] = user['username']
            session['role']     = user['role']
            
            with db.cursor() as cursor:
                cursor.execute("UPDATE users SET last_login = NOW() WHERE id = %s", (user['id'],))
                db.commit()

            flash('Logged in successfully.', 'success')
            if user['role'] == 'Admin':
                return redirect('/admin/dashboard')
            elif user['role'] == 'Seller':
                return redirect('/seller/dashboard')
            elif user['role'] == 'Customer':
                return redirect('/customer/products')
            else:
                flash('Unknown role. Please contact support.', 'warning')
                return redirect(url_for('login'))  # Fallback
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# -------------------- Product Management Routes --------------------

# List products
@app.route('/products')
@allowed_roles(['Admin', 'Seller'])
def list_products():
    db = get_db()
    with db.cursor() as cursor:
        if session['role'] == 'Seller':
            sql = """SELECT products.*, category.name as category_name 
                     FROM products 
                     JOIN category ON products.category_id = category.id 
                     WHERE seller_id = %s"""
            cursor.execute(sql, (session['user_id'],))
        else:
            sql = """SELECT products.*, category.name as category_name 
                     FROM products 
                     JOIN category ON products.category_id = category.id"""
            cursor.execute(sql)
        products = cursor.fetchall()
    
    return render_template('products.html', products=products)

#seller products
@app.route('/seller/products')
@allowed_roles(['Admin', 'Seller'])
def seller_list_products():
    db = get_db()
    with db.cursor() as cursor:
        if session['role'] == 'Seller':
            sql = """SELECT products.*, category.name as category_name 
                     FROM products 
                     JOIN category ON products.category_id = category.id 
                     WHERE seller_id = %s"""
            cursor.execute(sql, (session['user_id'],))
        else:
            sql = """SELECT products.*, category.name as category_name 
                     FROM products 
                     JOIN category ON products.category_id = category.id"""
            cursor.execute(sql)
        products = cursor.fetchall()
    
    return render_template('seller_products.html', products=products)


# Add a new product with file upload support for image and video
@app.route('/product/add', methods=['GET', 'POST'])
@allowed_roles(['Admin', 'Seller'])
def add_product():
    db = get_db()
    
    # Fetch categories from DB
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM category")
        categories = cursor.fetchall()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category_id = request.form['category']  # Now stores category ID
        seller_id = session['user_id']

        # Initialize file paths
        image_path = ''
        video_path = ''

        # Handle image upload
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            if image_file and allowed_file(image_file.filename, ALLOWED_IMAGE_EXTENSIONS):
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)
                image_path = '/' + image_path.replace("\\", "/")

        # Handle video upload (optional)
        if 'video_file' in request.files:
            video_file = request.files['video_file']
            if video_file and allowed_file(video_file.filename, ALLOWED_VIDEO_EXTENSIONS):
                filename = secure_filename(video_file.filename)
                video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                video_file.save(video_path)
                video_path = '/' + video_path.replace("\\", "/")

        # Insert into database
        with db.cursor() as cursor:
            sql = """INSERT INTO products (name, description, image, video, price, category_id, seller_id) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (name, description, image_path, video_path, price, category_id, seller_id))
        db.commit()

        flash('Product added successfully.', 'success')
        return redirect(url_for('list_products'))

    return render_template('add_product.html', categories=categories)

#seller add product
# Add a new product with file upload support for image and video
@app.route('/seller/product/add', methods=['GET', 'POST'])
@allowed_roles(['Seller'])
def seller_add_product():
    db = get_db()
    
    # Fetch categories from DB
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM category")
        categories = cursor.fetchall()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category_id = request.form['category']  # Now stores category ID
        seller_id = session['user_id']

        # Initialize file paths
        image_path = ''
        video_path = ''

        # Handle image upload
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            if image_file and allowed_file(image_file.filename, ALLOWED_IMAGE_EXTENSIONS):
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)
                image_path = '/' + image_path.replace("\\", "/")

        # Handle video upload (optional)
        if 'video_file' in request.files:
            video_file = request.files['video_file']
            if video_file and allowed_file(video_file.filename, ALLOWED_VIDEO_EXTENSIONS):
                filename = secure_filename(video_file.filename)
                video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                video_file.save(video_path)
                video_path = '/' + video_path.replace("\\", "/")

        # Insert into database
        with db.cursor() as cursor:
            sql = """INSERT INTO products (name, description, image, video, price, category_id, seller_id) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (name, description, image_path, video_path, price, category_id, seller_id))
        db.commit()

        flash('Product added successfully.', 'success')
        return redirect(url_for('seller_list_products'))

    return render_template('seller_add_product.html', categories=categories)

# Edit product with file upload support (optional new uploads)
@app.route('/product/edit/<int:product_id>', methods=['GET', 'POST'])
@allowed_roles(['Admin', 'Seller'])
def edit_product(product_id):
    db = get_db()
    
    # Fetch product details
    with db.cursor() as cursor:
        sql = "SELECT * FROM products WHERE id = %s"
        cursor.execute(sql, (product_id,))
        product = cursor.fetchone()
    
    # Fetch categories from DB
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM category")
        categories = cursor.fetchall()
    
    if session['role'] == 'Seller' and product['seller_id'] != session['user_id']:
        flash('Access denied. You can only edit your own products.', 'danger')
        return redirect(url_for('list_products'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category_id = request.form['category']  # Now stores category ID

        image_path = product['image']
        video_path = product['video']

        # Check for new image upload
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            if image_file and allowed_file(image_file.filename, ALLOWED_IMAGE_EXTENSIONS):
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)
                image_path = '/' + image_path.replace("\\", "/")

        # Check for new video upload
        if 'video_file' in request.files:
            video_file = request.files['video_file']
            if video_file and allowed_file(video_file.filename, ALLOWED_VIDEO_EXTENSIONS):
                filename = secure_filename(video_file.filename)
                video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                video_file.save(video_path)
                video_path = '/' + video_path.replace("\\", "/")

        # Update product in DB
        with db.cursor() as cursor:
            sql = """UPDATE products 
                     SET name=%s, description=%s, image=%s, video=%s, price=%s, category_id=%s 
                     WHERE id=%s"""
            cursor.execute(sql, (name, description, image_path, video_path, price, category_id, product_id))
        db.commit()
        
        flash('Product updated successfully.', 'success')
        return redirect(url_for('list_products'))

    return render_template('edit_product.html', product=product, categories=categories)

#seller edit product
# Edit product with file upload support (optional new uploads)
@app.route('/seller/product/edit/<int:product_id>', methods=['GET', 'POST'])
@allowed_roles(['Admin', 'Seller'])
def seller_edit_product(product_id):
    db = get_db()
    
    # Fetch product details
    with db.cursor() as cursor:
        sql = "SELECT * FROM products WHERE id = %s"
        cursor.execute(sql, (product_id,))
        product = cursor.fetchone()
        
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM category")
        categories = cursor.fetchall()
    # Fetch categories from DB
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM category")
        categories = cursor.fetchall()
    
    if session['role'] == 'Seller' and product['seller_id'] != session['user_id']:
        flash('Access denied. You can only edit your own products.', 'danger')
        return redirect(url_for('list_products'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category_id = request.form['category'] 

        image_path = product['image']
        video_path = product['video']

        # Check for new image upload
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            if image_file and allowed_file(image_file.filename, ALLOWED_IMAGE_EXTENSIONS):
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)
                image_path = '/' + image_path.replace("\\", "/")

        # Check for new video upload
        if 'video_file' in request.files:
            video_file = request.files['video_file']
            if video_file and allowed_file(video_file.filename, ALLOWED_VIDEO_EXTENSIONS):
                filename = secure_filename(video_file.filename)
                video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                video_file.save(video_path)
                video_path = '/' + video_path.replace("\\", "/")

        # Update product in DB
        with db.cursor() as cursor:
            sql = """UPDATE products 
                     SET name=%s, description=%s, image=%s, video=%s, price=%s, category_id=%s 
                     WHERE id=%s"""
            cursor.execute(sql, (name, description, image_path, video_path, price, category_id, product_id))
        db.commit()
        
        flash('Product updated successfully.', 'success')
        return redirect(url_for('seller_list_products'))

    return render_template('seller_edit_products.html', product=product, categories=categories)


# Delete product
@app.route('/product/delete/<int:product_id>')
@allowed_roles(['Admin', 'Seller'])
def delete_product(product_id):
    db = get_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM products WHERE id = %s"
        cursor.execute(sql, (product_id,))
        product = cursor.fetchone()
    
    if session['role'] == 'Seller' and product['seller_id'] != session['user_id']:
        flash('Access denied. You can only delete your own products.', 'danger')
        return redirect(url_for('list_products'))
    
    with db.cursor() as cursor:
        sql = "DELETE FROM products WHERE id = %s"
        cursor.execute(sql, (product_id,))
    db.commit()
    
    flash('Product deleted successfully.', 'success')
    return redirect(url_for('list_products'))

#seller delete product
@app.route('/seller/product/delete/<int:product_id>')
@allowed_roles(['Admin', 'Seller'])
def seller_delete_product(product_id):
    db = get_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM products WHERE id = %s"
        cursor.execute(sql, (product_id,))
        product = cursor.fetchone()
    
    if session['role'] == 'Seller' and product['seller_id'] != session['user_id']:
        flash('Access denied. You can only delete your own products.', 'danger')
        return redirect(url_for('list_products'))
    
    with db.cursor() as cursor:
        sql = "DELETE FROM products WHERE id = %s"
        cursor.execute(sql, (product_id,))
    db.commit()
    
    flash('Product deleted successfully.', 'success')
    return redirect(url_for('seller_list_products'))

@app.route('/wishlist/add', methods=['POST'])
def add_to_wishlist():
    db = get_db()
    user_id = session.get('user_id')
    product_id = request.form.get('product_id')

    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM wishlist WHERE user_id=%s AND product_id=%s", (user_id, product_id))
        existing = cursor.fetchone()

        if not existing:
            cursor.execute("INSERT INTO wishlist (user_id, product_id) VALUES (%s, %s)", (user_id, product_id))
        db.commit()
        
    return redirect(url_for('customer_products'))


@app.route('/wishlist/remove', methods=['POST'])
def remove_from_wishlist():
    db = get_db()
    user_id = session.get('user_id')
    product_id = request.form.get('product_id')

    with db.cursor() as cursor:
        cursor.execute("DELETE FROM wishlist WHERE user_id=%s AND product_id=%s", (user_id, product_id))
    db.commit()

    return redirect(url_for('wishlist'))


@app.route('/wishlist')
def wishlist():
    db = get_db()
    user_id = session.get('user_id')

    with db.cursor() as cursor:
        cursor.execute("""
            SELECT products.* FROM products
            JOIN wishlist ON products.id = wishlist.product_id
            WHERE wishlist.user_id = %s
        """, (user_id,))
        wishlist_items = cursor.fetchall()

    return render_template("wishlist.html", wishlist_items=wishlist_items)


@app.route('/customer/products')
@allowed_roles(['Customer'])
def customer_products():
    db = get_db()

    # 1) Read filter & sort parameters from query string
    search       = request.args.get('search', '', type=str)
    cat_ids      = request.args.getlist('category', type=int)
    price_max    = request.args.get('price_max', type=float)
    sort_option  = request.args.get('sort', 'newest')
    page         = request.args.get('page', 1, type=int)
    per_page     = 6
    offset       = (page - 1) * per_page

    # 2) Build dynamic SQL
    base_sql = """
      FROM products p
      JOIN category c ON p.category_id = c.id
      WHERE 1=1
    """
    filters = []
    params = []

    if search:
        base_sql += " AND p.name LIKE %s"
        params.append(f"%{search}%")
    if cat_ids:
        placeholders = ",".join(["%s"] * len(cat_ids))
        base_sql += f" AND p.category_id IN ({placeholders})"
        params.extend(cat_ids)
    if price_max is not None:
        base_sql += " AND p.price <= %s"
        params.append(price_max)

    # 3) Apply sorting
    order_by = " ORDER BY p.id DESC"  # Default: newest
    if sort_option == 'price-asc':
        order_by = " ORDER BY p.price ASC"
    elif sort_option == 'price-desc':
        order_by = " ORDER BY p.price DESC"

    # Final SQL queries
    data_sql = f"SELECT p.*, c.name AS category_name {base_sql} {order_by} LIMIT %s OFFSET %s"
    count_sql = f"SELECT COUNT(*) AS count {base_sql}"
    data_params = params + [per_page, offset]
    count_params = params

    with db.cursor() as cursor:
        # Fetch products
        cursor.execute(data_sql, data_params)
        products = cursor.fetchall()

        # Fetch total count for pagination
        cursor.execute(count_sql, count_params)
        total_products = cursor.fetchone()['count']

        # Fetch categories
        cursor.execute("SELECT id, name FROM category ORDER BY name")
        categories = cursor.fetchall()

    total_pages = (total_products + per_page - 1) // per_page    

    # Compute cart badge count
    cart = session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())

    return render_template(
        'customer_products.html',
        products=products,
        categories=categories,
        cart_count=cart_count,
        current_search=search,
        current_cats=cat_ids,
        current_price=price_max or '',
        current_sort=sort_option,
        current_page=page,
        total_pages=total_pages
    )

@app.route('/cart')
@allowed_roles(['Customer'])
def cart():
    user_id = session.get('user_id')
    db = get_db()
    with db.cursor() as cursor:
        sql = """
        SELECT c.*, p.name, p.price, p.image 
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
        """
        cursor.execute(sql, (user_id,))
        cart_items = cursor.fetchall()
    return render_template('cart.html', cart_items=cart_items)

@app.route('/add_category', methods=['GET', 'POST'])
@allowed_roles(['Admin'])  # Optional: Restrict category addition to Admin
def add_category():
    db = get_db()

    if request.method == 'POST':
        category_name = request.form['category_name']
        
        # Ensure category_name is not empty
        if not category_name.strip():
            flash("Category name cannot be empty.", "danger")
            return redirect(url_for('add_category'))

        with db.cursor() as cursor:
            sql = "INSERT INTO category (name) VALUES (%s)"
            cursor.execute(sql, (category_name,))
        db.commit()

        flash("Category added successfully!", "success")
        return redirect(url_for('add_category'))

    return render_template('add_category.html')



# Add to Cart: Store cart data in the database
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@allowed_roles(['Customer'])
def add_to_cart(product_id):
    user_id = session.get('user_id')
    db = get_db()
    # Verify product exists
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
    if not product:
        return {"message": "Product not found."}

    # Check if product already exists in the cart for this user
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
        cart_item = cursor.fetchone()

    if cart_item:
        # Update quantity if product already in cart
        new_quantity = cart_item['quantity'] + 1
        with db.cursor() as cursor:
            cursor.execute("UPDATE cart SET quantity = %s, added_at = NOW() WHERE id = %s", (new_quantity, cart_item['id']))
    else:
        # Insert new cart record
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO cart (user_id, product_id, quantity, added_at) VALUES (%s, %s, %s, NOW())",
                (user_id, product_id, 1)
            )
    db.commit()
    return {"message": "Product added to cart!"}


@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
@allowed_roles(['Customer'])
def remove_from_cart(product_id):
    user_id = session.get('user_id')
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
    db.commit()
    flash("Item removed from cart.", "info")
    return redirect(url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
@allowed_roles(['Customer'])
def checkout():
    user_id = session.get('user_id')
    db = get_db()
    if request.method == 'POST':
        with db.cursor() as cursor:
            sql = """
            SELECT c.*, p.price
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = %s
            """
            cursor.execute(sql, (user_id,))
            cart_items = cursor.fetchall()
        if not cart_items:
            flash("Your cart is empty!", "danger")
            return redirect(url_for('cart'))
        
        total_amount = sum(item['price'] * item['quantity'] for item in cart_items)
        with db.cursor() as cursor:
            # Insert new order record
            sql = "INSERT INTO orders (user_id, total_price, status, created_at) VALUES (%s, %s, %s, NOW())"
            cursor.execute(sql, (user_id, total_amount, 'Pending'))
            order_id = cursor.lastrowid
            # Insert each cart item into order_items
            for item in cart_items:
                sql = "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (order_id, item['product_id'], item['quantity'], item['price']))
            # Clear the customer's cart
            cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
        db.commit()
        flash("Order placed successfully!", "success")
        return redirect(url_for('order_history'))
    else:
        # For GET request: display cart details for checkout confirmation.
        with db.cursor() as cursor:
            sql = """
            SELECT c.*, p.name, p.price, p.image 
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = %s
            """
            cursor.execute(sql, (user_id,))
            cart_items = cursor.fetchall()
        return render_template('checkout.html', cart_items=cart_items)

@app.route('/order_history')
@allowed_roles(['Customer'])
def order_history():
    user_id = session['user_id']
    
    db = get_db()
    with db.cursor() as cursor:
        sql = """SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC"""
        cursor.execute(sql, (user_id,))
        orders = cursor.fetchall()
    
    return render_template('order_history.html', orders=orders)

#admin view order
@app.route('/orders')
@allowed_roles(['Admin','Seller'])
def view_orders():
    db = get_db()
    with db.cursor() as cursor:
        if session['role'] == 'Seller':
            sql = """
            SELECT o.id AS order_id, o.status, o.created_at, 
                   oi.quantity, oi.price, 
                   p.name AS product_name, u.username AS customer_name
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            JOIN products p ON oi.product_id = p.id
            JOIN users u ON o.user_id = u.id
            WHERE p.seller_id = %s
            ORDER BY o.created_at DESC
            """
            cursor.execute(sql, (session['user_id'],))
        else:  # Admin
            sql = """
            SELECT o.id AS order_id, o.status, o.created_at, 
                   oi.quantity, oi.price, 
                   p.name AS product_name, u.username AS customer_name
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            JOIN products p ON oi.product_id = p.id
            JOIN users u ON o.user_id = u.id
            ORDER BY o.created_at DESC
            """
            cursor.execute(sql)
        orders = cursor.fetchall()
    return render_template('view_orders.html', orders=orders)

@app.route('/order/update_status/<int:order_id>', methods=['POST'])
@allowed_roles(['Admin', 'Seller'])
def update_order_status(order_id):
    new_status = request.form['new_status']
    db = get_db()
    with db.cursor() as cursor:
        sql = "UPDATE orders SET status = %s WHERE id = %s"
        cursor.execute(sql, (new_status, order_id))
    db.commit()
    flash("Order status updated successfully!", "success")
    return redirect(url_for('view_orders'))

@app.route('/seller/order/update_status/<int:order_id>', methods=['POST'])
@allowed_roles(['Admin', 'Seller'])
def seller_update_order_status(order_id):
    new_status = request.form['new_status']
    db = get_db()
    with db.cursor() as cursor:
        sql = "UPDATE orders SET status = %s WHERE id = %s"
        cursor.execute(sql, (new_status, order_id))
    db.commit()
    flash("Order status updated successfully!", "success")
    return redirect(url_for('seller_view_orders'))

#seller view order
@app.route('/seller/orders')
@allowed_roles(['Seller'])
def seller_view_orders():
    db = get_db()
    with db.cursor() as cursor:
        if session['role'] == 'Seller':
            sql = """
            SELECT o.id AS order_id, o.status, o.created_at, 
                   oi.quantity, oi.price, 
                   p.name AS product_name, u.username AS customer_name
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            JOIN products p ON oi.product_id = p.id
            JOIN users u ON o.user_id = u.id
            WHERE p.seller_id = %s
            ORDER BY o.created_at DESC
            """
            cursor.execute(sql, (session['user_id'],))
        
        orders = cursor.fetchall()
    return render_template('seller_view_orders.html', orders=orders)


# @app.route('/admin/dashboard')
# @allowed_roles(['Admin'])
# def admin_dashboard():
#     db = get_db()
#     with db.cursor() as cursor:
#         cursor.execute("SELECT COUNT(*) AS total_orders, COALESCE(SUM(total_price), 0) AS total_revenue FROM orders")
#         orders_summary = cursor.fetchone()

#         cursor.execute("SELECT COUNT(*) AS total_sellers FROM users WHERE role = 'Seller'")
#         seller_summary = cursor.fetchone()

#         cursor.execute("SELECT COUNT(*) AS total_customers FROM users WHERE role = 'Customer'")
#         customer_summary = cursor.fetchone()

#     return render_template(
#         'admin_dashboard.html',
#         orders_summary=orders_summary,
#         seller_summary=seller_summary,
#         customer_summary=customer_summary
#     )
@app.route('/admin/dashboard')
@allowed_roles(['Admin'])
def admin_dashboard():
    db = get_db()

    with db.cursor() as cursor:
        # Website Statistics
        cursor.execute("SELECT COUNT(*) AS total_orders FROM orders")
        total_orders = cursor.fetchone()['total_orders']

        cursor.execute("SELECT COUNT(*) AS total_sellers FROM users WHERE role='Seller' AND is_blocked=0")
        active_sellers = cursor.fetchone()['total_sellers']

        cursor.execute("SELECT COUNT(*) AS total_customers FROM users WHERE role='Customer' AND is_blocked=0")
        active_customers = cursor.fetchone()['total_customers']

        # Monthly Sales and Orders
        cursor.execute("""
            SELECT DATE_FORMAT(created_at, '%Y-%m') AS month, COUNT(*) AS order_count, SUM(total_price) AS sales
            FROM orders
            GROUP BY month
            ORDER BY month ASC
        """)
        rows = cursor.fetchall()
        
                # User activity heatmap (logins or registrations or any tracked activity)
        cursor.execute("""
            SELECT 
                HOUR(last_login) AS hour,
                DAYOFWEEK(last_login) AS weekday,
                COUNT(*) AS activity_count
            FROM users
            WHERE last_login IS NOT NULL
            GROUP BY weekday, hour
        """)
        activity_rows = cursor.fetchall()

    # Heatmap matrix
    heatmap_data = [{'x': row['weekday'], 'y': row['hour'], 'v': row['activity_count']} for row in activity_rows]


    # Prepare chart data
    months = [row['month'] for row in rows]
    order_counts = [row['order_count'] for row in rows]
    sales = [float(row['sales']) if row['sales'] else 0 for row in rows]

    return render_template('admin_dashboard.html',
                           total_orders=total_orders,
                           active_sellers=active_sellers,
                           active_customers=active_customers,
                           months=months,
                           order_counts=order_counts,
                           sales=sales,
                           heatmap_data=heatmap_data)



@app.route('/admin/users', methods=['GET', 'POST'])
@allowed_roles(['Admin'])
def manage_users():
    db = get_db()

    if request.method == 'POST':
        user_id = request.form['user_id']
        action = request.form['action']

        with db.cursor() as cursor:
            if action == 'block':
                cursor.execute("UPDATE users SET is_blocked = 1 WHERE id = %s", (user_id,))
            elif action == 'unblock':
                cursor.execute("UPDATE users SET is_blocked = 0 WHERE id = %s", (user_id,))
        db.commit()
        return redirect(url_for('manage_users'))

    with db.cursor() as cursor:
        cursor.execute("SELECT id, username, email, role, is_blocked FROM users WHERE role != 'Admin'")
        users = cursor.fetchall()
    
    return render_template('manage_users.html', users=users)

@app.route('/seller/dashboard')
@allowed_roles(['Seller'])
def seller_dashboard():
    connection = get_db()

    # Get seller info from session
    seller_id = session.get('user_id')
    seller_name = session.get('username')  # Optional: if you want to greet user

    if not seller_id:
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))

    with connection.cursor() as cursor:
        # Total Orders
        cursor.execute("""
            SELECT COUNT(DISTINCT o.id) AS total_orders
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            JOIN products p ON oi.product_id = p.id
            WHERE p.seller_id = %s
        """, (seller_id,))
        total_orders = cursor.fetchone()['total_orders'] or 0

        # Total Revenue
        cursor.execute("""
            SELECT SUM(oi.quantity * oi.price) AS total_revenue
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE p.seller_id = %s
        """, (seller_id,))
        total_revenue = cursor.fetchone()['total_revenue'] or 0

        # Pending Orders
        cursor.execute("""
            SELECT COUNT(DISTINCT o.id) AS pending_orders
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            JOIN products p ON oi.product_id = p.id
            WHERE p.seller_id = %s AND o.status = 'Pending'
        """, (seller_id,))
        pending_orders = cursor.fetchone()['pending_orders'] or 0

        # Shipped Orders
        cursor.execute("""
            SELECT COUNT(DISTINCT o.id) AS shipped_orders
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            JOIN products p ON oi.product_id = p.id
            WHERE p.seller_id = %s AND o.status = 'Shipped'
        """, (seller_id,))
        shipped_orders = cursor.fetchone()['shipped_orders'] or 0
        
        cursor.execute("""
            SELECT COUNT(*) AS total_products
            FROM products
            WHERE seller_id = %s
        """, (seller_id,))
        total_products = cursor.fetchone()['total_products'] or 0
        
        cursor.execute("""
        SELECT 
        MONTH(o.created_at) AS month,
        SUM(oi.quantity * oi.price) AS revenue
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN products p ON oi.product_id = p.id
        WHERE p.seller_id = %s AND YEAR(o.created_at) = YEAR(CURDATE())
        GROUP BY MONTH(o.created_at)
        ORDER BY month
        """, (seller_id,))

        monthly_data = cursor.fetchall()

# Format data for chart
        monthly_revenue = [0] * 12  # Jan to Dec
        for row in monthly_data:
            month_index = row['month'] - 1
            monthly_revenue[month_index] = float(row['revenue'] or 0)

    return render_template(
        'seller_dashboard.html',
        seller_name=seller_name,
        total_orders=total_orders,
        total_revenue=total_revenue,
        pending_orders=pending_orders,
        shipped_orders=shipped_orders,
        total_products=total_products,
        monthly_revenue=monthly_revenue
    )


@app.route('/chat', methods=['POST'])
def chat():
    db = get_db()
    cur = db.cursor()

    user_message = request.json.get('message', '').lower()
    user_id      = session.get('user_id')
    username     = session.get('username', 'Guest')

    # 1) Save the user message
    cur.execute(
        "INSERT INTO chatbot_history (user_id, message, is_bot) VALUES (%s, %s, %s)",
        (user_id, user_message, False)
    )

    reply = "I'm still learning. Type 'help' to see what I can do."

    # 2) Greeting
    if any(g in user_message for g in ['hi', 'hello', 'hey']):
        reply = f"Hi {username}! How can I assist you today?"

    # 3) Help menu
    elif 'help' in user_message:
        reply = (
            "I can help with:\n"
            "- Show my orders\n"
            "- Status of order [ID]\n"
            "- Items in order [ID]\n"
            "- Cancel order [ID]\n"
            "- Recommend popular products\n"
            "- Tell me about [product name]\n"
            "- Show categories\n"
            "- Show products in [category]\n"
            "- Show my wishlist\n"
            "- Add [product] to wishlist\n"
            "- Remove [product] from wishlist\n"
            "- Show my cart\n"
            "- My profile\n"
            "- Shipping times\n"
            "- Return policy\n"
            "- Contact info"
        )

    # 4) Recent orders
    elif 'my orders' in user_message:
        if not user_id:
            reply = "Please log in to view your orders."
        else:
            cur.execute(
                "SELECT id, status, total_price FROM orders "
                "WHERE user_id=%s ORDER BY created_at DESC LIMIT 3",
                (user_id,)
            )
            orders = cur.fetchall()
            if not orders:
                reply = "You don't have any orders yet."
            else:
                lines = [f"Order #{o['id']} – ${o['total_price']} – {o['status']}" for o in orders]
                reply = "Here are your recent orders:\n" + "\n".join(lines)

    # 5) Order status
    elif 'status' in user_message and 'order' in user_message:
        order_id = ''.join(filter(str.isdigit, user_message))
        if not order_id:
            reply = "Please specify an order ID, e.g. 'status of order 123'."
        else:
            cur.execute(
                "SELECT status FROM orders WHERE id=%s AND user_id=%s",
                (order_id, user_id)
            )
            order = cur.fetchone()
            if order:
                reply = f"Status of order #{order_id}: {order['status']}."
            else:
                reply = "I couldn't find that order."

    # 6) Items in an order
    elif 'items in order' in user_message:
        order_id = ''.join(filter(str.isdigit, user_message))
        if not order_id:
            reply = "Please specify an order ID, e.g. 'items in order 123'."
        else:
            cur.execute(
                "SELECT oi.quantity, oi.price, p.name "
                "FROM order_items oi JOIN products p ON oi.product_id=p.id "
                "WHERE oi.order_id=%s",
                (order_id,)
            )
            items = cur.fetchall()
            if items:
                lines = [f"{i['name']} x{i['quantity']} = ${i['price']*i['quantity']:.2f}" for i in items]
                reply = f"Items in order #{order_id}:\n" + "\n".join(lines)
            else:
                reply = f"No items found for order #{order_id}."

    # 7) Cancel order
    elif 'cancel order' in user_message:
        order_id = ''.join(filter(str.isdigit, user_message))
        if not order_id:
            reply = "Please specify an order ID to cancel, e.g. 'cancel order 123'."
        else:
            cur.execute(
                "SELECT status FROM orders WHERE id=%s AND user_id=%s",
                (order_id, user_id)
            )
            order = cur.fetchone()
            if not order:
                reply = "I couldn't find that order."
            elif order['status'] not in ('Pending', 'Processing'):
                reply = f"Order #{order_id} cannot be canceled (current status: {order['status']})."
            else:
                cur.execute(
                    "UPDATE orders SET status='Cancelled' WHERE id=%s",
                    (order_id,)
                )
                db.commit()
                reply = f"Order #{order_id} has been canceled."

    # 8) Popular / trending products
    elif any(w in user_message for w in ['popular', 'trending', 'recommend']):
        cur.execute("SELECT name, price FROM products ORDER BY id DESC LIMIT 3")
        prods = cur.fetchall()
        lines = [f"{p['name']} – ${p['price']}" for p in prods]
        reply = "Check out these products:\n" + "\n".join(lines)

    # 9) Product details
    elif 'tell me about' in user_message or 'details of' in user_message:
        keywords = user_message.replace('tell me about', '').replace('details of', '').strip()
        cur.execute(
            "SELECT name, description, price FROM products WHERE name LIKE %s LIMIT 1",
            (f"%{keywords}%",)
        )
        prod = cur.fetchone()
        if prod:
            reply = f"{prod['name']} – ${prod['price']}\nDescription: {prod['description']}"
        else:
            reply = "I couldn't find that product."

    # 10) Shipping info
    elif 'shipping' in user_message or 'delivery time' in user_message:
        reply = "Standard shipping takes 3-5 business days. Express shipping options are available at checkout."

    # 11) Return/refund policy
    elif 'return' in user_message or 'refund' in user_message:
        reply = "You can return products within 14 days of delivery. Refunds process within 5-7 business days."

    # 12) Contact/support
    elif 'contact' in user_message or 'support' in user_message:
        reply = "Contact us at support@example.com or call 1-800-123-4567."

    # 13) Show categories
    elif 'category' in user_message or 'categories' in user_message:
        cur.execute("SELECT name FROM category")
        cats = cur.fetchall()
        if cats:
            reply = "We have these categories:\n" + "\n".join(c['name'] for c in cats)
        else:
            reply = "No categories found."

    # 14) Products in a category
    elif 'products in ' in user_message:
        cat_name = user_message.split('products in ')[1].strip()
        cur.execute("SELECT id FROM category WHERE name LIKE %s LIMIT 1", (f"%{cat_name}%",))
        cat = cur.fetchone()
        if cat:
            cur.execute(
                "SELECT name, price FROM products WHERE category_id=%s LIMIT 5",
                (cat['id'],)
            )
            prods = cur.fetchall()
            if prods:
                lines = [f"{p['name']} – ${p['price']}" for p in prods]
                reply = f"Products in {cat_name}:\n" + "\n".join(lines)
            else:
                reply = f"No products found in {cat_name}."
        else:
            reply = f"I couldn't find category '{cat_name}'."

    # 15) Show my wishlist
    elif 'my wishlist' in user_message or 'show wishlist' in user_message:
        if not user_id:
            reply = "Please log in to view your wishlist."
        else:
            cur.execute(
                "SELECT p.name, p.price FROM wishlist w "
                "JOIN products p ON w.product_id = p.id "
                "WHERE w.user_id = %s",
                (user_id,)
            )
            items = cur.fetchall()
            if items:
                reply = "Your wishlist:\n" + "\n".join(f"{i['name']} – ${i['price']}" for i in items)
            else:
                reply = "Your wishlist is empty."

    # 16) Add to wishlist
    elif re.match(r'^add\s+(.+?)\s+to\s+wishlist$', user_message):
        if not user_id:
            reply = "Please log in to add to your wishlist."
        else:
            prod_name = re.match(r'^add\s+(.+?)\s+to\s+wishlist$', user_message).group(1)
            cur.execute(
                "SELECT id FROM products WHERE name LIKE %s LIMIT 1",
                (f"%{prod_name}%",)
            )
            prod = cur.fetchone()
            if prod:
                cur.execute(
                    "INSERT IGNORE INTO wishlist (user_id, product_id) VALUES (%s, %s)",
                    (user_id, prod['id'])
                )
                db.commit()
                reply = f"Added **{prod_name}** to your wishlist."
            else:
                reply = f"Could not find product '{prod_name}'."

    # 17) Remove from wishlist
    elif re.match(r'^remove\s+(.+?)\s+from\s+wishlist$', user_message):
        prod_name = re.match(r'^remove\s+(.+?)\s+from\s+wishlist$', user_message).group(1).strip()
        if not user_id:
            reply = "Please log in to modify your wishlist."
        else:
            cur.execute(
            "SELECT id FROM products WHERE name LIKE %s LIMIT 1",
            (f"%{prod_name}%",)
             )
            prod = cur.fetchone()
            if prod:
                cur.execute(
                "DELETE FROM wishlist WHERE user_id=%s AND product_id=%s",
                (user_id, prod['id'])
            )
                db.commit()
                reply = f"Removed **{prod_name}** from your wishlist."
            else:
                reply = f"Could not find product '{prod_name}'."

    # 18) Show my cart
    elif 'my cart' in user_message or 'show cart' in user_message:
        cart = session.get('cart', {})
        if not cart:
            reply = "Your cart is empty."
        else:
            lines = []
            total = 0
            for pid, item in cart.items():
                cur.execute("SELECT name, price FROM products WHERE id=%s", (pid,))
                p = cur.fetchone()
                subtotal = p['price'] * item['quantity']
                total += subtotal
                lines.append(f"{p['name']} x{item['quantity']} = ${subtotal:.2f}")
            lines.append(f"Total: ${total:.2f}")
            reply = "Your cart contains:\n" + "\n".join(lines)

    # 19) My profile info
    elif 'my profile' in user_message or 'profile' in user_message:
        if not user_id:
            reply = "Please log in to view your profile."
        else:
            cur.execute(
                "SELECT username, email, role, last_login FROM users WHERE id=%s",
                (user_id,)
            )
            u = cur.fetchone()
            reply = (
                f"Profile Info:\n"
                f"Username: {u['username']}\n"
                f"Email: {u['email']}\n"
                f"Role: {u['role']}\n"
                f"Last Login: {u['last_login']}"
            )
    elif 'add ' in user_message and ' to cart' in user_message:
        if not user_id:
            reply = "Please log in to add items to your cart."
        else:
            prod_name = user_message.split('add ')[1].split(' to cart')[0].strip()
            cur.execute("SELECT id, name, price FROM products WHERE name LIKE %s LIMIT 1",
                        (f"%{prod_name}%",))
            prod = cur.fetchone()
            if prod:
                cart = session.get('cart', {})
                pid = prod['id']
                if pid in cart:
                    cart[pid]['quantity'] += 1
                else:
                    cart[pid] = {'name': prod['name'], 'price': float(prod['price']), 'quantity': 1}
                session['cart'] = cart
                reply = f"Added **{prod['name']}** to your cart."
            else:
                reply = f"Could not find a product named '{prod_name}'."

    # ————————————————
    # 22) Remove product from cart
    # ————————————————
    elif 'remove ' in user_message and ' from cart' in user_message:
        if not user_id:
            reply = "Please log in to modify your cart."
        else:
            prod_name = user_message.split('remove ')[1].split(' from cart')[0].strip()
            cur.execute("SELECT id FROM products WHERE name LIKE %s LIMIT 1", (f"%{prod_name}%",))
            prod = cur.fetchone()
            cart = session.get('cart', {})
            if prod and prod['id'] in cart:
                del cart[prod['id']]
                session['cart'] = cart
                reply = f"Removed **{prod_name}** from your cart."
            else:
                reply = f"'{prod_name}' is not in your cart."

    # ————————————————
    # 23) Update cart quantity
    # ————————————————
    elif 'set quantity of ' in user_message and ' to ' in user_message:
        if not user_id:
            reply = "Please log in to modify your cart."
        else:
            part = user_message.split('set quantity of ')[1]
            prod_name, _, qty_str = part.partition(' to ')
            try:
                qty = int(qty_str.strip())
            except:
                reply = "Please specify a valid quantity, e.g. 'set quantity of widget to 3'."
            else:
                cur.execute("SELECT id FROM products WHERE name LIKE %s LIMIT 1", (f"%{prod_name.strip()}%",))
                prod = cur.fetchone()
                cart = session.get('cart', {})
                if prod and prod['id'] in cart:
                    if qty > 0:
                        cart[prod['id']]['quantity'] = qty
                        session['cart'] = cart
                        reply = f"Updated **{prod_name.strip()}** quantity to {qty}."
                    else:
                        del cart[prod['id']]
                        session['cart'] = cart
                        reply = f"Removed **{prod_name.strip()}** from your cart."
                else:
                    reply = f"'{prod_name.strip()}' is not in your cart."

    # ————————————————
    # 24) Clear my cart
    # ————————————————
    elif 'clear my cart' in user_message:
        session['cart'] = {}
        reply = "Your cart has been cleared."

    # ————————————————
    # 25) Checkout summary
    # ————————————————
    elif 'checkout' in user_message:
        cart = session.get('cart', {})
        if not cart:
            reply = "Your cart is empty—nothing to checkout."
        else:
            total = sum(item['price']*item['quantity'] for item in cart.values())
            reply = (
                "Your cart total is $" + f"{total:.2f}.\n"
                "To complete your purchase, visit: /checkout"
            )

    # ————————————————
    # 26) Most expensive products
    # ————————————————
    elif 'most expensive' in user_message:
        cur.execute("SELECT name, price FROM products ORDER BY price DESC LIMIT 3")
        prods = cur.fetchall()
        reply = "Top 3 most expensive products:\n" + "\n".join(
            f"{p['name']} – ${p['price']}" for p in prods
        )

    # ————————————————
    # 27) Cheapest products
    # ————————————————
    elif 'cheapest' in user_message:
        cur.execute("SELECT name, price FROM products ORDER BY price ASC LIMIT 3")
        prods = cur.fetchall()
        reply = "Top 3 cheapest products:\n" + "\n".join(
            f"{p['name']} – ${p['price']}" for p in prods
        )

    # ————————————————
    # 28) Count categories
    # ————————————————
    elif 'how many categories' in user_message:
        cur.execute("SELECT COUNT(*) AS cnt FROM category")
        cnt = cur.fetchone()['cnt']
        reply = f"We have {cnt} categories in our store."

    # ————————————————
    # 29) Count products
    # ————————————————
    elif 'how many products' in user_message:
        cur.execute("SELECT COUNT(*) AS cnt FROM products")
        cnt = cur.fetchone()['cnt']
        reply = f"We currently offer {cnt} products."

    # ————————————————
    # 30) About us / Company info
    # ————————————————
    elif 'about us' in user_message:
        reply = (
            "We are **YourBrand Dropshipping**, dedicated to delivering "
            "the best products worldwide. Founded in 2023, we prioritize "
            "quality, speed, and customer satisfaction."
        )

    # ————————————————
    # 31) Terms & Privacy
    # ————————————————
    elif 'terms' in user_message:
        reply = "Read our Terms & Conditions here: https://yourdomain.com/terms"
    elif 'privacy' in user_message:
        reply = "Read our Privacy Policy here: https://yourdomain.com/privacy"

    # ————————————————
    # 32) Working hours & contact
    # ————————————————
    elif 'hours' in user_message or 'open' in user_message:
        reply = "Our support team is available 9 AM–6 PM (Mon–Fri)."
    elif 'phone' in user_message or 'call' in user_message:
        reply = "You can reach us at 1-800-123-4567."

    # ————————————————
    # Final fallback
    # ————————————————
    else:
        reply = (
            "Sorry, I didn't understand. Type 'help' to see all commands I support."
        )
    # 3) Save bot reply
    cur.execute(
        "INSERT INTO chatbot_history (user_id, message, is_bot) VALUES (%s, %s, %s)",
        (user_id, reply, True)
    )
    db.commit()
    cur.close()

    return jsonify({'reply': reply})

@app.route('/admin/reports')
def sales_reports():
    return render_template('admin_reports.html')

@app.route('/admin/stats')
def site_stats():
    return render_template('admin_stats.html')

if __name__ == '__main__':
    app.run(debug=True)
