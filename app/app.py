from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)

# Used for the shopping cart session
app.secret_key = "devshop-secret-key"


# Sample products
products = [
    {
        "id": 1,
        "name": "Laptop Pro",
        "price": 75000,
        "description": "Powerful laptop for work, development and everyday use.",
        "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853"
    },
    {
        "id": 2,
        "name": "Smartphone X",
        "price": 45000,
        "description": "Modern smartphone with a beautiful display and powerful processor.",
        "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9"
    },
    {
        "id": 3,
        "name": "Wireless Headphones",
        "price": 5000,
        "description": "Comfortable wireless headphones with high-quality sound.",
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e"
    },
    {
        "id": 4,
        "name": "Mechanical Keyboard",
        "price": 3500,
        "description": "Mechanical keyboard designed for developers and gamers.",
        "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3"
    }
]


@app.route("/")
def home():
    return render_template("index.html", products=products)


@app.route("/products")
def product_list():
    return render_template("products.html", products=products)


@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = next(
        (product for product in products if product["id"] == product_id),
        None
    )

    if product is None:
        return "Product not found", 404

    return render_template("product.html", product=product)


@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", [])

    if product_id not in cart:
        cart.append(product_id)

    session["cart"] = cart

    return redirect(url_for("cart"))


@app.route("/remove-from-cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", [])

    if product_id in cart:
        cart.remove(product_id)

    session["cart"] = cart

    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    cart_ids = session.get("cart", [])

    cart_products = [
        product
        for product in products
        if product["id"] in cart_ids
    ]

    total = sum(product["price"] for product in cart_products)

    return render_template(
        "cart.html",
        products=cart_products,
        total=total
    )


@app.route("/health")
def health():
    return {"status": "healthy"}


@app.route("/version")
def version():
    return {
        "application": "DevShop",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
