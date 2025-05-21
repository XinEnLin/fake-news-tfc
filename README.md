# 中文假新聞分類系統 Fake News Classifier (Taiwan TFC Version)

本專案旨在建立一個使用機器學習的假新聞分類系統，資料來源為「[台灣事實查核中心（TFC）](https://tfc-taiwan.org.tw/)」。透過中文自然語言處理（NLP）技術與分類模型，協助使用者辨別新聞資訊的真偽。

---

## ? 專案特色

- ? 中文語料：爬取台灣本地假新聞澄清資料
- ? 機器學習：使用 TF-IDF + Naive Bayes 進行分類
- ? NLP 處理：結合 jieba 分詞與中文停用詞表
- ? 可選 Streamlit Web App 作為互動介面

---

## ?? 專案資料夾結構

```plaintext
fake_news_project/
├── data/                      # 儲存原始與處理過的資料
│   ├── raw/                  # 原始爬下來的新聞與標註資料（HTML / JSON）
│   ├── processed/            # 清理後的資料（CSV / JSON）
│   └── stopwords/            # 中文停用詞列表（.txt）
│
├── notebooks/                # 分析與實驗 Jupyter 筆記本
│   ├── 01_data_exploration.ipynb    # 資料探索與分析
│   ├── 02_preprocessing.ipynb       # 資料清理與斷詞
│   ├── 03_model_training.ipynb      # 模型訓練（TF-IDF + Naive Bayes等）
│   └── 04_evaluation.ipynb          # 模型評估與視覺化
│
├── src/                      # Python 模組原始碼
│   ├── crawler/              # 網頁爬蟲模組
│   │   └── tfc_crawler.py    # 爬取台灣事實查核中心新聞
│   ├── preprocessing/        # 清理與斷詞模組
│   │   └── clean_text.py     # 中文清理與 jieba 分詞
│   ├── features/             # 特徵工程
│   │   └── vectorizer.py     # TF-IDF 建立與儲存
│   └── model/                # 模型訓練與預測模組
│       └── train_model.py    # 訓練與保存模型
│
├── app/                      # 最終展示用的 Web App（可選 Streamlit）
│   └── app.py                # UI 可貼新聞判斷真偽
│
├── outputs/                  # 結果、圖表與模型
│   ├── figures/              # 混淆矩陣、ROC 曲線等圖表
│   ├── models/               # 儲存訓練好的模型 (.pkl)
│   └── logs/                 # 訓練過程中的記錄與 log
│
├── requirements.txt          # 套件需求檔案（pip install -r）
├── README.md                 # 專案說明
└── .gitignore                # 忽略無用檔案
ˋˋˋ

---

## 使用技術

- Python 3.10+
- jieba 中文分詞
- scikit-learn
- pandas / numpy
- matplotlib / seaborn
- Streamlit（可選用來展示結果）

---

##  快速開始 

1. **安裝套件**

```bash
pip install -r requirements.txt