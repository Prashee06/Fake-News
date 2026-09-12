from news_evidence import find_matching_news


print("\n==============================")
print("      NEWS EVIDENCE TEST")
print("==============================")


query = input(
    "\nEnter news topic to search: "
)


results = find_matching_news(
    query
)


print("\n==============================")
print("       MATCHING NEWS")
print("==============================")


if not results:

    print(
        "No matching news found."
    )

else:

    for i, result in enumerate(
        results[:5],
        start=1
    ):

        print(
            f"\n--- NEWS {i} ---"
        )

        print(
            "Title:",
            result["title"]
        )

        print(
            "Match score:",
            result["match_score"]
        )

        print(
            "Link:",
            result["link"]
        )

        print(
            "Description:",
            result["description"]
        )