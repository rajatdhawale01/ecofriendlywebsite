import streamlit as st
import datetime
import base64
import pandas as pd
from utils import load_db, save_db
from components.ecobot import render_ecobot

# 🌄 Optional background
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
            background-color: rgba(255, 255, 255, 0.92);
            padding: 2rem;
            border-radius: 12px;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

# Apply background if needed
# set_local_background("assets/checkout_bg.jpg")

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
        # ✅ Display cart as a formatted table
        st.subheader("🛒 Items in Your Cart")
        cart_data = []
        total = 0
        for item in cart:
            line_total = item["price"] * item["quantity"]
            cart_data.append({
                "Item": item["name"],
                "Quantity": item["quantity"],
                "Price (₹)": item["price"],
                "Total (₹)": line_total
            })
            total += line_total

        df = pd.DataFrame(cart_data)
        st.table(df)
        st.markdown(f"### 🧮 Grand Total: ₹{total}")

        # 🏠 Shipping address form
        st.subheader("🏠 Shipping Address")
        name = st.text_input("Full Name")
        address = st.text_area("Address")
        city = st.text_input("City")
        pincode = st.text_input("Pincode")

        # 💳 Payment details (demo only)
        st.subheader("💳 Payment Details (Demo Only)")
        card_number = st.text_input("Card Number")
        expiry = st.text_input("Expiry Date (MM/YY)")
        cvv = st.text_input("CVV")

        # ✅ Order submission
        if st.button("Place Order"):
            if not all([name, address, city, pincode, card_number, expiry, cvv]):
                st.error("Please fill in all required fields.")
            else:
                order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_order = {
                    "id": len(db["orders"]) + 1,
                    "user": user,
                    "items": cart.copy(),
                    "time": order_time,
                    "status": "Order Placed",
                    "shipping": {
                        "name": name,
                        "address": address,
                        "city": city,
                        "pincode": pincode
                    },
                    "payment_status": "Paid"
                }
                db["orders"].append(new_order)
                db["cart"][user] = []
                save_db(db)
                st.success("✅ Order placed successfully!")

# 🤖 EcoBot assistant
render_ecobot()
