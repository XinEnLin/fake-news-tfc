# features/vectorizer.py

import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# === 路徑設定 ===
INPUT_FILE = "data/processed/clean_articles.csv"
MODEL_DIR = "outputs/models"
VECTORIZER_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
MATRIX_PATH = os.path.join(MODEL_DIR, "tfidf_matrix.pkl")

# === 建立輸出資料夾 ===
os.makedirs(MODEL_DIR, exist_ok=True)

# === 讀取資料 ===
print(f"📂 讀取資料：{INPUT_FILE}")
df = pd.read_csv(INPUT_FILE)

# === TF-IDF 向量化 ===
print("🔄 正在執行 TF-IDF 向量化...")
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["tokens"].astype(str))  # 確保欄位為文字

# === 儲存模型與向量 ===
joblib.dump(vectorizer, VECTORIZER_PATH)
joblib.dump(X, MATRIX_PATH)

print(f"✅ TF-IDF 向量儲存至：{MATRIX_PATH}")
print(f"✅ 向量器模型儲存至：{VECTORIZER_PATH}")
print(f"🔢 向量維度：{X.shape}")
