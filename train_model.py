import pandas as pd
import numpy as np
import pickle
import re

from sklearn.model_selection import train_test_split

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping


# ============================================================
# 1. LOAD DATA
# ============================================================

print("=" * 60)
print("FAKE NEWS DETECTION USING BiLSTM")
print("=" * 60)

df = pd.read_csv("processed_dataset.csv")

print("\nDataset shape:", df.shape)

# Keep only required columns
df = df[["content", "label"]]

# Remove missing values
df = df.dropna()

# ============================================================
# 2. USE A SMALL BALANCED DATASET
# ============================================================
# This makes training faster on a normal laptop.

fake = df[df["label"] == 0].sample(n=6000, random_state=42)
real = df[df["label"] == 1].sample(n=6000, random_state=42)

df = pd.concat([fake, real])

# Shuffle
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print("Training dataset used:", df.shape)
print("\nLabel distribution:")
print(df["label"].value_counts())


# ============================================================
# 3. INPUT AND OUTPUT
# ============================================================

X = df["content"].astype(str)
y = df["label"].values


# ============================================================
# 4. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# 5. TOKENIZATION
# ============================================================

MAX_WORDS = 20000
MAX_LENGTH = 200

tokenizer = Tokenizer(
    num_words=MAX_WORDS,
    oov_token="<OOV>"
)

tokenizer.fit_on_texts(X_train)

X_train_seq = tokenizer.texts_to_sequences(X_train)
X_test_seq = tokenizer.texts_to_sequences(X_test)


# ============================================================
# 6. PADDING
# ============================================================

X_train_pad = pad_sequences(
    X_train_seq,
    maxlen=MAX_LENGTH,
    padding="post",
    truncating="post"
)

X_test_pad = pad_sequences(
    X_test_seq,
    maxlen=MAX_LENGTH,
    padding="post",
    truncating="post"
)

print("\nTraining sequence shape:", X_train_pad.shape)
print("Testing sequence shape:", X_test_pad.shape)


# ============================================================
# 7. BUILD BiLSTM MODEL
# ============================================================

model = Sequential([
    Embedding(
        input_dim=MAX_WORDS,
        output_dim=64,
        input_length=MAX_LENGTH
    ),

    Bidirectional(
        LSTM(64)
    ),

    Dropout(0.5),

    Dense(32, activation="relu"),

    Dropout(0.3),

    Dense(1, activation="sigmoid")
])


# ============================================================
# 8. COMPILE MODEL
# ============================================================

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.summary()


# ============================================================
# 9. TRAIN MODEL
# ============================================================

print("\nStarting BiLSTM training...")

early_stop = EarlyStopping(
    monitor="val_loss",
    patience=1,
    restore_best_weights=True
)

history = model.fit(
    X_train_pad,
    y_train,
    validation_split=0.1,
    epochs=2,
    batch_size=64,
    callbacks=[early_stop],
    verbose=1
)


# ============================================================
# 10. EVALUATE MODEL
# ============================================================

loss, accuracy = model.evaluate(
    X_test_pad,
    y_test,
    verbose=0
)

print("\n" + "=" * 60)
print("MODEL EVALUATION")
print("=" * 60)

print("Test Accuracy:", round(accuracy * 100, 2), "%")


# ============================================================
# 11. SAVE MODEL
# ============================================================

model.save("fake_news_bilstm.keras")

with open("tokenizer.pkl", "wb") as file:
    pickle.dump(tokenizer, file)

print("\nModel saved as:")
print("fake_news_bilstm.keras")

print("\nTokenizer saved as:")
print("tokenizer.pkl")

print("\n" + "=" * 60)
print("TRAINING COMPLETED")
print("=" * 60)