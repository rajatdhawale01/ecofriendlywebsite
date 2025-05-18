import streamlit as st
import io
import base64
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from utils import load_db
from components.ecobot import render_ecobot

# Optional background
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
            background-color: rgba(255, 255, 255, 0.9);
            padding: 2rem;
            border-radius: 10px;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

# Optionally set a background
# set_local_background("assets/background_img.jpg")

st.set_page_config(page_title="Dashboard | PlastiMart", page_icon="📊", layout="wide")
st.title("📊 Dashboard")

user = st.session_state.get("user")
if not user:
    st.warning("Please login first.")
    st.stop()

# 🔄 Refresh Button using st.rerun()
if st.button("🔄 Refresh Orders"):
    st.rerun()

db = load_db()
orders = [o for o in db["orders"] if o["user"] == user]

if not orders:
    st.info("No past orders found.")
else:
    # --- Analytics Section ---
    total_orders = len(orders)
    total_spent = 0
    total_items = 0
    product_count = {}

    for order in orders:
        for item in order["items"]:
            total_spent += item["price"] * item["quantity"]
            total_items += item["quantity"]
            product_count[item["name"]] = product_count.get(item["name"], 0) + item["quantity"]

    avg_order_value = total_spent / total_orders if total_orders else 0
    most_bought = max(product_count, key=product_count.get) if product_count else "N/A"

    st.markdown("## 📈 Your Shopping Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("🛒 Total Orders", total_orders)
    col2.metric("📦 Items Purchased", total_items)
    col3.metric("💰 Total Spent", f"₹{total_spent}")
    st.metric("📊 Avg Order Value", f"₹{avg_order_value:.2f}")
    st.metric("🏆 Most Purchased Item", most_bought)

    if product_count:
        df = pd.DataFrame({
            "Product": list(product_count.keys()),
            "Quantity": list(product_count.values())
        })
        st.bar_chart(df.set_index("Product"))

    # Debug view
    with st.expander("📦 View Raw Order Data"):
        st.json(orders)

    # --- Orders List ---
    for order in orders:
        st.subheader(f"Order #{order['id']} - {order['time']}")
        for item in order["items"]:
            st.write(f"{item['name']} - ₹{item['price']} x {item['quantity']}")
        if st.button(f"Download Invoice #{order['id']}", key=order['id']):
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            story = [
                Paragraph(f"<b>Invoice #{order['id']}</b>", styles["Title"]),
                Spacer(1, 12),
                Paragraph(f"<b>User:</b> {order['user']}", styles["Normal"]),
                Paragraph(f"<b>Date:</b> {order['time']}", styles["Normal"]),
                Spacer(1, 12)
            ]
            data_table = [['Item', 'Price', 'Qty', 'Total']]
            total = 0
            for item in order["items"]:
                line_total = item["price"] * item["quantity"]
                total += line_total
                data_table.append([item["name"], f"₹{item['price']}", item["quantity"], f"₹{line_total}"])
            data_table.append(['', '', 'Grand Total:', f"₹{total}"])
            table = Table(data_table)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
            ]))
            story.append(table)
            story.append(Spacer(1, 24))
            story.append(Paragraph("Thank you for shopping with us!", styles['Italic']))
            doc.build(story)
            buffer.seek(0)
            st.download_button("Download PDF", data=buffer, file_name=f"invoice_{order['id']}.pdf", mime="application/pdf")

# 🤖 EcoBot
render_ecobot()
