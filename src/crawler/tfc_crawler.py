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

# 加入標頭來避免被網站拒絕
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/117.0.0.0 Safari/537.36"
}

# ---------------------------------------------------------
# 取得單一頁面上的查核文章連結（只抓 /fact-check-reports/ 的文章）
def fetch_article_links(page_num):
    url = LATEST_NEWS_URL.format(page_num)
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        print(f"❌ Failed to fetch page {page_num}")
        return []

    soup = BeautifulSoup(res.text, 'html.parser')

    # 抓 figure 區塊中的 <a> 標籤（用於連結查核文章）
    figure_links = soup.select('figure.wp-block-kadence-image a')

    links = []
    for a_tag in figure_links:
        href = a_tag.get('href')
        if href and '/fact-check-reports/' in href:
            if href.startswith("http"):
                links.append(href)
            else:
                links.append(BASE_URL + href)
    print(f"✅ Page {page_num}: found {len(links)} article links")
    return links


# ---------------------------------------------------------
# 拿到單一篇文章的詳細資料（標題、日期、查核結果、內容）
def fetch_article_detail(url):
    res = requests.get(url, headers=HEADERS)  # ✅ 同樣加上 headers
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
    for page in range(1, max_pages+1):  # 注意：TFC 的頁碼從 1 開始
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
