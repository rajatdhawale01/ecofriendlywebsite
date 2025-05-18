import streamlit as st
import datetime
import base64
import pandas as pd
from utils import load_db, save_db
from components.ecobot import render_ecobot

# Optional background styling
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

# Optional usage
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
        # 🧾 Properly formatted table without DataFrame index
        st.subheader("🛒 Items in Your Cart")
        cart_data = []
        total = 0
        for i, item in enumerate(cart, start=1):
            line_total = item["price"] * item["quantity"]
            cart_data.append([i, item["name"], item["quantity"], item["price"], line_total])
            total += line_total

        cart_df = pd.DataFrame(cart_data, columns=["No.", "Item", "Quantity", "Price", "Total"])
        st.table(cart_df)  # shows without index
        st.markdown(f"### 🧮 Grand Total: {total}")

        # 🏠 Address form
        st.subheader("🏠 Shipping Address")
        name = st.text_input("Full Name").strip()
        address = st.text_area("Address").strip()
        city = st.text_input("City").strip()
        pincode = st.text_input("Pincode").strip()

        # 💳 Payment (Demo)
        st.subheader("💳 Payment Details (Demo Only)")
        card_number = st.text_input("Card Number").strip()
        expiry = st.text_input("Expiry Date (MM/YY)").strip()
        cvv = st.text_input("CVV").strip()

        # ✅ Validate and process order
        if st.button("Place Order"):
            required_fields = [name, address, city, pincode, card_number, expiry, cvv]
            if all(field != "" for field in required_fields):
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
            else:
                st.error("Please fill in all required fields.")

# 🤖 Chatbot remains active
render_ecobot()
