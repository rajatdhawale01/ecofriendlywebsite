import streamlit as st
import io
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from utils import load_db

st.title("📊 Dashboard")

user = st.session_state.get("user")
if not user:
    st.warning("Please login first.")
else:
    db = load_db()
    orders = [o for o in db["orders"] if o["user"] == user]
    if not orders:
        st.info("No past orders found.")
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
