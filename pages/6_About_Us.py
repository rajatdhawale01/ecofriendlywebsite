import streamlit as st
import base64
from components.ecobot import render_ecobot

# ✅ Wide layout fixes the invisible left-margin issue
st.set_page_config(page_title="About Us | EcoShop", page_icon="🌿", layout="wide")

# ✅ Function to apply local background with improved readability and styling
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
            margin: 2rem auto;
        }}
        h1, h2, h3, p, span, li, div {{
            color: #222 !important;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

# ✅ Apply background image
set_local_background("assets/background_img.jpg")

# ✅ About Us content
st.title("🌿 About EcoShop")

st.markdown("""
Welcome to **EcoShop**, your one-stop store for sustainable living.  
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
Reach us at: **support@ecoshop.org**
""")


# ✅ Display EcoBot on the same page
render_ecobot()
