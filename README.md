# 🌿 EcoShop – Eco-Friendly Shopping Web App

EcoShop is a modern and interactive web application built with **Streamlit** that enables users to explore, shop, and track orders for sustainable and eco-friendly products. It also features a built-in **AI-powered EcoBot** to assist with green product-related queries using OpenAI's GPT model.

---

## ✨ Features

- 🛒 **Eco Product Shop** – Browse curated eco-friendly items
- 🛍️ **Shopping Cart & Checkout** – Add items to cart and place orders
- 📊 **Dashboard** – View order history and download invoices
- 🤖 **EcoBot Assistant** – Chatbot that answers only sustainability-focused questions
- 👤 **User Login/Register**
- 📘 **About Us** page with mission and values
- 🌄 Beautiful, page-specific backgrounds
- 📦 Deploy-ready for Streamlit Cloud

---

## 🔐 Environment Variables

Create a `.env` file in the root directory (DO NOT commit this file):

```env
OPENAI_API_KEY=your-openai-api-key
```

---

## 🗂️ Project Structure

```
.
├── app.py                  # Main entry with welcome screen
├── utils.py                # Utility functions (e.g., load/save db)
├── requirements.txt
├── .env                    # Your secret key (excluded from git)
├── .gitignore
├── assets/                 # Backgrounds & product images
├── pages/
│   ├── 1_Shop.py
│   ├── 2_Cart.py
│   ├── 3_Checkout.py
│   ├── 4_Dashboard.py
│   ├── 5_Login_Register.py
│   ├── 6_About_Us.py
│   └── 7_EcoBot.py
└── components/
    └── ecobot.py           # Reusable chatbot logic
```

---

## 🚀 Deployment on Streamlit Cloud

1. Push your project to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click "New app" → select your repo and `app.py`
4. In **Settings → Secrets**, add:

```toml
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

5. Deploy and enjoy your live eco-store!

---

## 📦 Install & Run Locally

```bash
git clone https://github.com/your-username/ecoshop.git
cd ecoshop
pip install -r requirements.txt
streamlit run app.py
```

---

## 🙏 Credits

- Images from [Unsplash](https://unsplash.com)
- Built using [Streamlit](https://streamlit.io)
- Chat powered by [OpenAI](https://platform.openai.com)

---

## 🧠 License

MIT License © 2024
