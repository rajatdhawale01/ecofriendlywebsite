import streamlit as st
import pandas as pd
from utils import load_db, save_db
from components.ecobot import render_ecobot

st.set_page_config(page_title="Cart | EcoShop", page_icon="🛒", layout="wide")
st.title("🛍️ Your Cart")

user = st.session_state.get("user")
if not user:
    st.warning("Please login first.")
else:
    db = load_db()
    cart = db["cart"].get(user, [])
    if not cart:
        st.info("Your cart is currently empty.")
    else:
        # 🧾 Format cart table
        cart_data = []
        total = 0
        for i, item in enumerate(cart, start=1):
            line_total = item["price"] * item["quantity"]
            cart_data.append([i, item["name"], item["quantity"], item["price"], line_total])
            total += line_total

        df = pd.DataFrame(cart_data, columns=["No.", "Item", "Quantity", "Price", "Total"])
        st.subheader("🧾 Cart Summary")
        st.table(df)
        st.markdown(f"### 🧮 Grand Total: {total}")

        # Clear Cart Option
        if st.button("🗑️ Clear Cart"):
            db["cart"][user] = []
            save_db(db)
            st.success("Cart has been cleared.")

# 🤖 Chat Assistant
render_ecobot()
