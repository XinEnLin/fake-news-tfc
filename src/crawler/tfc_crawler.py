# src/crawler/tfc_crawler.py

import requests                      # 發送 HTTP 請求
from bs4 import BeautifulSoup       # 解析 HTML 結構
import csv                          # 儲出為 CSV 檔
import os                           # 處理路徑與建立資料夾
import time                         # 加入延遲，避免對網站造成壓力
import re                           # 使用正則表達式擷取日期與標題結構

# 網站主網址
BASE_URL = "https://tfc-taiwan.org.tw"

# 輸出的 CSV 檔案儲存路徑
OUTPUT_FILE = "data/raw/tfc_articles.csv"

# 加入標頭模擬瀏覽器，以免被網站阻擋或回傳錯誤格式
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/117.0.0.0 Safari/537.36"
}

# ---------------------------------------------------------
# 函式：抓取某一頁的所有查核文章連結
def fetch_article_links(page_num):
    # 第一頁網址沒有參數，之後頁數使用 ?pg=
    if page_num == 1:
        url = BASE_URL + "/latest-news/"
    else:
        url = BASE_URL + f"/latest-news/?pg={page_num}"

    # 發送 HTTP 請求
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        print(f"❌ Failed to fetch page {page_num}")
        return []

    # 使用 BeautifulSoup 解析 HTML 結構
    soup = BeautifulSoup(res.text, 'html.parser')

    # 選取所有含有 "Read More" 按鈕的連結
    link_tags = soup.select('a.kb-button')

    links = []
    for a_tag in link_tags:
        href = a_tag.get('href')
        if href and '/fact-check-reports/' in href:
            # 如果不是完整 URL，加上主機名稱補足
            full_url = href if href.startswith('http') else BASE_URL + href
            # 避免重複加入相同連結
            if full_url not in links:
                links.append(full_url)

    print(f"✅ Page {page_num}: found {len(links)} article links")
    return links

# ---------------------------------------------------------
# 函式：擷取單篇查核文章的詳細內容
def fetch_article_detail(url):
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        print(f"❌ Failed to fetch article {url}")
        return None

    soup = BeautifulSoup(res.text, 'html.parser')

    try:
        # 判斷是否為舊版結構：舊版含有 <h1 class="entry-title">
        is_old = bool(soup.select_one('h1.entry-title'))

        # ---------------- 新版結構 ----------------
        if not is_old:
            # 新版標題在 p > strong 中
            title_tag = soup.select_one('p.wp-block-kadence-advancedheading strong')
            title = title_tag.text.strip() if title_tag else '未知'

            # 新版日期從 <strong> 標籤中搜尋包含「發佈」的段落
            date = '未知'
            for tag in soup.find_all('strong'):
                if '發佈' in tag.text:
                    parent = tag.parent
                    if parent:
                        text = parent.get_text(strip=True).replace("發佈：", "").replace("發佈", "").strip()
                        if re.match(r"\d{4}-\d{2}-\d{2}", text):  # 確保是正確格式
                            date = text
                    break

            # 查核結論：從 verdict 元素取得（如「錯誤」、「正確」）
            verdict_tag = soup.select_one('a.kb-dynamic-list-item-link')
            verdict = verdict_tag.text.strip() if verdict_tag else '未知'

            # 內文：從彩色背景段落中選取所有 p
            paragraphs = soup.select('p.wp-block-kadence-advancedheading.has-theme-palette-7-background-color')
            content = '\n'.join([p.text.strip() for p in paragraphs])
            content = content[:100]

        # ---------------- 舊版結構 ----------------
        else:
            # 標題與查核結果寫在 h1 中，例如：【錯誤】香蕉致癌
            title_h1 = soup.select_one('h1.entry-title')
            full_title = title_h1.text.strip() if title_h1 else '未知'

            # 用正規表示法擷取【查核結論】
            verdict_match = re.match(r'【(.+?)】', full_title)
            verdict = verdict_match.group(1) if verdict_match else '未知'
            title = full_title.replace(f'【{verdict}】', '').strip()

            # 日期：從 <div class="entity-list-date"> 中擷取發布日期
            date_tag = soup.select_one('div.entity-list-date')
            date = '未知'
            if date_tag and "發布日期" in date_tag.text:
                match = re.search(r'\d{4}-\d{2}-\d{2}', date_tag.text)
                if match:
                    date = match.group(0)

            # 內文：抓取所有 <p> 段落
            paragraphs = soup.select('div.entry-content.single-content p')
            content = '\n'.join([p.text.strip() for p in paragraphs if p.text.strip()])
            content = content[:100]

        # 回傳該篇文章的所有欄位資訊
        return {
            'title': title,
            'date': date,
            'verdict': verdict,
            'url': url,
            'content': content
        }

    except Exception as e:
        print(f"⚠️ Error parsing {url}: {e}")
        return None

# ---------------------------------------------------------
# 函式：將爬下來的所有文章寫入 CSV
def save_to_csv(articles, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # 若資料夾不存在就建立
    with open(filename, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'date', 'verdict', 'url', 'content'])
        writer.writeheader()
        for article in articles:
            writer.writerow(article)
    print(f"✅ Saved {len(articles)} articles to {filename}")

# ---------------------------------------------------------
# 主函式：依序抓取每一頁的所有文章並儲存
def main(max_pages):
    all_articles = []
    for page in range(1, max_pages + 1):
        print(f"🔎 Fetching page {page}...")
        links = fetch_article_links(page)
        for link in links:
            detail = fetch_article_detail(link)
            if detail:
                all_articles.append(detail)
            time.sleep(0.5)  # 每篇文章延遲 0.5 秒，避免對網站造成過多請求
    save_to_csv(all_articles, OUTPUT_FILE)

# ---------------------------------------------------------
# 程式進入點（main）
if __name__ == "__main__":
    main(max_pages=605)  # 預設抓取前 605 頁文章（可依需求調整）
