from final_verification import verify_news


ocr_text = """
250 pilot whales die in New Zealand
after another beaching incident
"""


result = verify_news(
    ocr_text
)


print("\n==============================")
print("        FINAL OUTPUT")
print("==============================")

print(
    "Status:",
    result["status"]
)

print(
    "Confidence:",
    result["score"],
    "%"
)