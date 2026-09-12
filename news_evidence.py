import requests
from bs4 import BeautifulSoup
from ddgs import DDGS


def search_news(query):

    print("\nSearching news for:")
    print(query)

    results = []

    try:

        with DDGS() as ddgs:

            data = ddgs.text(
                query,
                max_results=10
            )

            for item in data:

                title = item.get(
                    "title",
                    ""
                )

                link = item.get(
                    "href",
                    ""
                )

                description = item.get(
                    "body",
                    ""
                )

                # Keep useful results
                if title or description:

                    results.append({

                        "title": title,

                        "link": link,

                        "description": description

                    })

    except Exception as e:

        print(
            "Search error:",
            e
        )

    return results


def get_article_text(url):

    try:

        headers = {
            "User-Agent":
            "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:

            return ""

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove unwanted elements
        for element in soup(
            ["script", "style", "nav",
             "footer", "header"]
        ):

            element.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        return text[:10000]

    except Exception:

        return ""


def find_matching_news(query):

    results = search_news(
        query
    )

    useful_results = []

    for result in results:

        title = result["title"]

        description = result[
            "description"
        ]

        # Simple relevance check
        combined = (
            title + " " +
            description
        ).lower()

        words = query.lower().split()

        matches = 0

        for word in words:

            if len(word) > 3 and word in combined:

                matches += 1

        # Require several matching words
        if matches >= 2:

            result["match_score"] = matches

            useful_results.append(
                result
            )

    # Highest matching results first
    useful_results.sort(
        key=lambda x:
        x["match_score"],
        reverse=True
    )

    return useful_results