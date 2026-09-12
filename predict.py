import tensorflow as tf
import pickle
import re
from tensorflow.keras.preprocessing.sequence import pad_sequences


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

model = tf.keras.models.load_model("fake_news_bilstm.keras")

with open("tokenizer.pkl", "rb") as file:
    tokenizer = pickle.load(file)


MAX_LENGTH = 200


# ============================================================
# TEXT CLEANING
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
# PREDICT NEWS
# ============================================================

def predict_news(news):

    cleaned_news = clean_text(news)

    sequence = tokenizer.texts_to_sequences(
        [cleaned_news]
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

        result = "REAL NEWS"
        confidence = prediction * 100

    else:

        result = "FAKE NEWS"
        confidence = (1 - prediction) * 100

    return result, confidence


# ============================================================
# MAIN PROGRAM
# ============================================================

print("=" * 60)
print("        REAL-WORLD NEWS DETECTION SYSTEM")
print("              USING BiLSTM")
print("=" * 60)

print("\nEnter a news article.")
print("Type EXIT to stop.\n")


while True:

    news = input("Enter News: ")

    if news.lower() == "exit":
        print("\nProgram stopped.")
        break

    if not news.strip():
        print("\nPlease enter some news.\n")
        continue

    result, confidence = predict_news(news)

    print("\n" + "-" * 60)
    print("PREDICTION:", result)
    print("CONFIDENCE:", round(confidence, 2), "%")
    print("-" * 60)