import re
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import pytesseract
from ddgs import DDGS


# --------------------------------------------------
# TESSERACT LOCATION
# --------------------------------------------------

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# --------------------------------------------------
# OCR
# --------------------------------------------------

def extract_text(image_path):

    print("\nAnalyzing image...")

    image = Image.open(image_path).convert("RGB")

    # Increase image size
    width, height = image.size

    image = image.resize(
        (width * 3, height * 3)
    )

    # Convert to grayscale
    gray = ImageOps.grayscale(image)

    # Increase contrast
    gray = ImageEnhance.Contrast(
        gray
    ).enhance(2.5)

    # Sharpen image
    gray = gray.filter(
        ImageFilter.SHARPEN
    )

    texts = []

    # Try different OCR modes
    for psm in [6, 11, 12]:

        text = pytesseract.image_to_string(
            gray,
            config=f"--psm {psm}"
        )

        texts.append(text)

    # Combine OCR results
    final_text = "\n".join(texts)

    return final_text


# --------------------------------------------------
# EXTRACT IMAGE IDENTIFIERS
# --------------------------------------------------

def extract_image_identifiers(text):

    identifiers = []

    # Getty Images
    if re.search(
        r"getty\s*images|ettyima|gettyi",
        text,
        re.IGNORECASE
    ):

        identifiers.append(
            "Getty Images"
        )

    # Detect long image IDs
    numbers = re.findall(
        r"\b\d{8,12}\b",
        text
    )

    for number in numbers:

        if number not in identifiers:

            identifiers.append(
                number
            )

    # Detect credit
    credit = re.search(
        r"credit\s*:?\s*([A-Za-z]+)",
        text,
        re.IGNORECASE
    )

    if credit:

        credit_name = credit.group(1).upper()

        if credit_name not in identifiers:

            identifiers.append(
                credit_name
            )

    return list(
        dict.fromkeys(identifiers)
    )


# --------------------------------------------------
# WEB SEARCH
# --------------------------------------------------

def search_web(query):

    results = []

    try:

        print(
            "\nSearching:",
            query
        )

        with DDGS() as ddgs:

            data = ddgs.text(
                query,
                max_results=10
            )

            for item in data:

                results.append({

                    "title": item.get(
                        "title",
                        ""
                    ),

                    "link": item.get(
                        "href",
                        ""
                    ),

                    "description": item.get(
                        "body",
                        ""
                    )

                })

    except Exception as e:

        print(
            "Search error:",
            e
        )

    return results


# --------------------------------------------------
# SEARCH IMAGE SOURCE
# --------------------------------------------------

def search_image_source(image_path):

    # ----------------------------------------------
    # OCR
    # ----------------------------------------------

    text = extract_text(
        image_path
    )

    print("\n==============================")
    print("IMPROVED OCR")
    print("==============================")

    print(text)


    # ----------------------------------------------
    # IDENTIFIERS
    # ----------------------------------------------

    identifiers = extract_image_identifiers(
        text
    )

    print("\n==============================")
    print("IMAGE IDENTIFIERS")
    print("==============================")

    print(identifiers)


    # ----------------------------------------------
    # SEARCH
    # ----------------------------------------------

    all_results = []


    for identifier in identifiers:

        # Image ID needs exact searches
        if identifier.isdigit():

            queries = [

                f'"{identifier}"',

                f'"{identifier}" Getty Images',

                f'"{identifier}" news',

                f'"{identifier}" photograph'

            ]

        # Getty Images
        elif identifier.lower() == "getty images":

            queries = [

                '"Getty Images" news photograph',

                '"Getty Images" incident photograph'

            ]

        # Photographer / credit
        else:

            queries = [

                f'"{identifier}" news photograph',

                f'"{identifier}" incident photograph'

            ]


        # ------------------------------------------
        # Run searches
        # ------------------------------------------

        for query in queries:

            results = search_web(
                query
            )

            all_results.extend(
                results
            )


    # ----------------------------------------------
    # REMOVE DUPLICATES
    # ----------------------------------------------

    unique_results = {}

    for result in all_results:

        link = result.get(
            "link",
            ""
        )

        if link and link not in unique_results:

            unique_results[link] = result


    final_results = list(
        unique_results.values()
    )


    # ----------------------------------------------
    # RETURN
    # ----------------------------------------------

    return {

        "ocr_text": text,

        "identifiers": identifiers,

        "results": final_results

    }