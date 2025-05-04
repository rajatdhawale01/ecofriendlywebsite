import streamlit as st

st.set_page_config(page_title="Welcome to EcoShop", page_icon="🌿", layout="wide")

# Custom HTML + CSS
st.markdown(
    """
    <style>
    .main {
        background-image: url('https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-position: center;
        height: 100vh;
        padding: 2rem;
        color: white;
    }
    .title-container {
        background-color: rgba(0, 100, 0, 0.6);
        padding: 2rem;
        border-radius: 10px;
        max-width: 700px;
        margin: auto;
        margin-top: 100px;
    }
    h1, h2, p {
        color: white;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>

    <div class="main">
        <div class="title-container">
            <h1>🌿 Welcome to Eco-Friendly Product Store</h1>
            <h2>Buy Green, Live Clean</h2>
            <p>Join us in our mission to make the planet cleaner, healthier, and more sustainable — one eco-friendly product at a time.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
