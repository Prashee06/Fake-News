from image_analyzer import analyze_image


print("\n==============================")
print("     IMAGE ANALYZER TEST")
print("==============================")


result = analyze_image(
    "test.jpg"
)


print("\n==============================")
print("          RESULT")
print("==============================")


for key, value in result.items():

    print(
        f"{key}: {value}"
    )