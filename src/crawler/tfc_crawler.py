# src/crawler/tfc_crawler.py

import requests                      # 發送 HTTP 請求
from bs4 import BeautifulSoup       # 解析 HTML 結構
import csv                          # 輸出為 CSV
import os                           # 建立資料夾
import time                         # 設定 delay，避免請求過快被封鎖

# 網站主網址
BASE_URL = "https://tfc-taiwan.org.tw"

# 最新消息頁面 URL 模板（可用 page=0, 1, 2... 依序翻頁）
LATEST_NEWS_URL = BASE_URL + "/latest-news?page={}"

# 輸出的 CSV 檔案路徑
OUTPUT_FILE = "data/raw/tfc_articles.csv"

# ---------------------------------------------------------
# 取得單一頁面上的查核文章連結（只抓 /fact-check-reports/ 的文章）
def fetch_article_links(page_num):
    url = LATEST_NEWS_URL.format(page_num)
    res = requests.get(url)
    if res.status_code != 200:
        print(f"❌ Failed to fetch page {page_num}")
        return []

    # 解析該頁 HTML 結構
    soup = BeautifulSoup(res.text, 'html.parser')

    # 找出每篇文章的 article 標籤
    articles = soup.select("article.node--type-article")

    links = []
    for article in articles:
        # 每篇文章中，圖片的 <a> 標籤中包含了真正的文章連結
        a_tag = article.select_one('.field--name-field-image a')
        if a_tag:
            href = a_tag.get('href')
            if href and href.startswith("/fact-check-reports"):
                links.append(BASE_URL + href)  # 補上完整網址
    return links

# ---------------------------------------------------------
# 拿到單一篇文章的詳細資料（標題、日期、查核結果、內容）
def fetch_article_detail(url):
    res = requests.get(url)
    if res.status_code != 200:
        print(f"❌ Failed to fetch article {url}")
        return None

    soup = BeautifulSoup(res.text, 'html.parser')

    try:
        # 標題
        title = soup.find('h1', class_='article-title').text.strip()

        # 發布日期
        date = soup.find('time').text.strip()

        # 查核結論（例如「錯誤」、「部份錯誤」、「無明確根據」）
        verdict_elem = soup.select_one('.field--name-field-verdict .field__item')
        verdict = verdict_elem.text.strip() if verdict_elem else '未知'

        # 文章內文（HTML 中的主體文字區塊）
        content_block = soup.select_one('.field--name-body')
        content = content_block.get_text(strip=True) if content_block else ""
    except Exception as e:
        print(f"⚠️ Error parsing {url}: {e}")
        return None

    return {
        'title': title,
        'date': date,
        'verdict': verdict,
        'url': url,
        'content': content[:300]  # 只取前 300 字做摘要用
    }

# ---------------------------------------------------------
# 將所有文章寫入 CSV 檔案
def save_to_csv(articles, filename):
    # 若目錄不存在則自動建立
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # 開啟 CSV 檔案並寫入欄位與每篇文章資料
    with open(filename, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'date', 'verdict', 'url', 'content'])
        writer.writeheader()
        for article in articles:
            writer.writerow(article)
    print(f"✅ Saved {len(articles)} articles to {filename}")

# ---------------------------------------------------------
# 主流程：爬取前 N 頁，組合成一個資料集並存檔
def main(max_pages=3):
    all_articles = []
    for page in range(0, max_pages):  # 注意：TFC 的頁碼從 0 開始
        print(f"🔎 Fetching page {page}...")
        links = fetch_article_links(page)
        for link in links:
            detail = fetch_article_detail(link)
            if detail:
                all_articles.append(detail)
            time.sleep(0.5)  # 禮貌性延遲，避免請求過快
    save_to_csv(all_articles, OUTPUT_FILE)

# ---------------------------------------------------------
# 程式進入點
if __name__ == "__main__":
    main(max_pages=3)  # 預設只抓前 3 頁，可自行增加頁數
