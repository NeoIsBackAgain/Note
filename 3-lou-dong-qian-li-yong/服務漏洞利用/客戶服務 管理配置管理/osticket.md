---
description: >-
  osTicket是一個開源支援票務系統。它可以與 Jira、OTRS、Request Tracker 和 Spiceworks 等系統進行比較。
  osTicket 可以將來自電子郵件、電話和基於網路的表單的使用者查詢整合到網路介面。 osTicket 是用 PHP 寫的，並使用 MySQL
  後端。它可以安裝在 Windows 或 Linux 上。儘管關於 osTicket 的市場資訊並不多，但用
---

# osTicket



<details>

<summary>攻擊流程總結</summary>

1️⃣ DNS 枚舉 + EyeWitness 發現 osTicket\
2️⃣ 嘗試登陸（用 email or 從 dehashed 泄露帳密）\
3️⃣ 瀏覽 ticket，獲取敏感內部資料\
4️⃣ 使用 ticket 洩露資料註冊其他系統 / 拿 API Token\
5️⃣ 如果有 VPN / Internal Portal 密碼，登入滲透\
6️⃣ 找機會提權，直攻 Active Directory

</details>



## <mark style="color:red;">**1. 發現點**</mark>

* **Nmap / EyeWitness** 可以掃出 osTicket：
  * 特徵：有 `OSTSESSID` cookie
  * 頁腳出現「powered by osTicket」 或「Support Ticket System」
* DNS / 子網域掃描結果：

```
support.inlanefreight.local
vpn.inlanefreight.local
```

* 發現支援系統通常都係企業重要資訊入手點！



## <mark style="color:red;">**2. 測試Payload**</mark>

* exploit-db 有紀錄：
  * **RFI (Remote File Inclusion)**
  * **SQL Injection**
  * **任意檔案上傳**
  * **XSS**

> 如果系統版本過舊，可以試 SQLi 或透過上傳 WebShell 拎 Shell

* 但如果系統好新，主要目標就係：\
  &#xNAN;**「利用票務系統洩露公司電郵地址」**

## <mark style="color:red;">3.   osTicket 利用方法（非漏洞性滲透）</mark>

#### 🎯 利用「公司支援信箱」收件功能

* 公司有公開支援信箱：`support@inlanefreight.local`
* 發送驗證 Email 到該信箱，然後透過 Ticket 系統查信件內容取得：
  * 註冊碼
  * 重設密碼連結
  * 甚至 API 金鑰

👉 目標係幫助滲透進入公司其他服務：

* GitLab / GitHub Enterprise
* Slack / Mattermost
* VPN / Internal Web Portal

\


## <mark style="color:red;">4.</mark> osTicket — 敏感資料洩漏範例

\
[https://github.com/sm00v/Dehashed](https://github.com/sm00v/Dehashed)

* 透過 **dehashed** 收集資料：

```
email: kevin@inlanefreight.local
username: kgrimes
password: Fish1ng_s3ason!
```

* 登入 `support.inlanefreight.local`
* 雖然帳號密碼唔 Work，但用 Email 嘗試 kevin@inlanefreight.local 登入成功！
* 進入介面：
  * 查封閉票據
  * 找內部聯繫、AD 用戶清單
  * 有時票據會有 VPN 憑證 / Password reset token











## <mark style="color:red;">5. 連鎖漏洞</mark>

| 階段                      | 動作                                                    |
| ----------------------- | ----------------------------------------------------- |
| 進入 osTicket 系統          | 檢查所有票據（open/closed），特別留意 reset links、VPN 憑證、API 金鑰    |
| 如果有 GitLab / Slack 註冊連結 | 嘗試使用支援信箱收確認郵件，取得 token 註冊進入 GitLab / Slack            |
| 如果票據裡有 VPN 設定資訊         | 直接登入 VPN，進行內部橫向滲透                                     |
| 收集 AD 使用者清單             | 找有無明文帳密或內部服務 URL                                      |
| 嘗試橫向攻擊                  | 用已取得帳密爆破 RDP、SMB、WinRM 或 GitLab、Jira、Wiki 等企業內部系統     |
| 最終目標                    | 找到 AD Domain Admin 帳號、提權成為 Domain Admin，或 Dump 全域帳號憑證 |

\
