from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import requests
import time
import os

class PTTImageCrawler:
    def __init__(self):
        # 設定常用的 HTTP 標頭
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
            "Cookie": "over18=1"  # 模擬已通過滿 18 歲驗證
        }

        # 記錄已處理過的文章 URL 以避免重複處理
        self.processed_article_ids = set()

        # 讀取先前處理過的文章記錄
        self.load_processed_articles()

    def load_processed_articles(self):
        """從檔案讀取已處理過的文章記錄"""
        try:
            file_path = "你找的正妹在這邊/processed_articles.txt"  # 相對路徑file_path = r"C:\Users\Test\Desktop\你找的正妹在這邊\processed_articles.txt"
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:  #用for逐行審視
                    article_url = line.strip().split(" ")[0]  
                    # 僅取出 URL 部分  .split(" ")[0] EX: https://www.pttweb.cc/bbs/Beauty/M.1733914446.A.AD1 搜尋關鍵字: "姬奈"
                    # 若想提取"姬奈" 或 搜尋關鍵字  要改成 .split(" ")[2] 或 或 .split(" ")[1]
                    self.processed_article_ids.add(article_url)
        except FileNotFoundError:
            print("處理過的文章記錄檔案不存在，將創建新的檔案。")
    


    def save_processed_article(self, article_url, search_term):
        """將新處理的文章 URL 和對應的搜尋條件存入檔案"""
        folder_path = "你找的正妹在這邊"  # 相對路徑
        file_path = os.path.join(folder_path, "processed_articles.txt")

        # 確保資料夾存在
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"{article_url} 搜尋關鍵字: \"{search_term}\"\n")

    
    def download_image(self, url, save_path):
        """下載圖片並儲存"""
        if os.path.exists(save_path):
            print(f"圖片已存在，跳過下載: {save_path}")
            return
        print(f"正在下載圖片: {url}")
        response = requests.get(url, headers=self.headers)
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print("-" * 30)

    def create_unique_dir(self, base_dir):
        """創建唯一的資料夾名稱"""
        dir_name = base_dir
        counter = 1
        # 如果資料夾已經存在，就給資料夾名稱加上一個數字後綴
        while os.path.exists(dir_name):
            dir_name = f"{base_dir}({counter})"
            counter += 1
        os.makedirs(dir_name)
        return dir_name

    def fetch_and_save_images(self, url, search_term, parent_dir):
        """抓取並儲存圖片"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  ###如果請求返回的狀態碼不是 200（表示成功），這行程式會引發異常，終止執行並進入 except 區塊
            soup = BeautifulSoup(response.text, "html.parser")

            # 使用 find_all 找到含有指定屬性的 <span> 標籤
            spans = soup.find_all("span", {"data-v-553a5074": True, "data-v-8f65c8fe": True})
            title = spans[0].text.strip()

            # 使用 create_unique_dir 處理資料夾名稱
            dir_name = self.create_unique_dir(f"{parent_dir}/{title}")

            image_links = soup.find_all("a")
            allow_file_name = ["jpg", "jpeg", "png", "gif"]
            downloaded_images = set()

            # 儲存已處理過的圖片連結，考慮到 jpg 和 jpeg 的情況
            for link in image_links:
                href = link.get("href")
                if not href:
                    continue
                file_name = href.split("/")[-1]
                extension = href.split(".")[-1].lower()

                if extension in allow_file_name:
                    # 將 jpg 和 jpeg 視為相同的文件
                    file_name_base = file_name.rsplit(".", 1)[0].lower()  # 不含副檔名的文件名
                    if file_name_base.endswith("jpeg"):
                        file_name_base = file_name_base[:-4] + "jpg"  # 轉換成 jpg 擴展名  EX: file.jpeg ----> file ----->file.jpg
                    print(f"檔案型態:{extension}")
                    print(f"url: {href}")
                    self.download_image(href, f"{dir_name}/{file_name}")
                    downloaded_images.add(file_name_base)  # 儲存無副檔名的文件名

            # 處理 <img> 標籤中的圖片
            img_tags = soup.find_all("img", {"loading": "lazy"})
            for img in img_tags:
                img_url = img.get("src")
                if img_url:
                    # 去除 img 的副檔名並轉換為 jpg
                    img_file_name = img_url.split("/")[-1]
                    img_file_name_base = img_file_name.rsplit(".", 1)[0].lower()
                    if img_file_name_base.endswith("jpeg"):
                        img_file_name_base = img_file_name_base[:-4] + "jpg"  # 轉換成 jpg 擴展名

                    # 檢查 img 標籤中的圖片是否已經下載過
                    if img_file_name_base not in downloaded_images:
                        print(f"下載圖片 (從 <img> 標籤): {img_url}")
                        self.download_image(img_url, f"{dir_name}/{img_file_name}")
                        downloaded_images.add(img_file_name_base)

            # 記錄已處理的文章
            self.save_processed_article(url, search_term)

        except requests.exceptions.RequestException as e:
            print(f"下載圖片時發生錯誤: {e}")
        except Exception as e:
            print(f"發生其他錯誤: {e}")

    def start_driver(self):
        """啟動 Selenium WebDriver"""
        options = Options()
        options.use_chromium = True
        service = Service("./msedgedriver.exe")  # 相對路徑
        driver = webdriver.Edge(service=service, options=options)
        return driver

    def scroll_page(self, driver):
        """先滾動到網頁進度條的一半，再花兩秒慢慢滾動到底"""
        # 滾動到進度條的一半
        half_height_script = "window.scrollTo(0, document.body.scrollHeight / 2);"
        driver.execute_script(half_height_script)
        time.sleep(2)  # 等待 2 秒，確保內容加載

        # 花 2 秒慢慢滾動到底
        full_height_script = """
        let currentPosition = document.body.scrollHeight / 2;
        let endPosition = document.body.scrollHeight;
        let step = (endPosition - currentPosition) / 100;

        function scrollDown() {
            if (currentPosition < endPosition) {
                currentPosition += step;
                window.scrollTo(0, currentPosition);
                setTimeout(scrollDown, 20); // 每次滾動間隔 20ms
            }
        }
        scrollDown();
        """
        driver.execute_script(full_height_script)
        time.sleep(2)  # 等待 2 秒以確保滾動完成
    
    # Adjust scroll_up_in_divisions to handle step-by-step scrolling
    def scroll_up_in_divisions(self, driver, total_divisions, current_step):
        page_height = driver.execute_script("return document.body.scrollHeight")
        scroll_distance = page_height / total_divisions
        target_position = page_height - (scroll_distance * current_step)
        driver.execute_script(f"window.scrollTo(0, {target_position});")
        time.sleep(15)  # 停留以確保內容加載



    def crawl_ptt_page(self, search_term):
        driver = self.start_driver()
        base_url = f"https://www.pttweb.cc/bbs/Beauty/search/t/{search_term}"
        driver.get(base_url)

        # 滾動到底部 5 次
        for _ in range(5):  # 重複執行5次
            self.scroll_page(driver)

        # 獲取頁面上的鏈接並下載圖片
        self.fetch_links_and_download(driver, search_term)

        # 分段向上滾動，並執行相同操作
        divisions = 12  # 分為12段
        for division in range(divisions):
            self.scroll_up_in_divisions(driver, divisions, division + 1)
            self.fetch_links_and_download(driver, search_term)

        # 確保所有操作完成後退出瀏覽器
        driver.quit()

    # Helper function for extracting links and downloading images
    def fetch_links_and_download(self, driver, search_term):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        articles = soup.find_all("a", class_="e7-article-default")

        parent_dir = "你找的正妹在這邊" + f"\\{search_term}"  # 相對路徑
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        for article in articles:
            article_url = f"https://www.pttweb.cc{article['href']}"
            if article_url not in self.processed_article_ids:
                self.processed_article_ids.add(article_url)
                print(f"處理文章: {article_url}")
                self.fetch_and_save_images(article_url, search_term, parent_dir)
            else:
                print(f"跳過重複文章: {article_url}")

        
if __name__ == "__main__":
    
    search_term = input("請輸入您想爬的正妹：")
    crawler = PTTImageCrawler()
    crawler.crawl_ptt_page(search_term)
    input("Press Enter to exit...")