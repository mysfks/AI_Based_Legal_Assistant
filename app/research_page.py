"""
    Online PDF and information search using Google API Key.
    Interface design with Streamlit.
"""
import os
from datetime import datetime
import streamlit as st
from utils.query_handler import handle_general_query, handle_pdf_query, handle_internet_query

def load_css():
    """
        Loads the application's custom CSS style
    """
    with open("app/assets/style.css", encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def show_research_page(go_home_callback):
    """
        General research interface and web search operations according to desired style.
    """
    load_css()

    st.title("🔍 Legal Research Assistant")

    if "pdf_mode" not in st.session_state:
        st.session_state.pdf_mode = False
    if "internet_mode" not in st.session_state:
        st.session_state.internet_mode = False
    if "uploaded_pdf_name" not in st.session_state:
        st.session_state.uploaded_pdf_name = None

    def toggle_pdf():
        st.session_state.pdf_mode = True
        st.session_state.internet_mode = False

    def toggle_internet():
        st.session_state.internet_mode = True
        st.session_state.pdf_mode = False

    def toggle_general():
        st.session_state.internet_mode = False
        st.session_state.pdf_mode = False

    if st.session_state.pdf_mode:
        placeholder = "📄 Enter your question about the PDF..."
    elif st.session_state.internet_mode:
        placeholder = "🌐 Enter your legal question to search online..."
    else:
        placeholder = "💬 Your general legal question..."

    user_input = st.text_input("✏️", placeholder=placeholder, key="user_input")

    # Column layout for buttons
    col1, col4, col2, col3 = st.columns([1, 2, 2, 2])

    with col1:
        send_disabled = not user_input.strip()
        send_clicked = st.button("⬆️ Send", disabled=send_disabled)

    with col2:
        if st.session_state.internet_mode:
            st.markdown('<button class="custom-button active">🌐 Web Search</button>', unsafe_allow_html=True)
        else:
            if st.button("🌐 Web Search", key="web_btn"):
                toggle_internet()

    with col3:
        if st.session_state.pdf_mode:
            st.markdown('<button class="custom-button active">📄 PDF Search</button>', unsafe_allow_html=True)
        else:
            if st.button("📄 PDF Search", key="pdf_btn"):
                toggle_pdf()

    with col4:
        if not st.session_state.pdf_mode and not st.session_state.internet_mode:
            st.markdown('<button class="custom-button active">💬 General Query</button>', unsafe_allow_html=True)
        else:
            if st.button("💬 General Query", key="general_btn"):
                toggle_general()

    # PDF Upload Section
    if st.session_state.pdf_mode:
        uploaded_file = st.file_uploader("📤 Upload PDF File", type=["pdf"], key="pdf_uploader")
        if uploaded_file is not None:
            upload_dir = "uploaded_pdfs"
            os.makedirs(upload_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            pdf_path = os.path.join(upload_dir, f"{timestamp}_{uploaded_file.name}")
            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.session_state.uploaded_pdf_name = pdf_path
            st.success(f"✅ {uploaded_file.name} uploaded successfully.")

    elif st.session_state.uploaded_pdf_name:
        st.markdown(f"📎 Uploaded: **{st.session_state.uploaded_pdf_name}**")

    st.markdown("---")
    st.button("🔙 Return to Home", on_click=go_home_callback)

    if send_clicked:
        query = user_input.strip()

        if st.session_state.pdf_mode:
            st.info("📄 Searching in PDF...")
            pdf_path = st.session_state.uploaded_pdf_name
            answer = handle_pdf_query(query, pdf_path)
            st.write(answer)

        elif st.session_state.internet_mode:
            st.info("🌐 Searching online...")
            answer = handle_internet_query(query)
            st.write(answer)

        else:
            st.info("💬 Processing general question...")
            answer = handle_general_query(query)
            st.write(answer)