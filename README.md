# README.md

> 在 Hacking 的世界裡，技術只是工具，心態才是關鍵！ 如果你想提升自己在攻防、安全測試或 CTF 競賽中的能力，以下幾個的心境和努力方向，能幫助你成為更強的hacker：

**「鍥而不捨，金石可鏤」**（《荀子·勸學》）

_🔥 : 許多漏洞、加密算法、反向工程挑戰都需要長時間的嘗試與研究。最強的hacker從不輕易放棄，他們在看似不可能的地方找到突破口。_

**「知己知彼，百戰不殆」**  《孫子兵法》\
&#xNAN;_&#xD83D;� ：hacker要成功，不僅要熟悉自己的技術，還要了解系統、目標、漏洞和防禦機制。只靠「試一試」是遠遠不夠的，深入分析、信息收集、學習敵人的防禦，才能做到無往不利。_

**「不經一番寒徹骨，怎得梅花撲鼻香」** 《黃檗禪師》

_🔥 ： 許多漏洞挖掘、代碼審計、密碼分析都需要極大的耐心。遇到困難時，不要覺得自己不夠聰明，而是要告訴自己：「這是變強的過程！」真正厲害的hacker，都經歷過無數次的失敗與煎熬。_

## 當感到無力時 ... ....

{% hint style="danger" %}
&#x20;「找出系統最脆弱的地方，然後攻擊它」
{% endhint %}

{% hint style="danger" %}
&#x20;「偷偷滲透目標系統，不讓對方發現」
{% endhint %}

{% hint style="danger" %}
&#x20;「假設開發者犯錯了，這個錯誤會讓我獲得什麼權限？」
{% endhint %}

