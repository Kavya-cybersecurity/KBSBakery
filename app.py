from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "kbs_bakery_secret_key"

cart = []

def get_db():
    conn = sqlite3.connect("kbs_bakery.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS products")

    cur.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            stock INTEGER,
            image TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            address TEXT,
            phone TEXT,
            total REAL,
            payment_method TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            item_name TEXT,
            price REAL,
            weight REAL,
            quantity INTEGER,
            subtotal REAL
        )
    """)

    products = [
        ("Chocolate Cake", 500, 5, "chocolate_cake.jpg"),
        ("Vanilla Cake", 400, 3, "vanilla_cake.jpg"),
        ("Strawberry Cake", 450, 4, "strawberry_cake.jpg"),
        ("Black Forest Cake", 600, 2, "black_forest.jpg"),
        ("Gulab Jamun", 300, 10, "gulab_jamun.jpg"),
        ("Rasgulla", 280, 8, "rasgulla.jpg"),
        ("Kaju Katli", 700, 0, "kaju_katli.jpg"),
        ("Ladoo", 350, 6, "ladoo.jpg"),
        ("Barfi", 450, 0, "barfi.jpg")
    ]

    cur.executemany(
        "INSERT INTO products (name, price, stock, image) VALUES (?, ?, ?, ?)",
        products
    )

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect("/cakes")
        else:
            return "Invalid login. <br><a href='/login'>Try Again</a>"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    cart.clear()
    return redirect("/")

@app.route("/cakes")
def cakes_page():
    if "user" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    items = cur.fetchall()
    conn.close()

    return render_template("cakes.html", items=items)

@app.route("/add", methods=["POST"])
def add_to_cart():
    if "user" not in session:
        return redirect("/login")

    item_id = int(request.form["item_id"])
    item_name = request.form["item_name"]
    price = float(request.form["price"])
    weight = float(request.form["weight"])
    quantity = int(request.form["quantity"])

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT stock FROM products WHERE id = ?", (item_id,))
    product = cur.fetchone()
    conn.close()

    if product["stock"] <= 0:
        return "Product unavailable now. <br><a href='/cakes'>Back to Menu</a>"

    if quantity > product["stock"]:
        return "Not enough stock available. <br><a href='/cakes'>Back to Menu</a>"

    subtotal = price * weight * quantity

    cart.append({
        "id": item_id,
        "name": item_name,
        "price": price,
        "weight": weight,
        "quantity": quantity,
        "subtotal": subtotal
    })

    return redirect("/cart")

@app.route("/cart")
def view_cart():
    if "user" not in session:
        return redirect("/login")

    total = sum(item["subtotal"] for item in cart)
    return render_template("cart.html", cart=cart, total=total)

@app.route("/remove/<int:index>")
def remove_from_cart(index):
    if 0 <= index < len(cart):
        cart.pop(index)

    return redirect("/cart")

@app.route("/update/<int:index>", methods=["POST"])
def update_cart(index):
    if 0 <= index < len(cart):
        weight = float(request.form["weight"])
        quantity = int(request.form["quantity"])

        item = cart[index]
        item["weight"] = weight
        item["quantity"] = quantity
        item["subtotal"] = item["price"] * weight * quantity

    return redirect("/cart")

@app.route("/checkout")
def checkout():
    if "user" not in session:
        return redirect("/login")

    total = sum(item["subtotal"] for item in cart)
    return render_template("checkout.html", cart=cart, total=total)

@app.route("/payment", methods=["POST"])
def payment():
    customer_name = request.form["customer_name"]
    address = request.form["address"]
    phone = request.form["phone"]

    session["customer_name"] = customer_name
    session["address"] = address
    session["phone"] = phone

    total = sum(item["subtotal"] for item in cart)
    return render_template("payment.html", total=total)

@app.route("/place_order", methods=["POST"])
def place_order():
    payment_method = request.form["payment_method"]

    customer_name = session.get("customer_name")
    address = session.get("address")
    phone = session.get("phone")

    total = sum(item["subtotal"] for item in cart)

    conn = get_db()
    cur = conn.cursor()

    for item in cart:
        cur.execute("SELECT stock FROM products WHERE id = ?", (item["id"],))
        product = cur.fetchone()

        if product["stock"] < item["quantity"]:
            conn.close()
            return f"{item['name']} is not available in requested quantity. <br><a href='/cart'>Back to Cart</a>"

    cur.execute(
        "INSERT INTO orders (customer_name, address, phone, total, payment_method) VALUES (?, ?, ?, ?, ?)",
        (customer_name, address, phone, total, payment_method)
    )

    order_id = cur.lastrowid

    for item in cart:
        cur.execute("""
            INSERT INTO order_items
            (order_id, item_name, price, weight, quantity, subtotal)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            order_id,
            item["name"],
            item["price"],
            item["weight"],
            item["quantity"],
            item["subtotal"]
        ))

        cur.execute(
            "UPDATE products SET stock = stock - ? WHERE id = ?",
            (item["quantity"], item["id"])
        )

    conn.commit()
    conn.close()

    cart.clear()

    session.pop("customer_name", None)
    session.pop("address", None)
    session.pop("phone", None)

    return render_template("success.html", payment_method=payment_method)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)