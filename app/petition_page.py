"""
    Petition interface and information collection using Streamlit
"""
import streamlit as st
from utils.gemini_handler import generate_answer

def show_petition_page(go_home_callback):
    """
        Displays the petition preparation page and organizes required information
    """
    st.header("📝 Petition Preparation Assistant")

    full_name = st.text_input("Full Name *")
    address = st.text_area("Address")
    court_name = st.text_input("Court Name * (e.g. Istanbul Anatolian 5th Family Court)")
    case_type = st.selectbox("Case Type *", ["Select", "Divorce", "Execution", "Labor Case", "Consumer", "Other"])
    opponent_name = st.text_input("Defendant/Plaintiff Name *")
    petition_details = st.text_area("Case Summary / Justification *")

    # List of fields to check for required information
    required_fields = {
        "Full Name": full_name,
        "Court Name": court_name,
        "Case Type": case_type if case_type != "Select" else "",
        "Opposing Party": opponent_name,
        "Case Summary": petition_details
    }

    if st.button("📄 Generate Petition"):
        missing_fields = [label for label, value in required_fields.items() if not value.strip()]
        if missing_fields:
            st.error(f"Please fill in the following required fields: {', '.join(missing_fields)}")
            return

        prompt = f"""
            You are a legal assistant. Using the information below, prepare an official and proper petition.
            The text should be written in clear and understandable Turkish. Include introduction, 
            case explanation and conclusion (request) sections.

            Information:
            - Full Name: {full_name}
            - Address: {address}
            - Court: {court_name}
            - Case Type: {case_type}
            - Opposing Party: {opponent_name}
            - Case Summary / Justification: {petition_details}

            Use an official and valid petition structure. End with "I respectfully submit this petition."
            """
        response = generate_answer(prompt)
        st.write(response.candidates[0].content.parts[0].text)

    st.button("🔙 Return to Home", on_click=go_home_callback)
