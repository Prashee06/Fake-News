import pandas as pd
import re

# ============================================================
# FAKE NEWS DETECTION USING BiLSTM
# DATA PREPROCESSING
# ============================================================

print("=" * 60)
print("FAKE NEWS DETECTION - DATA PREPROCESSING")
print("=" * 60)

# ============================================================
# 1. LOAD DATASETS
# ============================================================

fake = pd.read_csv("dataset/Fake.csv")
real = pd.read_csv("dataset/True.csv")

print("\nFake dataset shape:", fake.shape)
print("Real dataset shape:", real.shape)

# ============================================================
# 2. ADD LABELS
# ============================================================

# 0 = Fake News
# 1 = Real News

fake["label"] = 0
real["label"] = 1

# ============================================================
# 3. COMBINE BOTH DATASETS
# ============================================================

df = pd.concat([fake, real], ignore_index=True)

print("Combined dataset shape:", df.shape)

# ============================================================
# 4. DISPLAY COLUMNS
# ============================================================

print("\nColumns:")
print(df.columns.tolist())

# ============================================================
# 5. CHECK LABEL DISTRIBUTION
# ============================================================

print("\nLabel distribution:")
print(df["label"].value_counts())

# ============================================================
# 6. CHECK MISSING VALUES
# ============================================================

print("\nMissing values:")
print(df.isnull().sum())

# ============================================================
# 7. COMBINE TITLE AND TEXT
# ============================================================

df["content"] = df["title"].fillna("") + " " + df["text"].fillna("")

# ============================================================
# 8. TEXT CLEANING FUNCTION
# ============================================================

def clean_text(text):

    # Convert text to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)

    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Remove punctuation and special characters
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ============================================================
# 9. APPLY TEXT CLEANING
# ============================================================

df["content"] = df["content"].apply(clean_text)

# ============================================================
# 10. REMOVE EMPTY ARTICLES
# ============================================================

df = df[df["content"].str.strip() != ""]

# Reset index
df = df.reset_index(drop=True)

# ============================================================
# 11. DISPLAY CLEANED DATA
# ============================================================

print("\nCleaned sample:")
print(df[["content", "label"]].head(10))

# ============================================================
# 12. FINAL DATASET INFORMATION
# ============================================================

print("\nFinal dataset shape:", df.shape)

print("\nFinal label distribution:")
print(df["label"].value_counts())

# ============================================================
# 13. SAVE PROCESSED DATASET
# ============================================================

df.to_csv("processed_dataset.csv", index=False)

print("\nProcessed dataset saved successfully!")
print("File: processed_dataset.csv")

print("\n" + "=" * 60)
print("PREPROCESSING COMPLETED SUCCESSFULLY")
print("=" * 60)