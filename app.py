import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.title("E2E Pac Tech - Paper Bag Quotation")

# Inputs
client = st.text_input("Client Name")
bag_type = st.selectbox("Bag Type", ["Flat Handle", "Twisted Handle", "D Cut", "Luxury"])

gsm = st.number_input("GSM")
size = st.number_input("Size")
qty = st.number_input("Quantity")
rate = st.number_input("Rate")
margin = st.number_input("Margin %")
gst = st.number_input("GST %")

if st.button("Calculate"):
    base = (gsm * size * rate) / 1000
    margin_val = base * (margin / 100)
    selling = base + margin_val
    gst_val = selling * (gst / 100)
    final = selling + gst_val
    total = final * qty

    st.success(f"Final/Bag: ₹{final:.2f}")
    st.success(f"Total: ₹{total:.2f}")

    st.session_state.data = {
        "client": client,
        "bag_type": bag_type,
        "qty": qty,
        "final": final,
        "total": total
    }

# PDF generation
if st.button("Download PDF"):
    data = st.session_state.get("data")

    if data:
        file_name = f"{data['client']}_quotation.pdf"
        c = canvas.Canvas(file_name, pagesize=letter)

        c.drawString(50, 750, "E2E Pac Tech - Quotation")
        c.drawString(50, 720, f"Client: {data['client']}")
        c.drawString(50, 700, f"Bag Type: {data['bag_type']}")
        c.drawString(50, 680, f"Quantity: {data['qty']}")
        c.drawString(50, 660, f"Final/Bag: ₹{data['final']:.2f}")
        c.drawString(50, 640, f"Total: ₹{data['total']:.2f}")

        c.save()

        with open(file_name, "rb") as f:
            st.download_button("Download Now", f, file_name=file_name)

    else:
        st.error("Please calculate first")
