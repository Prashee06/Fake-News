from flask import Flask, render_template, request
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import re
import os
from PIL import Image
import pytesseract

from final_verification import verify_news


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ============================================================
# TESSERACT
# ============================================================

pytesseract.pytesseract.tesseract_cmd = "tesseract"


# ============================================================
# LOAD BiLSTM MODEL
# ============================================================

print("Loading BiLSTM model...")

model = tf.keras.models.load_model(
    "fake_news_bilstm.keras"
)

with open(
    "tokenizer.pkl",
    "rb"
) as file:

    tokenizer = pickle.load(file)


MAX_LENGTH = 200


print("BiLSTM model loaded successfully.")


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"http\S+|www\S+|https\S+",
        "",
        text
    )

    text = re.sub(
        r"<.*?>",
        "",
        text
    )

    text = re.sub(
        r"[^a-zA-Z\s]",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


# ============================================================
# BiLSTM PREDICTION
# ============================================================

def predict_news(text):

    cleaned = clean_text(text)

    sequence = tokenizer.texts_to_sequences(
        [cleaned]
    )

    padded = pad_sequences(
        sequence,
        maxlen=MAX_LENGTH,
        padding="post",
        truncating="post"
    )

    prediction = model.predict(
        padded,
        verbose=0
    )[0][0]

    if prediction >= 0.5:

        return (
            "REAL NEWS",
            round(
                prediction * 100,
                2
            )
        )

    else:

        return (
            "FAKE NEWS",
            round(
                (1 - prediction) * 100,
                2
            )
        )


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# IMAGE PREDICTION
# ============================================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    # --------------------------------------------------------
    # CHECK IMAGE
    # --------------------------------------------------------

    if "image" not in request.files:

        return render_template(
            "index.html",
            error="Please upload a news image."
        )


    image_file = request.files["image"]


    if image_file.filename == "":

        return render_template(
            "index.html",
            error="Please select an image."
        )


    # --------------------------------------------------------
    # SAVE IMAGE
    # --------------------------------------------------------

    filename = image_file.filename

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    image_file.save(
        filepath
    )


    # --------------------------------------------------------
    # OCR
    # --------------------------------------------------------

    try:

        print("\nReading uploaded image...")

        image = Image.open(
            filepath
        )

        extracted_text = pytesseract.image_to_string(
            image
        )

        extracted_text = extracted_text.strip()


    except Exception as e:

        return render_template(
            "index.html",
            error=(
                "Could not read the image: "
                + str(e)
            )
        )


    # --------------------------------------------------------
    # CHECK OCR
    # --------------------------------------------------------

    if not extracted_text:

        return render_template(
            "index.html",
            error=(
                "No readable news text was found. "
                "Please upload an image containing "
                "a news headline or article text."
            )
        )


    print("\nOCR TEXT:")
    print(extracted_text)


    # --------------------------------------------------------
    # BiLSTM
    # --------------------------------------------------------

    prediction, confidence = predict_news(
        extracted_text
    )


    print("\nBiLSTM:")
    print(prediction)
    print(confidence)


    # --------------------------------------------------------
    # REAL-WORLD NEWS VERIFICATION
    # --------------------------------------------------------

    try:

        verification_result = verify_news(
            extracted_text
        )

    except Exception as e:

        print(
            "Verification error:",
            e
        )

        verification_result = {
            "status": "UNVERIFIED",
            "score": 0,
            "query": "",
            "results": []
        }


    # --------------------------------------------------------
    # GET VERIFICATION INFORMATION
    # --------------------------------------------------------

    verification = verification_result.get(
        "status",
        "UNVERIFIED"
    )

    evidence_score = verification_result.get(
        "score",
        0
    )

    news_results = verification_result.get(
        "results",
        []
    )


    # --------------------------------------------------------
    # INCIDENT INFORMATION
    # --------------------------------------------------------

    if news_results:

        best_news = news_results[0]

        incident_info = (
            "The uploaded image contains a news claim "
            "that matches information found in online "
            "news reports. The strongest matching report is: "
            + best_news.get(
                "title",
                "Unknown"
            )
            + "."
        )

    else:

        incident_info = (
            "No sufficiently matching news report was "
            "found. The claim could not be independently "
            "verified from the available search results."
        )


    # --------------------------------------------------------
    # FINAL DECISION
    # --------------------------------------------------------

    if verification == "VERIFIED REAL":

        final_result = "🟢 VERIFIED REAL NEWS"

    elif verification == "LIKELY REAL":

        final_result = "🟡 LIKELY REAL NEWS"

    elif verification == "UNVERIFIED":

        final_result = "🟡 UNVERIFIED NEWS"

    else:

        final_result = "🔴 POSSIBLY FALSE / MISLEADING"


    # --------------------------------------------------------
    # SEND RESULT TO WEBPAGE
    # --------------------------------------------------------

    return render_template(
        "index.html",

        prediction=prediction,

        confidence=confidence,

        extracted_text=extracted_text,

        verification=verification,

        incident_info=incident_info,

        news_results=news_results,

        final_result=final_result,

        evidence_score=evidence_score
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)