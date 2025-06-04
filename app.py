from flask import Flask, render_template_string, request, session, redirect, url_for
import os

app = Flask(__name__)
# Set a secret key for session management (important for security!)
# In a real app, generate a strong random key and store it securely
app.secret_key = os.urandom(24)

menu = {
    "Latte": 7,
    "Cappuccino": 6,
    "Espresso": 4,
}

# HTML template for the main page
# We are embedding it as a string for simplicity, but in a real app,
# you'd use separate .html files in a 'templates' directory.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>BIG MO's Coffee Shop</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; color: #333; }
        .container { max-width: 800px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1, h2 { color: #5C4033; }
        ul { list-style: none; padding: 0; }
        li { margin-bottom: 5px; }
        .menu-item { font-weight: bold; }
        form { margin-top: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; background-color: #fafafa; }
        input[type="number"], input[type="text"], select { padding: 8px; margin-right: 10px; border: 1px solid #ccc; border-radius: 4px; }
        button { background-color: #8B4513; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background-color: #6a340f; }
        .basket { margin-top: 30px; padding: 15px; border: 1px dashed #bbb; border-radius: 5px; background-color: #ffe; }
        .total { font-size: 1.2em; font-weight: bold; margin-top: 15px; }
        .message { color: green; font-weight: bold; margin-top: 10px; }
        .error { color: red; font-weight: bold; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hello and Welcome to BIG MO's Coffee Shop!</h1>
        <p>May I take your name? (This is a web app, so no direct 'name' input here yet, just choose from menu!)</p>

        <h2>Here's our menu:</h2>
        <ul>
            {% for item, price in menu.items() %}
                <li><span class="menu-item">{{ item }}</span> - £{{ price }}</li>
            {% endfor %}
        </ul>

        <form action="/add" method="post">
            <label for="item">What would you like to order?</label>
            <select id="item" name="item" required>
                {% for item in menu.keys() %}
                    <option value="{{ item }}">{{ item }}</option>
                {% endfor %}
            </select>
            <label for="quantity">How many?</label>
            <input type="number" id="quantity" name="quantity" value="1" min="1" required>
            <button type="submit">Add to Basket</button>
        </form>

        {% if message %}
            <p class="message">{{ message }}</p>
        {% endif %}
        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}

        <div class="basket">
            <h2>Your Basket:</h2>
            {% if basket %}
                <ul>
                    {% for item, quantity in basket %}
                        <li>{{ quantity }} x {{ item }}</li>
                    {% endfor %}
                </ul>
                <form action="/checkout" method="post">
                    <button type="submit">Checkout</button>
                </form>
                {% if total_cost is not none %}
                    <p class="total">Your total is £{{ "%.2f"|format(total_cost) }}. Thank you for your order!</p>
                {% endif %}
            {% else %}
                <p>Your basket is empty.</p>
            {% endif %}
        </div>

        <form action="/remove" method="post">
            <label for="remove_item">Remove item:</label>
            <select id="remove_item" name="item" required>
                {% for item, quantity in basket %}
                    <option value="{{ item }}">{{ item }}</option>
                {% endfor %}
            </select>
            <button type="submit">Remove</button>
        </form>

        <p><small>Note: Basket is session-based. It clears if your browser session ends.</small></p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    # Initialize basket in session if not present
    if 'basket' not in session:
        session['basket'] = []
    return render_template_string(HTML_TEMPLATE, menu=menu, basket=session['basket'], message=None, error=None, total_cost=None)

@app.route('/add', methods=['POST'])
def add_to_basket_web():
    item = request.form['item']
    try:
        quantity = int(request.form['quantity'])
    except ValueError:
        return render_template_string(HTML_TEMPLATE, menu=menu, basket=session.get('basket', []), error="Please enter a valid number for quantity.", message=None, total_cost=None)

    if item in menu:
        if 'basket' not in session:
            session['basket'] = []
        
        # Check if item already exists in basket, update quantity
        found = False
        new_basket = []
        for b_item, b_qty in session['basket']:
            if b_item == item:
                new_basket.append((b_item, b_qty + quantity))
                found = True
            else:
                new_basket.append((b_item, b_qty))
        if not found:
            new_basket.append((item, quantity))
        
        session['basket'] = new_basket
        session.modified = True # Important if modifying mutable objects in session

        return render_template_string(HTML_TEMPLATE, menu=menu, basket=session['basket'], message=f"Added {quantity} x {item} to your basket.", error=None, total_cost=None)
    else:
        return render_template_string(HTML_TEMPLATE, menu=menu, basket=session.get('basket', []), error="Sorry, we don't sell that here.", message=None, total_cost=None)

@app.route('/remove', methods=['POST'])
def remove_from_basket_web():
    item_to_remove = request.form['item']
    if 'basket' not in session:
        session['basket'] = []

    original_basket_len = len(session['basket'])
    # Create a new basket list excluding the item to remove
    session['basket'] = [item for item in session['basket'] if item[0] != item_to_remove]
    session.modified = True

    if len(session['basket']) < original_basket_len:
        return render_template_string(HTML_TEMPLATE, menu=menu, basket=session['basket'], message=f"Removed {item_to_remove} from your basket.", error=None, total_cost=None)
    else:
        return render_template_string(HTML_TEMPLATE, menu=menu, basket=session['basket'], error=f"{item_to_remove} is not in your basket.", message=None, total_cost=None)


@app.route('/checkout', methods=['POST'])
def checkout_web():
    if 'basket' not in session or not session['basket']:
        return render_template_string(HTML_TEMPLATE, menu=menu, basket=session.get('basket', []), error="Your basket is empty. Nothing to checkout.", message=None, total_cost=None)

    total_cost = sum(menu[item] * quantity for item, quantity in session['basket'])
    session['basket'] = [] # Clear basket after checkout
    session.modified = True
    return render_template_string(HTML_TEMPLATE, menu=menu, basket=[], message=None, error=None, total_cost=total_cost)


if __name__ == '__main__':
    # This block is for local development only.
    # Gunicorn will handle running the app in production.
    app.run(debug=True, host='0.0.0.0', port=5001) # Or any other free port like 5001, 8081, etc.
    # app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
