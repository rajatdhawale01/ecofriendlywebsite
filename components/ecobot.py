import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Load environment variable once
load_dotenv()

# Init model
model = ChatOpenAI(model="gpt-3.5-turbo")

def render_ecobot():
    with st.sidebar.expander("🤖 EcoBot - Chat Assistant", expanded=False):
        if "eco_messages" not in st.session_state:
            st.session_state.eco_messages = [
                SystemMessage("You are an expert on eco-friendly products and sustainability. Only answer questions related to green living. Politely decline others.")
            ]

        # Show chat history
        for msg in st.session_state.eco_messages[1:]:
            role = "👤 You" if isinstance(msg, HumanMessage) else "🤖 EcoBot"
            st.markdown(f"**{role}:** {msg.content}")

        # Input at bottom using form
        with st.form(key="eco_form", clear_on_submit=True):
            eco_input = st.text_input("💬 Ask about eco-products:")
            submitted = st.form_submit_button("Send")
            if submitted and eco_input:
                st.session_state.eco_messages.append(HumanMessage(eco_input))
                response = model(st.session_state.eco_messages)
                st.session_state.eco_messages.append(SystemMessage(response.content))
