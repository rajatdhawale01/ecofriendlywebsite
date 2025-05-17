import streamlit as st
import base64
from utils import load_db, save_db
from components.ecobot import render_ecobot

# 🔄 Optional: Set a local background image
def set_local_background(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.9);
            padding: 2rem;
            border-radius: 10px;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

# 🌄 Use your local image
#set_local_background("assets/background_img.jpg")

# 🛒 Cart display
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


# ✅ Display EcoBot on the same page
render_ecobot()
