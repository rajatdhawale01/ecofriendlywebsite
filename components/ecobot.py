import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# ✅ Securely load API key
model = ChatOpenAI(
    model="gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# ✅ Render EcoBot chat inside sidebar
def render_ecobot():
    with st.sidebar.expander("🤖 EcoBot - Chat Assistant", expanded=False):
        if "eco_messages" not in st.session_state:
            st.session_state.eco_messages = [
                SystemMessage("You are an expert on eco-friendly products and sustainability. Only answer questions related to green living. Politely decline others.")
            ]

        # Display chat history
        for msg in st.session_state.eco_messages[1:]:
            role = "👤 You" if isinstance(msg, HumanMessage) else "🤖 EcoBot"
            st.markdown(f"**{role}:** {msg.content}")

        # Prompt at the bottom
        with st.form(key="eco_form", clear_on_submit=True):
            eco_input = st.text_input("💬 Ask about eco-products:")
            submitted = st.form_submit_button("Send")
            if submitted and eco_input:
                st.session_state.eco_messages.append(HumanMessage(eco_input))
                response = model(st.session_state.eco_messages)
                st.session_state.eco_messages.append(SystemMessage(response.content))
