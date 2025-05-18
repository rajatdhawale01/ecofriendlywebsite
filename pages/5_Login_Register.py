import base64
from components.ecobot import render_ecobot
import streamlit as st
from utils import load_db, save_db
from PIL import Image

st.set_page_config(page_title="Login | PlastiMart", page_icon="👤", layout="wide")

# ✅ Show visual branding image at bottom of page
def show_bottom_image():
    st.markdown("<hr>", unsafe_allow_html=True)
    st.image("assets/login_visual.jpg", caption="🌿 PlastiMart - Sustainable Living Starts Here", use_container_width=True)

# ✅ Title
st.markdown("<h2 style='text-align:center;'>🌿 Welcome to PlastiMart</h2>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔑 Login", "🆕 Register"])
db = load_db()

# ✅ Login Form
with tab1:
    st.subheader("Login to your account")
    login_user = st.text_input("👤 Username", placeholder="Enter your username")
    login_pass = st.text_input("🔒 Password", type="password", placeholder="Enter password (dummy)")
    if st.button("🚪 Login"):
        if login_user in db["users"]:
            st.session_state["user"] = login_user
            st.success(f"Welcome back, {login_user}!")
        else:
            st.error("User not found. Please register.")

# ✅ Register Form
with tab2:
    st.subheader("Create a new account")
    new_user = st.text_input("👤 New Username")
    new_pass = st.text_input("🔒 Password", type="password")
    confirm_pass = st.text_input("🔒 Confirm Password", type="password")
    if st.button("📝 Register"):
        if not new_user or not new_pass:
            st.warning("All fields are required.")
        elif new_pass != confirm_pass:
            st.error("Passwords do not match.")
        elif new_user in db["users"]:
            st.error("Username already exists.")
        else:
            db["users"].append(new_user)
            save_db(db)
            st.success("Registration successful. Please login.")

# ✅ Show eco-friendly image at bottom
show_bottom_image()
