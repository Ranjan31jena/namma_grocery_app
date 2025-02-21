import streamlit as st

# Initialize user database
if 'users' not in st.session_state:
    st.session_state['users'] = {}

# User login/register functionality
def user_auth():
    st.sidebar.header("User Authentication")
    auth_option = st.sidebar.radio("Choose an option", ["Login", "Register"])

    if auth_option == "Register":
        user = st.sidebar.text_input("New Username")
        pwd = st.sidebar.text_input("New Password", type='password')
        if st.sidebar.button("Register"):
            if user in st.session_state['users']:
                st.sidebar.warning("Username already exists!")
            else:
                st.session_state['users'][user] = pwd
                st.sidebar.success("Registered successfully!")

    elif auth_option == "Login":
        user = st.sidebar.text_input("Username")
        pwd = st.sidebar.text_input("Password", type='password')
        if st.sidebar.button("Login"):
            if user in st.session_state['users'] and st.session_state['users'][user] == pwd:
                st.sidebar.success(f"Logged in as {user}")
                st.session_state['logged_in'] = True
            else:
                st.sidebar.error("Invalid username/password")

# Payment method options
def payment_section(total):
    st.header("💳 Payment")
    payment_method = st.radio("Choose Payment Method", ["Credit Card", "Debit Card", "UPI", "Cash on Delivery"])
    if st.button("Pay Now"):
        st.success(f"Payment of ₹{total} done successfully via {payment_method}")

# Delivery options
def delivery_options():
    st.header("🚚 Delivery Options")
    address = st.text_area("Enter Delivery Address")
    delivery_time = st.selectbox("Choose Delivery Slot", ["Morning", "Afternoon", "Evening"])
    st.write(f"Delivering to: {address}")
    st.write(f"Delivery Slot: {delivery_time}")

# List of grocery items
grocery_items = [
    "Rice", "Wheat Flour", "Pulses", "Sugar", "Salt", "Spices", "Oils", "Dairy Products",
    "Snacks", "Sweets", "Dry Goods", "Canned Goods", "Bread", "Pastries", "Soft Drinks", "Juices", "Coffee",
    "Household Essentials", "Cleaning Supplies", "Detergents", "Paper Products", "Toiletries",
    "Dishwashing Soaps", "Dishwashing Powders", "Dishwashing Liquids", "Toilet Cleaner", "Floor Cleaner", "Kitchen Cleaner",
    "Shampoo", "Soap", "Toothpaste", "Toothbrush", "Bathing Soap", "Hair Conditioner", "Face Powder",
    "Pooja Items", "Matchbox", "Deepa Oil", "Cotton Thread", "Camphor", "Incense Sticks", "Dhoop",
    "Rock Candy", "Dry Grapes", "Medicines/Bandages", "Frozen Foods", "Packaged Foods"
]

# Store data with prices
stores = {
    "Shree Matha Food Bazaar": [{"name": item, "price": 20 + i*2} for i, item in enumerate(grocery_items)],
    "Krishna Supermarket": [{"name": item, "price": 22 + i*2} for i, item in enumerate(grocery_items)],
    "MTL Mart": [{"name": item, "price": 18 + i*2} for i, item in enumerate(grocery_items)],
    "Palrecha General Stores": [{"name": item, "price": 21 + i*2} for i, item in enumerate(grocery_items)],
    "S Nagaraj Setty Kirani Stores": [{"name": item, "price": 19 + i*2} for i, item in enumerate(grocery_items)],
    "Prabhu Kirani": [{"name": item, "price": 23 + i*2} for i, item in enumerate(grocery_items)],
    "Darshan Provisional Store": [{"name": item, "price": 17 + i*2} for i, item in enumerate(grocery_items)],
    "Kavali Entrepreneurs": [{"name": item, "price": 24 + i*2} for i, item in enumerate(grocery_items)],
    "Rajasthan Stores": [{"name": item, "price": 20 + i*2} for i, item in enumerate(grocery_items)]
}

# User authentication
user_auth()

if 'logged_in' in st.session_state and st.session_state['logged_in']:
    st.title("🛒 Namma Grocery")

    # Store selection
    store = st.selectbox("Select a Store:", list(stores.keys()))

    # Display products
    st.header(f"Products from {store}")
    products = stores[store]

    cart = []
    for product in products:
        col1, col2 = st.columns([3, 1])
        col1.write(f"{product['name']} - ₹{product['price']}")
        quantity = col2.number_input("Qty", min_value=0, key=f"{store}_{product['name']}")
        if quantity > 0:
            cart.append({"name": product['name'], "price": product['price'], "quantity": quantity})

    # Display cart
    if cart:
        st.header("🛍️ Your Cart")
        total = 0
        for item in cart:
            st.write(f"{item['name']} x {item['quantity']} = ₹{item['price'] * item['quantity']}")
            total += item['price'] * item['quantity']
        st.subheader(f"Total: ₹{total}")

        # Delivery options
        delivery_options()

        # Payment section
        payment_section(total)
