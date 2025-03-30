# Search Engine Discovery

* 識別暴露的文件：
  * `site:example.com filetype:pdf`
  * `site:example.com (filetype:xls OR filetype:docx)`
* 發現設定檔：
  * `site:example.com inurl:config.php`
  * `site:example.com (ext:conf OR ext:cnf)`（搜尋設定檔常用的副檔名）
* 尋找資料庫備份：
  * `site:example.com inurl:backup`
  * `site:example.com filetype:sql`

以下是一些常見的 Google Dorks 範例，更多範例請參考[Google Hacking Database](https://www.exploit-db.com/google-hacking-database)：

<table data-header-hidden><thead><tr><th width="142.11328125"></th><th width="309.5703125"></th><th></th><th></th></tr></thead><tbody><tr><td>操作員</td><td>操作符描述</td><td>例子</td><td>範例說明</td></tr><tr><td><code>site:</code></td><td>將結果限製到特定的網站或網域。</td><td><code>site:example.com</code></td><td>尋找 example.com 上所有可公開造訪的頁面。</td></tr><tr><td><code>inurl:</code></td><td>尋找 URL 中含有特定術語的頁面。</td><td><code>inurl:login</code></td><td>搜尋任何網站上的登入頁面。</td></tr><tr><td><code>filetype:</code></td><td>搜尋特定類型的文件。</td><td><code>filetype:pdf</code></td><td>尋找可下載的 PDF 文件。</td></tr><tr><td><code>intitle:</code></td><td>尋找標題中包含特定術語的頁面。</td><td><code>intitle:"confidential report"</code></td><td>尋找標題為「機密報告」或類似名稱的文件。</td></tr><tr><td><code>intext:</code>或者<code>inbody:</code></td><td>在頁面正文中搜尋某個術語。</td><td><code>intext:"password reset"</code></td><td>識別包含術語「密碼重設」的網頁。</td></tr><tr><td><code>cache:</code></td><td>顯示網頁的快取版本（如果可用）。</td><td><code>cache:example.com</code></td><td>查看 example.com 的快取版本以查看其先前的內容。</td></tr><tr><td><code>link:</code></td><td>尋找連結到特定網頁的頁面。</td><td><code>link:example.com</code></td><td>識別連結到 example.com 的網站。</td></tr><tr><td><code>related:</code></td><td>尋找與特定網頁相關的網站。</td><td><code>related:example.com</code></td><td>發現與 example.com 類似的網站。</td></tr><tr><td><code>info:</code></td><td>提供網頁的資訊摘要。</td><td><code>info:example.com</code></td><td>獲取有關 example.com 的基本詳細信息，例如其標題和描述。</td></tr><tr><td><code>define:</code></td><td>提供單字或短語的定義。</td><td><code>define:phishing</code></td><td>從各種來源取得「網路釣魚」的定義。</td></tr><tr><td><code>numrange:</code></td><td>搜尋特定範圍內的數字。</td><td><code>site:example.com numrange:1000-2000</code></td><td>在 example.com 上尋找包含 1000 至 2000 之間的數字的頁面。</td></tr><tr><td><code>allintext:</code></td><td>尋找正文中包含所有指定字詞的頁面。</td><td><code>allintext:admin password reset</code></td><td>搜尋正文中同時包含「管理者」和「密碼重設」的頁面。</td></tr><tr><td><code>allinurl:</code></td><td>尋找包含 URL 中所有指定單字的頁面。</td><td><code>allinurl:admin panel</code></td><td>尋找 URL 中帶有「admin」和「panel」的頁面。</td></tr><tr><td><code>allintitle:</code></td><td>尋找標題中包含所有指定字詞的頁面。</td><td><code>allintitle:confidential report 2023</code></td><td>搜尋標題中帶有「機密」、「報告」和「2023」的頁面。</td></tr><tr><td><code>AND</code></td><td>透過要求所有術語都存在來縮小結果範圍。</td><td><code>site:example.com AND (inurl:admin OR inurl:login)</code></td><td>在 example.com 上專門尋找管理或登入頁面。</td></tr><tr><td><code>OR</code></td><td>透過包含含有任意術語的頁面來擴大搜尋結果。</td><td><code>"linux" OR "ubuntu" OR "debian"</code></td><td>搜尋提及 Linux、Ubuntu 或 Debian 的網頁。</td></tr><tr><td><code>NOT</code></td><td>排除包含指定術語的結果。</td><td><code>site:bank.com NOT inurl:login</code></td><td>尋找 bank.com 上除登入頁面之外的頁面。</td></tr><tr><td><code>*</code>（通配符）</td><td>代表任意字元或單字。</td><td><code>site:socialnetwork.com filetype:pdf user* manual</code></td><td>在 socialnetwork.com 上搜尋 PDF 格式的使用者手冊（使用者指南、使用者手冊）。</td></tr><tr><td><code>..</code>（範圍搜尋）</td><td>尋找指定數值範圍內的結果。</td><td><code>site:ecommerce.com "price" 100..500</code></td><td>在電子商務網站上尋找價格在 100 到 500 之間的產品。</td></tr><tr><td><code>" "</code>（引號）</td><td>搜尋精確的短語。</td><td><code>"information security policy"</code></td><td>尋找提及精確短語「資訊安全政策」的文件。</td></tr><tr><td><code>-</code>（減號）</td><td>從搜尋結果中排除術語。</td><td><code>site:news.com -inurl:sports</code></td><td>在 news.com 上搜尋新聞文章（不包括體育相關內容）。</td></tr></tbody></table>

*

\
