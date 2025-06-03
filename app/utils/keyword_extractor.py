"""
    Extracts keywords from the entered question.
    Returns these keywords using the generate_answer() function.
"""
from utils.gemini_handler import generate_answer

def extract_keywords(question, max_keywords=5):
    """
        Extracts the specified number of keywords from the given legal question.
    """
    prompt = f"""Extract the most relevant {max_keywords} keywords from the following legal question.
        Write the keywords separated by single spaces.

        Example Output: unlicensed accident motorcycle  

        Question: {question}

        Keywords:"""

    response = generate_answer(prompt)
    return response.candidates[0].content.parts[0].text
