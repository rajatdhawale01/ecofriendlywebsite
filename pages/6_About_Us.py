import streamlit as st
import base64
from components.ecobot import render_ecobot

# ✅ Wide layout + visible sidebar
st.set_page_config(page_title="About Us | PlastiMart", page_icon="🌿", layout="wide")

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
            background-color: rgba(255, 255, 255, 0.95);
            padding: 3rem;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .sidebar .block-container {{
            background-color: rgba(255, 255, 255, 0.85);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1, h2, h3, p, span, li, div {{
            color: #222 !important;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

# ✅ Apply background
#set_local_background("assets/background_img.jpg")

# ✅ Content
st.title("🌿 About PlastiMart")

st.markdown("""
Welcome to **PlastiMart**, your one-stop store for sustainable living.  
We are on a mission to make the planet cleaner, greener, and healthier — one eco-friendly product at a time.

---

### 💡 Our Mission

To empower conscious consumers to choose eco-friendly alternatives that reduce waste and support the planet.

---

### 🌍 Our Values

- ♻️ Sustainability First  
- 🧼 Natural, Chemical-Free Products  
- 🧑‍🤝‍🧑 Ethical Sourcing  
- 🌱 Reusability & Zero-Waste Lifestyle

---

### 👥 Meet the Team

We’re a team of engineers, designers, and environmentalists passionate about combining technology with sustainability to build a better tomorrow.

---

### 📬 Contact Us

Have questions or feedback?  
Reach us at: **support@PlastiMart.org**
""")

# ✅ Display EcoBot on the same page
render_ecobot()

