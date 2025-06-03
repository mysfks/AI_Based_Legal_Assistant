"""
    Generating responses using Google API Key. (Includes document handling)
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def generate_answer(prompt: str):
    """
        Generates a response based on the given prompt
    """
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response

def generate_answer_from_docs(query, documents) -> str:
    """
        Creates a detailed yet concise response from user query and relevant documents
        Combines page contents from the documents
    """
    context = "\n\n".join([doc.page_content for doc in documents])

    prompt = f"""
        Below you will find a legal question from the user and text excerpts obtained from documents related to this question.
        Considering the documents, create a detailed but concise response in formal and understandable language.

        Question:
        \"{query}\"

        Relevant Documents:
        \"\"\"
        {context}
        \"\"\"

        The answer should be based solely on the information in the documents and should not include any speculation.
        If a direct answer cannot be produced, an explanatory statement should be used.

        Answer:
        """
    return generate_answer(prompt)
