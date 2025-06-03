"""
    Operations for retrieving requested information from "karararama.yargitay.gov.tr" website.
"""
import requests
from bs4 import BeautifulSoup

session = requests.Session()

# Custom HTTP headers for the Supreme Court decision search website
headers = {
    "Host": "karararama.yargitay.gov.tr",
    "Content-Type": "application/json; charset=UTF-8",
    "Origin": "https://karararama.yargitay.gov.tr",
    "Referer": "https://karararama.yargitay.gov.tr/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

def perform_search(query, page=1, page_size=10):
    """
        Sends a query to the Supreme Court decision search API and returns results as JSON.
    """
    url = "https://karararama.yargitay.gov.tr/aramalist"
    payload = {
        "data": {
            "aranan": query,
            "arananKelime": query,
            "pageSize": page_size,
            "pageNumber": page
        }
    }
    response = session.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_decision_by_id(doc_id):
    """
        Retrieves decision details for the specified decision ID as JSON.
    """
    url = f"https://karararama.yargitay.gov.tr/getDokuman?id={doc_id}"
    response = session.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def extract_text_from_html(html_str):
    """
        Extracts only the text content from HTML.
    """
    soup = BeautifulSoup(html_str, "html.parser")
    body = soup.find("body")
    return body.get_text(separator="\n", strip=True) if body else ""

def fetch_decision_texts(keywords, limit=7):
    """
        Searches for Supreme Court decisions using keywords, retrieves decision texts,
        and returns them concatenated.
    """
    all_results = ""

    try:
        search_results = perform_search(keywords, page=1, page_size=limit)
        decisions = search_results.get("data", {}).get("data", [])[:limit]

        all_results += f"\n### Search: '{keywords}'\n"

        for decision in decisions:
            decision_id = decision.get("id")
            print(f"Processing: Decision ID {decision_id}")
            if not decision_id:
                continue

            decision_json = fetch_decision_by_id(decision_id)
            html_content = decision_json.get("data", "")
            text = extract_text_from_html(html_content)

            all_results += f"\n--- Decision ID: {decision_id} ---\n{text}\n"

        all_results += "\n" + "=" * 80 + "\n"

    except Exception as e:
        print(f"⚠️ Error occurred: {e}")
        all_results += f"\n[ERROR: Problem encountered while searching for '{keywords}']\n"

    return all_results
