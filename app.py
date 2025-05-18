import streamlit as st
import base64
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# ✅ Set page config
st.set_page_config(page_title="PlastiMart", page_icon="🛒", layout="wide")

# ✅ Improved contrast for overlay + text
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
            background-color: rgba(255, 255, 255, 0.85); /* lighter overlay */
            padding: 4rem;
            border-radius: 15px;
        }}
        h1, h2, h3, p, span, div {{
            color: #333 !important; /* slightly lighter than black */
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

# ✅ Apply welcome background
#set_local_background("assets/home_page.jpg")

# ✅ Welcome header
st.markdown("<h1 style='text-align:center;'>🌿 Welcome to PlastiMart</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>Your One-Stop Store for Sustainable Living</h3>", unsafe_allow_html=True)

st.write("---")
st.markdown("""
PlastiMart is dedicated to helping you make eco-conscious choices without compromising on quality or convenience.

Explore our selection of natural, reusable, and sustainable products that help you reduce waste and support a cleaner planet.

---

🛍️ **Shop smarter. Live greener. Join the Eco movement today!**

Use the sidebar to navigate through the app:
- 🛒 Shop
- 🛍️ Cart
- 📦 Checkout
- 📊 Dashboard
- 👤 Login/Register
- 📘 About Us
- 🤖 EcoBot (Chat Assistant)
""")

# ✅ Load OpenAI API Key and model
model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Sidebar: EcoBot Chat Assistant
with st.sidebar.expander("🤖 EcoBot - Chat with our Assistant", expanded=False):
    if "eco_messages" not in st.session_state:
        st.session_state.eco_messages = [
            SystemMessage("You are an expert on eco-friendly products and sustainability. Only answer questions related to green living. Politely decline others.")
        ]

    # 🗨️ Show chat history
    for msg in st.session_state.eco_messages[1:]:
        role = "👤 You" if isinstance(msg, HumanMessage) else "🤖 EcoBot"
        st.markdown(f"**{role}:** {msg.content}")

    # ✍️ Input at bottom
    with st.form(key="eco_form", clear_on_submit=True):
        eco_input = st.text_input("💬 Ask about eco-products:")
        submitted = st.form_submit_button("Send")
        if submitted and eco_input:
            st.session_state.eco_messages.append(HumanMessage(eco_input))
            response = model(st.session_state.eco_messages)
            st.session_state.eco_messages.append(SystemMessage(response.content))
