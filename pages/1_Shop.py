import streamlit as st
from PIL import Image
from utils import load_db, save_db
from components.ecobot import render_ecobot

st.set_page_config(page_title="Shop | Eco-Friendly Store", page_icon="🛒", layout="wide")
st.title("🛍️ Explore Our Eco-Friendly Products")

user = st.session_state.get("user")
if not user:
    st.warning("Please log in to add items to your cart.")
else:
    db = load_db()
    cart = db["cart"].get(user, [])

    products = [
        {"name": "Bamboo Toothbrush", "price": 50, "img": "assets/toothbrush.jpg"},
        {"name": "Reusable Bag", "price": 120, "img": "assets/bag.jpg"},
        {"name": "Organic Soap", "price": 80, "img": "assets/soap.jpg"},
        {"name": "Eco Water Bottle", "price": 250, "img": "assets/bottle.jpg"},
        {"name": "Compost Bin", "price": 500, "img": "assets/compost.jpg"},
        {"name": "Beeswax Wrap", "price": 150, "img": "assets/Beeswax.jpg"}
    ]

    for row in range(0, len(products), 3):
        cols = st.columns(3)
        for idx in range(3):
            if row + idx < len(products):
                product = products[row + idx]
                with cols[idx]:
                    try:
                        img = Image.open(product["img"]).resize((300, 200))
                        st.image(img, use_container_width=False)
                    except Exception as e:
                        st.error(f"Image not found: {product['img']}")
                    st.markdown(f"### {product['name']}")
                    st.write(f"💰 Price: ₹{product['price']}")
                    if st.button(f"🛒 Add to Cart", key=f"{product['name']}_{row}_{idx}"):
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

# ✅ Display EcoBot on the same page
render_ecobot()
