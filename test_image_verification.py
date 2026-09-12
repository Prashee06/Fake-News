from image_verification import verify_image


result = verify_image("test.jpg")


print("\n================================")
print("      NEWS IMAGE VERIFICATION")
print("================================")


print("\nEXTRACTED TEXT:")
print(result["text"])


print("\nSEARCH QUERY:")
print(result.get("query", ""))


print("\nSTATUS:")
print(result["status"])


print("\nMATCHING NEWS:")

for news in result["results"]:

    print("\nTitle:", news["title"])
    print("Source:", news["source"])
    print("Date:", news["date"])
    print("Link:", news["link"])