import streamlit as st
import datetime
from utils import load_db, save_db

st.title("📦 Checkout")

user = st.session_state.get("user")
if not user:
    st.warning("Please login first.")
else:
    db = load_db()
    cart = db["cart"].get(user, [])
    if not cart:
        st.warning("Your cart is empty.")
    else:
        total = sum(item["price"] * item["quantity"] for item in cart)
        st.write(f"### Order Total: ₹{total}")
        if st.button("Place Order"):
            order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_order = {
                "id": len(db["orders"]) + 1,
                "user": user,
                "items": cart.copy(),
                "time": order_time,
                "status": "Order Placed"
            }
            db["orders"].append(new_order)
            db["cart"][user] = []
            save_db(db)
            st.success("Order placed successfully.")
