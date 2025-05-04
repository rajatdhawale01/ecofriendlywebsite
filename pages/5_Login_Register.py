import streamlit as st
from utils import load_db, save_db

st.set_page_config(page_title="Login | EcoShop", page_icon="👤", layout="centered")
st.markdown("<h2 style='text-align:center;'>🌿 Welcome to EcoShop</h2>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔑 Login", "🆕 Register"])
db = load_db()

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
