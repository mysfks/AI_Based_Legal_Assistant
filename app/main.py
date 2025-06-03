"""
    Main page design and presentation of options
"""
import streamlit as st
from research_page import show_research_page
from petition_page import show_petition_page

st.set_page_config(page_title="⚖️ Legal Assistant", layout="wide")

# Set page state to 'home' if not already defined
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_home():
    """
        Function to return to home page
    """
    st.session_state.page = "home"

def go_to_research():
    """
    Function to navigate to legal research page
    """
    st.session_state.page = "research"

def go_to_petition():
    """
        Function to navigate to petition creation page
    """
    st.session_state.page = "petition"

if st.session_state.page == "home":
    st.title("⚖️ AI-Powered Legal Assistant")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔍 Legal Research Assistant")
        st.write("""
        Use this section to research legal sources, precedents and laws.
        """)
        st.button("Start Research", on_click=go_to_research)

    with col2:
        st.subheader("📝 Petition Preparation Assistant")
        st.write("""
        Use this section to automatically generate petitions tailored to your needs.
        """)
        st.button("Start Preparing Petition", on_click=go_to_petition)

elif st.session_state.page == "research":
    show_research_page(go_home)

elif st.session_state.page == "petition":
    show_petition_page(go_home)
