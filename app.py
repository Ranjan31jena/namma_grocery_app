import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

# Firebase setup
if not firebase_admin._apps:
   cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

# Firebase setup using Streamlit secrets
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["firebase"])
    firebase_admin.initialize_app(cred)


# User authentication function
def user_auth():
    st.sidebar.header("User Authentication")
    choice = st.sidebar.selectbox('Login/Register', ['Login', 'Register'])

    email = st.sidebar.text_input('Email')
    password = st.sidebar.text_input('Password', type='password')

    if choice == 'Register':
        if st.sidebar.button('Register'):
            try:
                user = auth.create_user(email=email, password=password)
                st.sidebar.success('Account created successfully!')
            except Exception as e:
                st.sidebar.error('Registration failed: ' + str(e))
                
    elif choice == 'Login':
        if st.sidebar.button('Login'):
            try:
                user = auth.get_user_by_email(email)
                st.sidebar.success('Logged in as {}'.format(email))
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = email
            except Exception as e:
                st.sidebar.error('Login failed: ' + str(e))

user_auth()

# Grocery Items
grocery_items = [
    "Rice", "Wheat Flour", "Pulses", "Sugar", "Salt", "Spices", "Oils", "Dairy Products",
    "Snacks", "Sweets", "Dry Goods", "Canned Goods", "Bread", "Pastries", "Soft Drinks", "Juices", "Coffee",
    "Household Essentials", "Cleaning Supplies", "Detergents", "Paper Products", "Toiletries",
    "Dishwashing Soaps", "Dishwashing Powders", "Dishwashing Liquids", "Toilet Cleaner", "Floor Cleaner", "Kitchen Cleaner",
    "Shampoo", "Soap", "Toothpaste", "Toothbrush", "Bathing Soap", "Hair Conditioner", "Face Powder",
    "Pooja Items", "Matchbox", "Deepa Oil", "Cotton Thread", "Camphor", "Incense Sticks", "Dhoop",
    "Rock Candy", "Dry Grapes", "Medicines/Bandages", "Frozen Foods", "Packaged Foods"
]

# Store data
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

if 'logged_in' in st.session_state and st.session_state['logged_in']:
    st.title("🛒 Namma Grocery")
    store = st.selectbox("Select a Store:", list(stores.keys()))
    st.header(f"Products from {store}")
    products = stores[store]

    cart = []
    for product in products:
        col1, col2 = st.columns([3, 1])
        col1.write(f"{product['name']} - ₹{product['price']}")
        quantity = col2.number_input("Qty", min_value=0, key=f"{store}_{product['name']}")
        if quantity > 0:
            cart.append({"name": product['name'], "price": product['price'], "quantity": quantity})

    if cart:
        st.header("🛍️ Your Cart")
        total = sum(item['price'] * item['quantity'] for item in cart)
        for item in cart:
            st.write(f"{item['name']} x {item['quantity']} = ₹{item['price'] * item['quantity']}")
        st.subheader(f"Total: ₹{total}")

        st.header("🚚 Delivery Options")
        address = st.text_area("Enter Delivery Address")
        delivery_time = st.selectbox("Choose Delivery Slot", ["Morning", "Afternoon", "Evening"])
        st.write(f"Delivering to: {address}")
        st.write(f"Delivery Slot: {delivery_time}")

        st.header("💳 Payment")
        payment_method = st.radio("Choose Payment Method", ["Credit Card", "Debit Card", "UPI", "Cash on Delivery"])
        if st.button("Pay Now"):
            st.success(f"Payment of ₹{total} done successfully via {payment_method}")
