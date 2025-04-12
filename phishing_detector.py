import re
import requests
from bs4 import BeautifulSoup
from googlesearch import search

def check_url_structure(url):
    phishing_patterns = [r"https?://.@.", r"https?://\d+\.\d+\.\d+\.\d+"]  
    for pattern in phishing_patterns:
        if re.search(pattern, url):
            return True 
    return False

def check_https(url):
    return not url.startswith("https://")

def is_in_google_search(url):
    query = url.replace("https://", "").replace("http://", "")
    try:
        results = list(search(query, num_results=3))
        return len(results) > 0
    except:
        return False

def check_phishing_keywords(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text().lower()
        phishing_words = ["password", "verify", "confirm", "account locked"]
        return any(word in text for word in phishing_words)
    except:
        return True

def detect_phishing(url):
    warnings = []

    if check_url_structure(url):
        warnings.append("❌ Suspicious URL structure detected.")

    if check_https(url):
        warnings.append("❌ Website is not using HTTPS.")

    if not is_in_google_search(url):
        warnings.append("❌ Website is not found in Google search.")

    if check_phishing_keywords(url):
        warnings.append("❌ Phishing-related words detected on the page.")

    if warnings:
        print("\n".join(warnings))
        print("⚠ This website may be a phishing site!")
    else:
        print("✅ This website seems safe 😛.")

if __name__ == "__main__":
    url = input("Enter a URL to check: ")
    detect_phishing(url)
