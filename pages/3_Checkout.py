import streamlit as st
import datetime
import base64
from utils import load_db, save_db
from components.ecobot import render_ecobot

# 🌄 Local background function
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

# Apply background
set_local_background("assets/background_img.jpg")

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
            st.success("✅ Order placed successfully!")


# ✅ Display EcoBot on the same page
render_ecobot()
