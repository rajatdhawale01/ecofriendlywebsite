import streamlit as st
import base64
from utils import load_db, save_db
from PIL import Image
from components.ecobot import render_ecobot

st.set_page_config(page_title="Login | PlastiMart", page_icon="👤", layout="wide")

# ✅ HTML-based redirect to home
if st.session_state.get("user"):
    st.markdown("✅ Redirecting to home...")
    st.markdown('<meta http-equiv="refresh" content="0;url=/" />', unsafe_allow_html=True)
    st.stop()

# Optional background setup
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.95);
            padding: 3rem;
            border-radius: 15px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1, h2, h3, p, span, div, input {{
            color: #222 !important;
        }}
        </style>
        """, unsafe_allow_html=True)

# Optional: set_background("assets/login_bg.jpg")

# Page title
st.markdown("<h2 style='text-align:center;'>🌿 Welcome to PlastiMart</h2>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔑 Login", "🆕 Register"])
db = load_db()

# 🔐 Login
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

# 📝 Register
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

# Bottom image
#st.markdown("<hr>", unsafe_allow_html=True)
#st.image("assets/login_visual.jpg", caption="🌿 PlastiMart - Sustainable Living Starts Here", use_container_width=True)

# 🤖 Chatbot
render_ecobot()
