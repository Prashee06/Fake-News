from image_source_search import search_image_source


print("\n==============================")
print(" IMAGE SOURCE SEARCH")
print("==============================")

image_path = "test.jpg"

# Run image source search
result = search_image_source(image_path)

print("\n==============================")
print(" IDENTIFIERS")
print("==============================")

for identifier in result["identifiers"]:
    print(identifier)


print("\n==============================")
print(" SEARCH RESULTS")
print("==============================")

if not result["results"]:

    print("No search results found.")

else:

    for i, item in enumerate(
        result["results"][:15],
        start=1
    ):

        print(f"\n--- RESULT {i} ---")

        print("TITLE:")
        print(item["title"])

        print("\nLINK:")
        print(item["link"])

        print("\nDESCRIPTION:")
        print(item["description"])