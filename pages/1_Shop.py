import streamlit as st
from utils import load_db, save_db

st.title("🛒 Shop")

products = [
    {"name": "Bamboo Toothbrush", "price": 50},
    {"name": "Reusable Bag", "price": 120},
    {"name": "Organic Soap", "price": 80}
]

user = st.session_state.get("user")
if not user:
    st.warning("Please login first.")
else:
    db = load_db()
    cart = db["cart"].get(user, [])
    for product in products:
        if st.button(f"Add {product['name']} - ₹{product['price']}"):
            found = False
            for item in cart:
                if item["name"] == product["name"]:
                    item["quantity"] += 1
                    found = True
                    break
            if not found:
                cart.append({**product, "quantity": 1})
            db["cart"][user] = cart
            save_db(db)
            st.success(f"Added {product['name']} to cart.")
