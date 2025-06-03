"""
    Interface design using Streamlit.
    Saving text extractions from PDFs to Qdrant Vector Store.
"""
import streamlit as st
from utils.gemini_handler import generate_answer, generate_answer_from_docs
from utils.pdf_handler import process_uploaded_pdf, process_decisions_text
from utils.vektor_store import initialize_vector_store, add_to_vector_store, query_vector_store
from utils.keyword_extractor import extract_keywords
from utils.web_searcher import fetch_decision_texts

def handle_general_query(query: str):
    """
        Generates a simple response for general legal questions.
    """
    prompt = f"""
        You are a professional legal consultant. Below is a legal question from a user.
        Your goal is to provide a brief, clear response based on technical terms and formal language.
        The response should not exceed 4-5 sentences.

        Question: "{query}"

        Answer:
        """
    response = generate_answer(prompt)
    return response.candidates[0].content.parts[0].text

def handle_pdf_query(query: str, pdf_path: str):
    """
        Extracts the most relevant information from the uploaded PDF file
        and generates a response to the query.
    """
    collection_name = "research_pdf"

    st.info("Processing PDF...")
    docs = process_uploaded_pdf(pdf_path)

    client, embeddings = initialize_vector_store(collection_name)

    st.info("Saving to vector database...")
    add_to_vector_store(client, embeddings, docs, collection_name)

    st.info("Searching for the most relevant content for your query...")
    relevant_docs = query_vector_store(client, embeddings, query, collection_name)

    st.info("Generating response...")
    answer = generate_answer_from_docs(query, relevant_docs)

    return answer.candidates[0].content.parts[0].text

def handle_internet_query(query: str):
    """
        Downloads relevant court decision texts from the Supreme Court website,
        processes them, and generates a response.
    """
    collection_name = "research_pdfs"

    keywords = extract_keywords(query)
    st.success(f"Extracted Keywords: {keywords}")

    st.info("Searching for relevant decisions on Yargitay.gov.tr...")
    decisions_text = fetch_decision_texts(keywords)

    if not decisions_text:
        st.error("No relevant decisions found. Please modify your query and try again.")
    else:
        st.info("Downloading and processing decisions...")
        docs = process_decisions_text(decisions_text)
        if not docs:
            st.error("An error occurred while processing decisions.")
        else:
            st.info("Saving to vector database...")
            client, embeddings = initialize_vector_store(collection_name)
            add_to_vector_store(client, embeddings, docs, collection_name)

            st.info("Searching for the most relevant content for your query...")
            relevant_docs = query_vector_store(client, embeddings, query, collection_name)

            st.info("Generating response...")
            answer = generate_answer_from_docs(query, relevant_docs)

            return answer.candidates[0].content.parts[0].text
