import re
import requests
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image).strip()


def extract_urls(text):
    return re.findall(r'https?://[^\s]+', text)


def extract_news_title(text):
    """
    Extract useful news words from OCR.
    Removes browser/interface text.
    """

    # Remove URL
    text = re.sub(r'https?://\S+', ' ', text)

    # Remove common browser text
    remove_words = [
        "Fake News Detection",
        "recent news images of incident",
        "Type here to search",
        "OOkie",
        "On ad",
        "06:57 PM",
        "07-09-2026",
        "v",
        "x",
        "X",
        "+"
    ]

    for word in remove_words:
        text = text.replace(word, " ")

    # Fix common OCR spacing problem
    text = text.replace("inNewZe", "in New Zealand")

    # Remove unwanted symbols
    text = re.sub(r'[^A-Za-z0-9\s]', ' ', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def search_news(query):

    url = (
        "https://news.google.com/rss/search?"
        "q=" + requests.utils.quote(query) +
        "&hl=en-IN&gl=IN&ceid=IN:en"
    )

    try:

        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.content,
            "xml"
        )

        results = []

        for item in soup.find_all("item")[:10]:

            title = item.find("title")
            link = item.find("link")
            date = item.find("pubDate")
            source = item.find("source")

            results.append({
                "title": title.text if title else "",
                "link": link.text if link else "",
                "date": date.text if date else "",
                "source": source.text if source else ""
            })

        return results

    except Exception as e:

        print("News search error:", e)

        return []


def verify_image(image_path):

    print("\nReading image...")

    raw_text = extract_text(image_path)

    print("\nRAW OCR:")
    print(raw_text)

    # Find URL
    urls = extract_urls(raw_text)

    # Clean OCR
    cleaned_text = extract_news_title(raw_text)

    print("\nCLEANED TEXT:")
    print(cleaned_text)

    # If URL exists, extract useful part from URL
    if urls:

        url = urls[0]

        print("\nNEWS URL FOUND:")
        print(url)

        # Extract article slug
        slug = url.rstrip("/").split("/")[-1]

        # Remove article ID at the end
        slug = re.sub(r'-\d+$', '', slug)

        # Convert hyphens to spaces
        slug = slug.replace("-", " ")

        query = slug

    else:

        # Use cleaned OCR
        query = cleaned_text[:150]

    print("\nSEARCH QUERY:")
    print(query)

    # Search news
    results = search_news(query)

    if results:

        status = "LIKELY REAL"

    else:

        status = "UNVERIFIED"

    return {
        "status": status,
        "text": raw_text,
        "cleaned_text": cleaned_text,
        "query": query,
        "url": urls[0] if urls else "",
        "results": results
    }