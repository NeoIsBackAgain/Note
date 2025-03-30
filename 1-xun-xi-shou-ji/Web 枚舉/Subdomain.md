  

## **1️⃣ 找到 `subdomains-top1million-110000.txt`**

  

```bash

list=$(sudo find / -iname subdomains-top1million-110000.txt 2>/dev/null)

```

  

📌 **說明：**

  

* 使用 `find` 命令在整個系統 (`/`) 搜索 `subdomains-top1million-110000.txt` 文件

* `2>/dev/null`：避免錯誤訊息顯示

  

***

  

## **2️⃣ 使用 `dnsenum` 進行 DNS 枚舉**

  

```bash

dnsenum --enum inlanefreight.com -f $list -r

```

  

📌 **說明：**

  

* `--enum`：開啟所有可能的 DNS 枚舉方式

* `-f $list`：提供子域名字典 (`subdomains-top1million-110000.txt`)

* `-r`：執行反向查找 (Reverse Lookup)

  

***

  

## **3️⃣ 使用 `Gobuster` 搜索虛擬主機 (VHOST)**

  

```bash

gobuster vhost -u http://inlanefreight.htb:81 -w $list --append-domain

```

  

📌 **說明：**

  

* `vhost`：暴力破解虛擬主機 (VHOST)

* `-u`：指定目標網址 (`http://inlanefreight.htb:81`)

* `-w $list`：使用 `subdomains-top1million-110000.txt` 進行爆破

* `--append-domain`：自動在字典中每個子域名後面追加 `inlanefreight.htb`

  
  
  

在發現了子域名後，為了方便存取，可以將它們添加到 `/etc/hosts` 文件中。這

  

#### **- 手動編輯 `/etc/hosts`**

  

```bash

sudo vim /etc/hosts

```

  

📌 **在文件底部添加：**

  

```

10.129.201.50 sub1.inlanefreight.com

10.129.201.50 sub2.inlanefreight.com

10.129.201.50 sub3.inlanefreight.com

```

  

✅ :wq

  

***

  

#### &#x20;**- 測試解析**

  

```bash

ping -c 3 sub1.inlanefreight.com

```

  

**如果成功解析，說明 `/etc/hosts` 配置成功！🎯** 🚀

  

***

  

## **4️⃣ 使用 `crt.sh` 查詢 SSL/TLS 証書中的子域名**

  

```bash

curl -s "https://crt.sh/?q=/example.com&output=json" | jq -r '.[].name_value' | sort -u | while read -r domain; do

status_code=$(curl -o /dev/null -s -w "%{http_code}" "https://$domain")

if [[ "$status_code" -eq 200 ]]; then

echo -e "\e[32m$domain - response: $status_code\e[0m"

elif [[ "$status_code" -eq 400 ]] || [[ "$status_code" -eq 000 ]]; then

echo "$domain - response: $status_code"

else

echo -e "\e[33m$domain - response: $status_code\e[0m"

fi

done

```

  

📌 **說明：**

  

1. `curl -s "https://crt.sh/?q=/example.com&output=json"`\

🔹 查詢 `crt.sh`，獲取 `example.com` 的所有 SSL/TLS 証書子域名

2. `jq -r '.[].name_value' | sort -u`\

🔹 使用 `jq` 解析 JSON，提取所有 `name_value`，並去重

3. `while read -r domain; do ... done`\

🔹 遍歷每個子域名，使用 `curl` 測試 HTTP 回應狀態碼

4. 根據 `HTTP Code` 分類輸出：

* **🟢 200 (成功響應)** ✅

* **🟠 其他狀態碼** ⚠️

* **🔴 400/000 (無效)** ❌

  

***

  

#### **🔗 5️⃣ 進一步攻擊思路**

  

✅ **找到有效的子域名後，可以嘗試：**

  

* 使用 **`nmap`** 掃描端口：

  

```bash

nmap -p- -sV -sC inlanefreight.com

```

* 使用 **`ffuf`** 尋找隱藏目錄：

  

```bash

ffuf -u https://inlanefreight.com/FUZZ -w /usr/share/wordlists/dirb/common.txt

```

* 嘗試 **子域接管 (Subdomain Takeover)**：

  

```bash

host subdomain.inlanefreight.com

```