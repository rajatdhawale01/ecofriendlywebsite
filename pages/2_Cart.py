import streamlit as st
from utils import load_db, save_db

st.title("🛍️ Your Cart")

user = st.session_state.get("user")
if not user:
    st.warning("Please login first.")
else:
    db = load_db()
    cart = db["cart"].get(user, [])
    if not cart:
        st.info("Cart is empty.")
    else:
        total = 0
        for item in cart:
            line_total = item["price"] * item["quantity"]
            total += line_total
            st.write(f"{item['name']} - ₹{item['price']} x {item['quantity']} = ₹{line_total}")
        st.write(f"### Total: ₹{total}")
        if st.button("Clear Cart"):
            db["cart"][user] = []
            save_db(db)
            st.success("Cart cleared.")
