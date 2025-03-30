# Web Fuzzing

## **常用指令**

{% stepper %}
{% step %}
## **基本目錄模糊測試**

```
ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -u http://IP:PORT/FUZZ
```
{% endstep %}

{% step %}
## 檢查 robots.txt

```
curl http://yourdoman.com/robots.txt
```
{% endstep %}

{% step %}
## **GET 參數測試**

```
wenum -w /usr/share/seclists/Discovery/Web-Content/common.txt --hc 404 -u "http://IP:PORT/get.php?x=FUZZ"
```
{% endstep %}

{% step %}
## **POST 參數測試**

```
ffuf -u http://IP:PORT/post.php -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "y=FUZZ" -w /usr/share/seclists/Discovery/Web-Content/common.txt -mc 200 -v
```
{% endstep %}

{% step %}
## **Web API**

```
python3 api_fuzzer.py http://IP:PORT
```
{% endstep %}
{% endstepper %}



***

## **1.ffuf 備用**

*   **基本目錄模糊測試**

    ```bash
    ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -u http://IP:PORT/FUZZ
    ```
*   **包含特定副檔名的模糊測試**

    ```bash
    bffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt -u http://IP:PORT/FUZZ -e .php,.html,.txt,.bak,.js -v
    ```
* **遞歸模糊測試**
* ```
  ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -u http://IP:PORT/FUZZ -e .html -recursion -recursion-depth 2 -rate 500
  ```
* **Web API**
* ```
  PikachuN@htb[/htb]$ git clone https://github.com/PandaSt0rm/webfuzz_api.git
  PikachuN@htb[/htb]$ cd webfuzz_api
  PikachuN@htb[/htb]$ pip3 install -r requirements.txt
  PikachuN@htb[/htb]$ python3 api_fuzzer.py http://IP:PORT
  ```

#### **2. 參數模糊測試（Parameter Fuzzing）**



* 測試 GET/POST 參數，找出可能觸發特別回應的輸入值
* 嘗試發掘潛在漏洞，如 SQL Injection、LFI、XSS 等

## **GET 參數測試**

*   **手動測試**

    ```bash
    curl http://IP:PORT/get.php?x=1
    ```
*   **自動模糊測試**

    ```bash
    wenum -w /usr/share/seclists/Discovery/Web-Content/common.txt --hc 404 -u "http://IP:PORT/get.php?x=FUZZ"
    ```

## **POST 參數測試**

*   **手動測試**

    ```bash
    curl -d "y=1" http://IP:PORT/post.php
    ```
*   **自動模糊測試**

    ```bash
    ffuf -u http://IP:PORT/post.php -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "y=FUZZ" -w /usr/share/seclists/Discovery/Web-Content/common.txt -mc 200 -v
    ```

***

#### **3. 進階控制選項**

| 參數                     | 功能                          |
| ---------------------- | --------------------------- |
| `-w <wordlist>`        | 指定使用的字典                     |
| `-u <URL>`             | 目標 URL                      |
| `-e <extensions>`      | 指定副檔名                       |
| `-X <method>`          | 指定 HTTP 方法 (`GET`、`POST` 等) |
| `-d <data>`            | POST 請求的數據                  |
| `-H <header>`          | 添加請求標頭                      |
| `-mc <code>`           | 僅顯示特定回應狀態碼的結果               |
| `-recursion`           | 遞歸掃描目錄                      |
| `-recursion-depth <N>` | 設定遞歸深度                      |
| `-rate <N>`            | 控制請求速率，防止伺服器過載              |
| `--hc 404`             | 隱藏 404 回應                   |

用於模糊測試 Web 目錄和文件的最常用單字清單`SecLists`是：

<table data-header-hidden><thead><tr><th width="179.515625"></th><th></th><th></th></tr></thead><tbody><tr><td><strong>字典名稱</strong></td><td><strong>用途</strong></td><td><strong>適用情境</strong></td></tr><tr><td><code>Discovery/Web-Content/common.txt</code></td><td>常見目錄與檔案名稱</td><td>初步掃描，快速獲取有價值結果</td></tr><tr><td><code>Discovery/Web-Content/directory-list-2.3-medium.txt</code></td><td>目錄名稱專用字典</td><td>進一步探索潛在目錄</td></tr><tr><td><code>Discovery/Web-Content/raft-large-directories.txt</code></td><td>來自多個來源的目錄名大集合</td><td>進行深度模糊測試</td></tr><tr><td><code>Discovery/Web-Content/big.txt</code></td><td>大量目錄與檔案名稱</td><td>廣泛掃描，尋找所有可能性</td></tr></tbody></table>
