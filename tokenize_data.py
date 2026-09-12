import pandas as pd
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load data
train_df = pd.read_csv("train_data.csv")
test_df = pd.read_csv("test_data.csv")

X_train = train_df["content"].astype(str)
X_test = test_df["content"].astype(str)

y_train = train_df["label"].values
y_test = test_df["label"].values

# Vocabulary size
MAX_WORDS = 50000

# Maximum article length
MAX_LEN = 300

# Create tokenizer
tokenizer = Tokenizer(
    num_words=MAX_WORDS,
    oov_token="<OOV>"
)

tokenizer.fit_on_texts(X_train)

# Convert words to numbers
X_train_seq = tokenizer.texts_to_sequences(X_train)
X_test_seq = tokenizer.texts_to_sequences(X_test)

# Make all sequences same length
X_train_pad = pad_sequences(
    X_train_seq,
    maxlen=MAX_LEN,
    padding="post",
    truncating="post"
)

X_test_pad = pad_sequences(
    X_test_seq,
    maxlen=MAX_LEN,
    padding="post",
    truncating="post"
)

# Save tokenizer
with open("tokenizer.pkl", "wb") as file:
    pickle.dump(tokenizer, file)

# Save processed numerical data
import numpy as np

np.save("X_train.npy", X_train_pad)
np.save("X_test.npy", X_test_pad)
np.save("y_train.npy", y_train)
np.save("y_test.npy", y_test)

print("Vocabulary size:", len(tokenizer.word_index))
print("X_train shape:", X_train_pad.shape)
print("X_test shape:", X_test_pad.shape)
print("Tokenization completed!")