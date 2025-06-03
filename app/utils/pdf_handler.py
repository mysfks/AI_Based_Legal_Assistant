"""
    Text extraction operations from PDFs.
"""
from typing import List
import fitz
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_path, max_pages: int = 200):
    """
        Extracts text from a PDF by reading the first N pages.
    """
    try:
        pdf_doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"PDF reading error ({pdf_path}): {e}")
        return ""

    full_text = ""
    for i, page in enumerate(pdf_doc):
        if i >= max_pages:
            break
        full_text += page.get_text()

    return full_text

def process_uploaded_pdf(pdf_path) -> list[Document]:
    """
        Extracts text from uploaded PDF file, splits the text into chunks,
        and returns as a list of LangChain Document objects.
    """
    full_text = extract_text_from_pdf(pdf_path)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(full_text)

    documents = []
    for i, chunk in enumerate(chunks):
        doc = Document(
            page_content=chunk,
            metadata={
                "chunk": i,
                "document": pdf_path.split("/")[-1]
            }
        )
        documents.append(doc)

    return documents

def process_decisions_text(decisions_text: str, source_name: str = "court_decision") -> list[Document]:
    """
        Splits long texts like court decisions into chunks and returns
        a list of Document objects.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(decisions_text)

    documents = []
    for i, chunk in enumerate(chunks):
        doc = Document(
            page_content=chunk,
            metadata={
                "chunk": i,
                "source": source_name
            }
        )
        documents.append(doc)

    return documents
