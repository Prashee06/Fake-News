import re
from news_evidence import find_matching_news


def clean_text(text):
    """
    Clean OCR text for searching.
    """

    text = text.lower()

    # Remove URLs
    text = re.sub(
        r'https?://\S+',
        ' ',
        text
    )

    # Keep letters and numbers
    text = re.sub(
        r'[^a-z0-9\s]',
        ' ',
        text
    )

    # Remove extra spaces
    text = re.sub(
        r'\s+',
        ' ',
        text
    ).strip()

    return text


def create_search_query(ocr_text):

    text = clean_text(
        ocr_text
    )

    words = text.split()

    # Remove common OCR/browser words
    unwanted = {
        "fake",
        "news",
        "detection",
        "google",
        "chrome",
        "search",
        "home",
        "type",
        "here",
        "windows",
        "taskbar",
        "today",
        "recent"
    }

    words = [
        word
        for word in words
        if word not in unwanted
    ]

    # Keep a reasonable query
    words = words[:15]

    return " ".join(words)


def calculate_evidence(results, query):

    if not results:

        return {
            "score": 0,
            "status": "UNVERIFIED"
        }

    best_score = max(
        result.get(
            "match_score",
            0
        )
        for result in results
    )

    source_count = len(results)

    # Evidence rules
    if best_score >= 7 and source_count >= 2:

        status = "VERIFIED REAL"

        score = min(
            100,
            70 + best_score * 3
        )

    elif best_score >= 5:

        status = "LIKELY REAL"

        score = min(
            85,
            50 + best_score * 3
        )

    elif best_score >= 3:

        status = "UNVERIFIED"

        score = 40 + best_score * 3

    else:

        status = "UNVERIFIED"

        score = 20

    return {
        "score": score,
        "status": status
    }


def verify_news(ocr_text):

    print("\n==============================")
    print("      FINAL NEWS VERIFICATION")
    print("==============================")

    print("\nOCR TEXT:")
    print(ocr_text)

    query = create_search_query(
        ocr_text
    )

    print("\nSEARCH QUERY:")
    print(query)

    if not query:

        return {
            "status": "UNVERIFIED",
            "score": 0,
            "query": "",
            "results": []
        }

    results = find_matching_news(
        query
    )

    evidence = calculate_evidence(
        results,
        query
    )

    print("\n==============================")
    print("          RESULT")
    print("==============================")

    print(
        "STATUS:",
        evidence["status"]
    )

    print(
        "CONFIDENCE:",
        evidence["score"],
        "%"
    )

    print(
        "\nMATCHING NEWS:"
    )

    for result in results[:5]:

        print(
            "\nTitle:",
            result["title"]
        )

        print(
            "Score:",
            result["match_score"]
        )

        print(
            "Source:",
            result["link"]
        )

        print(
            "Description:",
            result["description"]
        )

    return {
        "status": evidence["status"],
        "score": evidence["score"],
        "query": query,
        "results": results[:5]
    }