IppSec 的網站為網路安全愛好者和專業人士提供了寶貴的資源。它包括主要關注駭客技術、安全研究和 CTF（奪旗）挑戰的教程、文章和影片。這些內容對於希望提高道德駭客和滲透測試技能的學習者很有幫助。如需詳細指南和更新，請直接造訪網站： [ippsec.rocks](https://ippsec.rocks/?) 。

***

## 系統性策略

> Bug Bounty 不是「瞎測」，需要系統性策略。使用**番茄鐘來分段測試不同目標**：
>
> **💡 Bug Bounty 4 階段番茄鐘策略**
>
> **🕵️‍♂️ 階段 1：目標偵查（Recon）** 🔹 **30 min 番茄**
>
> * 使用 `Amass`, `Subfinder` 進行子域名枚舉
> * `nmap` 進行端口掃描
> * `waybackurls` 取得歷史 API 端點
> * `gau` 查詢 Google Analytics 歷史記錄
>
> ☕ 休息 5 min
>
> ***
>
> **💣 階段 2：Web 漏洞測試** 🔹 **50 min 番茄**
>
> * 手動測試 **XSS, CSRF, SSRF**
> * Burp Suite 測試 **IDOR, BOLA, API Injection**
> * 嘗試 Exploit GraphQL API
>
> ☕ 休息 10 min
>
> ***
>
> **🚀 階段 3：Exploit 深度測試** 🔹 **90 min 番茄**
>
> * 測試 SQLi（Time-based, Blind SQL）
> * 嘗試 SSRF **與雲端伺服器整合**
> * 嘗試 CSP Bypass
>
> ☕ 休息 30 min（避免 Burnout）
>
> ***
>
> **📜 階段 4：報告與證據收集** 🔹 **45 min 番茄**
>
> * 編寫 **PoC（Proof of Concept）**
> * 確保 Payload 可重現
> * 撰寫高質量報告
>
> ☕ 休息 10 min

## **測試類別選擇表**

| **測試類別**                                                              | **測試項目**                  | **番茄鐘時間** | **休息時間** |
| --------------------------------------------------------------------- | ------------------------- | --------- | -------- |
| <mark style="color:purple;">**JavaScript 重度應用**</mark>                | DOM XSS（跨站腳本攻擊）           | 25 分鐘     | 5 分鐘     |
|                                                                       | 原型污染（Prototype Pollution） | 45 分鐘     | 10 分鐘    |
|                                                                       | WebSocket 注入              | 50 分鐘     | 10 分鐘    |
|                                                                       | CSP 規避                    | 60 分鐘     | 15 分鐘    |
| <mark style="color:purple;">**WordPress / CMS（內容管理系統）**</mark>        | 版本識別                      | 15 分鐘     | 5 分鐘     |
|                                                                       | 外掛 XSS 測試                 | 25 分鐘     | 5 分鐘     |
|                                                                       | XML-RPC API 測試            | 30 分鐘     | 5 分鐘     |
|                                                                       | PHP 反序列化漏洞                | 45 分鐘     | 10 分鐘    |
| <mark style="color:purple;">**靜態網站（Static Pages）**</mark>             | CORS 錯誤配置                 | 30 分鐘     | 5 分鐘     |
|                                                                       | 硬編碼 API 金鑰                | 25 分鐘     | 5 分鐘     |
|                                                                       | 開放重定向測試                   | 30 分鐘     | 5 分鐘     |
|                                                                       | robots.txt & 隱藏目錄測試       | 15 分鐘     | 5 分鐘     |
| <mark style="color:purple;">**SaaS 網站（軟體即服務）**</mark>                 | OAuth2 配置錯誤               | 50 分鐘     | 10 分鐘    |
|                                                                       | JWT 令牌操作                  | 50 分鐘     | 10 分鐘    |
|                                                                       | 多租戶權限提升                   | 60 分鐘     | 15 分鐘    |
|                                                                       | 子網域接管測試                   | 30 分鐘     | 5 分鐘     |
| <mark style="color:purple;">**電子商務網站（E-Commerce）**</mark>             | 結帳流程操控                    | 50 分鐘     | 10 分鐘    |
|                                                                       | 支付閘道繞過                    | 60 分鐘     | 15 分鐘    |
|                                                                       | 折扣碼濫用                     | 30 分鐘     | 5 分鐘     |
|                                                                       | 購物車篡改                     | 45 分鐘     | 10 分鐘    |
| <mark style="color:purple;">**金融科技 / 銀行應用（FinTech / Banking）**</mark> | API 限制繞過                  | 50 分鐘     | 10 分鐘    |
|                                                                       | Session 固定攻擊              | 60 分鐘     | 15 分鐘    |
|                                                                       | 交易篡改                      | 50 分鐘     | 10 分鐘    |
|                                                                       | 弱身份驗證機制                   | 45 分鐘     | 10 分鐘    |
| <mark style="color:purple;">**醫療 / HIPAA 網站**</mark>                  | 病患數據外洩                    | 60 分鐘     | 15 分鐘    |
|                                                                       | 訪問控制錯誤配置                  | 50 分鐘     | 10 分鐘    |
|                                                                       | API 敏感信息洩露                | 45 分鐘     | 10 分鐘    |
|                                                                       | 醫療隱私數據外洩                  | 60 分鐘     | 15 分鐘    |
| <mark style="color:purple;">**政府與公共部門網站**</mark>                      | 機密文件洩露                    | 50 分鐘     | 10 分鐘    |
|                                                                       | 身份驗證漏洞                    | 60 分鐘     | 15 分鐘    |
|                                                                       | 開放重定向漏洞                   | 30 分鐘     | 5 分鐘     |
|                                                                       | 過時軟體與外掛                   | 45 分鐘     | 10 分鐘    |
| <mark style="color:purple;">**CPTS（企業內部測試與紅隊）**</mark>                | AD 內部網路滲透                 | 90 分鐘     | 15 分鐘    |
|                                                                       | Kerberoasting 攻擊          | 60 分鐘     | 15 分鐘    |
|                                                                       | Lateral Movement（橫向移動）    | 75 分鐘     | 15 分鐘    |
|                                                                       | Active Directory 權限提升     | 90 分鐘     | 20 分鐘    |
|                                                                       | 零信任環境繞過                   | 60 分鐘     | 15 分鐘    |
|                                                                       | 雙因素驗證繞過                   | 50 分鐘     | 10 分鐘    |

## CTF 全面漏洞發現 Check-list

{% tabs %}
{% tab title="URL 參數" %}
1. SQL injection
2. LFI
3. IDOR
4. SSTi
{% endtab %}

{% tab title="表單" %}
1. SQL injection
2. XXE
3. CSRF
{% endtab %}

{% tab title="搜尋框 " %}
1. Sql inject&#x20;
2. SSTI
3. XSS
{% endtab %}

{% tab title="login" %}
1. Http Verb Tampering
2. Sql injection
3. 弱口令測試 `admin/admin`、`admin/123456`
4. 密碼重設流程檢查
5. Default Password&#x20;
{% endtab %}

{% tab title="文件上傳" %}
1. **XXE**
2. LFI
3. File upload
4. 上傳PHP、ASPX或 .htaccess&#x20;
{% endtab %}

{% tab title="Api" %}
1. SQLi
2. XXE
3. IDOR
4. Http Verb Tampering
{% endtab %}

{% tab title="留言" %}
1. sqlinject
2. XSS
3. SSTI
{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="JS 文件" %}
* 查看前端 JavaScript 檔案，有時會洩露 API key 或 debug 信息
* 觀察有冇 hardcode 嘅密碼或開發路徑
{% endtab %}

{% tab title="隱藏路徑 " %}
* `/admin`
* `/backup.zip`
* `/old/`
* `.git/`
* 用 `robots.txt` 搵有冇敏感路徑
{% endtab %}

{% tab title="Header" %}
Http Verb Tampering
{% endtab %}

{% tab title="Cookies" %}
1. IDOR


{% endtab %}
{% endtabs %}











## 解決模組問題的良好藍圖

<table data-header-hidden><thead><tr><th width="40"></th><th></th></tr></thead><tbody><tr><td></td><td> <strong>任務</strong></td></tr><tr><td>1.</td><td> 閱讀模組</td></tr><tr><td>2.</td><td>練習</td></tr><tr><td>3.</td><td>完成模組</td></tr><tr><td>4.</td><td>從頭開始模組練習</td></tr><tr><td>5.</td><td>再次做練習時，做筆記</td></tr><tr><td>6.</td><td>Create technical documentation based on the notes</td></tr><tr><td>7.</td><td>根據筆記建立非技術文檔</td></tr></tbody></table>

## 解決退役的機器問題的良好藍圖

<table data-header-hidden><thead><tr><th width="40"></th><th></th></tr></thead><tbody><tr><td></td><td><strong>Task  任務</strong></td></tr><tr><td>1.</td><td>自行取得用戶標誌</td></tr><tr><td>2.</td><td>自行取得 root 標誌</td></tr><tr><td>3.</td><td>撰寫技術文檔</td></tr><tr><td>4.</td><td>編寫非技術文檔</td></tr><tr><td>5.</td><td>將你的筆記與官方文章（或社群文章，如果你沒有 VIP 訂閱）進行比較</td></tr><tr><td>6.</td><td>創建你錯過的資訊列表</td></tr><tr><td>7.</td><td>觀看<a href="https://www.youtube.com/channel/UCa6eh7gCkpPo5XXUDfygQQA">Ippsec 的</a>演練並將其與您的筆記進行比較</td></tr><tr><td>8.</td><td>透過添加遺漏的部分來擴展你的筆記和文檔</td></tr></tbody></table>

## 解決退役的機器問題的良好藍圖

這種方法的優點是我們使用我們不熟悉且無法找到文件的單一主機（黑盒方法）來模擬盡可能真實的情況。只要機器保持活躍，就不會發布任何官方文章。這意味著我們無法從任何官方來源檢查我們是否擁有所有內容或是否遺漏了某些內容。這使我們處於依靠自己和自己的能力的境地。主動機器的理想練習步驟如下：

<table data-header-hidden><thead><tr><th width="40"></th><th></th></tr></thead><tbody><tr><td></td><td><strong>Task  任務</strong></td></tr><tr><td>1.</td><td>取得使用者和 root 標誌</td></tr><tr><td>2.</td><td>撰寫技術文檔</td></tr><tr><td>3.</td><td>編寫非技術文檔</td></tr><tr><td>4.</td><td>讓技術和非技術人員校對</td></tr></tbody></table>
