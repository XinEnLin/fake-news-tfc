# model/train_classifier.py

import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB  # 可改為 SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# === 讀入資料 ===
print("📂 載入 TF-IDF 向量與標籤資料...")
X = joblib.load("outputs/models/tfidf_matrix.pkl")
df = pd.read_csv("data/processed/clean_articles.csv")

# === 將 verdict 轉為數值標籤（0 = 真實，1 = 假新聞）===
def convert_verdict(v):
    v = str(v).strip()
    if v in ['正確']:
        return 0  # 真新聞
    elif v in ['錯誤', '部分錯誤', '事實釐清', '證據不足']:
        return 1  # 假新聞或不明確資訊
    else:
        return 1  # 其他未知的 verdict 一律視為假


y = df['verdict'].apply(convert_verdict)

# === 分割訓練與測試集 ===
print("🔀 分割訓練與測試集...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === 建立模型 ===
print("🤖 訓練 Naive Bayes 分類器...")
model = MultinomialNB()
model.fit(X_train, y_train)

# === 評估模型 ===
y_pred = model.predict(X_test)
print("✅ 準確率 (Accuracy):", accuracy_score(y_test, y_pred))
print("📊 混淆矩陣:")
print(confusion_matrix(y_test, y_pred))
print("📋 分類報告:")
print(classification_report(y_test, y_pred, digits=3))

# === 儲存模型 ===
os.makedirs("outputs/models", exist_ok=True)
joblib.dump(model, "outputs/models/news_classifier.pkl")
print("✅ 模型已儲存：outputs/models/news_classifier.pkl")
