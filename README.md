This repository contains a crawler designed to collect publicly available content from the PTT forums, including user-submitted articles. The crawler helps archive content that may be difficult to find or has been deleted from the public view.

############################################################################################################################################
1.用cmd直接再接壓縮完的資料夾執行EXE檔 並且開始跑後不要點擊selenium開啟的網頁
(你可以打開自己的其他瀏覽器或是啥都好。

2. driver會自動導項這個folder裡的driver所以不要亂動。 ((重要!!!!

3. 開始執行exe檔後，會自動生成一個名為 "你找的正妹在這邊" 的資料夾在這分解壓縮後的folder裡。

4. 搜尋的關鍵字將會以您輸入的搜尋字樣建立相對應的資料夾。

5. 執行過程中，會爬取在ptt包含您所輸入的關鍵字的文章，並將其存儲於該資料夾內的子資料夾，圖片也會儲存在內。

6. 在 "你找的正妹在這邊" 資料夾中，會生成一個txt檔 "processed_articles.txt"，此檔案會記錄您之前爬過的網址。

7. 即便您下次使用不同的搜尋名稱（例如：有個名字叫菊地姬奈的模特，ptt上有文章 "[正妹] 菊地姬奈 20th anniversary"），若您搜尋“菊地”或“姬奈”，程式會自動根據 "processed_articles.txt" 所記錄的網址來過濾已爬過的文章，避免重複爬取。

8. 設計此機制的原因：
    - 因為某些文章標題會以不同形式出現，例如：
        "[正妹] 菊地姬奈 滿20歲了"
        "[正妹] 菊地姬奈 20th anniversary"
        "[正妹] 菊地姬奈 早上起來刷刷牙~~~"
    - 但在ptt中有些使用者可能會發文不打全名，可能會打小名或外號，例如 "[正妹] 從側邊看姬奈"，所以這樣可以避免遺漏。

9. 推薦的關鍵字搜尋：
    - 阿江
    - 江江
    - 寺本
    - 菊地
    - 姬奈
    - 闆娘的模特
    - "闆娘的模特蒐尋出來後那些英文名子的挺有料的" EX: g.su, merry, woo, min.e

10. 如果圖片爬下來後，您進入資料夾發現不是您要找的女生並將該資料夾刪除，這樣您隔一段時間再搜尋相同關鍵字時，程式不會再次爬取不想要的資料夾。

11. 只要您不修改 "processed_articles.txt" 檔案內容，就不會重複爬取之前已經刪除過的資料夾。

############################################################################################################################################
1.Execute the EXE file directly in the extracted folder via CMD and run it. Once it starts, do not click on the webpage opened by Selenium. (You can open other browsers or do anything else.)

2.The driver will automatically locate the driver in this folder, so do not move it. (Important!)

3.Once the EXE file is executed, a folder named "The Beautiful Girl You Are Looking For" will be generated inside the extracted folder.

4.The search keyword you enter will create a corresponding folder.

5.During the execution, the program will crawl articles on PTT that contain the keyword you entered and save them in a subfolder inside the corresponding folder. Images will also be saved there.

6.In the "The Beautiful Girl You Are Looking For" folder, a text file named "processed_articles.txt" will be created. This file records the URLs of the articles you have already crawled.

7.Even if you use a different search term next time (for example: a model named "菊地姬奈" on PTT has an article "[Beauty] 菊地姬奈 20th anniversary"), if you search for “菊地” or “姬奈,” the program will automatically filter out the URLs already recorded in "processed_articles.txt" to avoid crawling the same articles again.

8.The reason for this design:

    Some article titles may appear in different formats, such as:
        "[Beauty] 菊地姬奈 滿20歲了" (Translation: "Beautiful Girl: 菊地姬奈 Turns 20")
        "[Beauty] 菊地姬奈 20th anniversary"
        "[Beauty] 菊地姬奈 早上起來刷刷牙~~~" (Translation: "Beautiful Girl: 菊地姬奈 Wakes Up and Brushes Teeth~~~")
    Some users on PTT might not use the full name, like "[Beauty] From the Side, 姬奈" (where 姬奈 is the nickname), so this mechanism helps to avoid missing articles.

9.Recommended search keywords:

    阿江 (Ajang)
    江江 (Jiang Jiang)
    寺本 (Shih Ben)
    菊地 (Juzhi)
    姬奈 (Jinna)
    闆娘的模特 (Ban Niang's Model)
    "Models found by Ban Niang" example keywords: g.su, merry, woo, min.e

10.If after downloading the images, you enter the folder and find that the images are not of the girl you were looking for and delete the folder, the program will not crawl the unwanted folder again when searching for the same keyword after some time.

11.As long as you don't modify the content of "processed_articles.txt", the program will not crawl articles that you have previously deleted.
