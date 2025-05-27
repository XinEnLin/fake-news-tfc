import os
import pandas as pd
import jieba
import re

# 停用詞載入函式
def load_stopwords(filepath="data/stopwords/stopwords.txt"):
    if not os.path.exists(filepath):
        print("⚠️ 無停用詞檔，略過停用處理")
        return set()
    with open(filepath, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

# 中文清洗函式
def clean_text(text):
    # 去除英文、數字、標點
    text = re.sub(r'[^\u4e00-\u9fa5]', '', text)
    return text

# 主流程
def main():
    raw_path = "data/raw/tfc_articles.csv"
    output_path = "data/processed/clean_articles.csv"
    stopwords = load_stopwords()

    df = pd.read_csv(raw_path)
    
    cleaned_texts = []
    for content in df['content'].astype(str):
        clean = clean_text(content)
        tokens = jieba.cut(clean)
        tokens = [t for t in tokens if t not in stopwords and len(t) > 1]
        cleaned_texts.append(' '.join(tokens))

    df['tokens'] = cleaned_texts
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"✅ 已儲存處理後文章至：{output_path}")

if __name__ == "__main__":
    main()
