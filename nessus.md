# Nessus

## 漏洞掃描

#### **步驟 1：克隆 Nessus-Scanner 倉庫**

首先，拉取 GitHub 上的 **nessus-scanner** 專案：

```bash
git clone https://github.com/ciro-mota/nessus-scanner.git
cd nessus-scanner
```

***

#### **步驟 2：構建 Nessus Docker 映像**

進入倉庫目錄後，執行以下命令來構建 Docker 映像：

```bash
docker build -t nessus-scanner .
```

這會根據 `Dockerfile` 下載 Nessus 並安裝到 Docker 容器中。

***

#### **步驟 3：運行 Nessus 容器**

構建完成後，使用以下命令來啟動 Nessus：

```bash
docker run -d --name nessus -p 8834:8834 nessus-scanner
```

這裡：

* `-d` 讓容器在後台運行。
* `--name nessus` 給容器命名為 `nessus`。
* `-p 8834:8834` 讓你可以通過 **https://localhost:8834** 訪問 Nessus。

***

#### **步驟 4：訪問 Nessus Web 界面**

等待幾分鐘後，打開瀏覽器，訪問：

```
https://localhost:8834
```

如果 Nessus 運行在遠程伺服器，你需要用它的 IP，例如：

```
https://<your-server-ip>:8834
```

第一次登錄時，你需要創建一個帳戶，然後輸入 **Tenable Nessus 激活碼**（可免費註冊 Tenable 社區版）。

***

#### **步驟 5：檢查容器狀態**

確保 Nessus 正常運行：

```bash
docker ps
```

或者：

```bash
docker logs -f nessus
```

如果 Nessus 服務沒有運行，可以手動啟動：

```bash
docker start nessus
```

***

#### **步驟 6：使用 Nessus API 進行漏洞掃描**

這個專案包含了一個 `scan.py` 腳本，你可以使用它來與 Nessus API 交互：

```bash
python3 scan.py --target <your-target-ip>
```

這將會觸發一次 Nessus 掃描。

***

#### **結論**

這個 Docker 化的 Nessus 版本讓部署變得更加簡單，總結：

1. **克隆倉庫** ➝ `git clone`
2. **構建映像** ➝ `docker build`
3. **運行容器** ➝ `docker run`
4. **訪問 Web 界面** ➝ `https://localhost:8834`
5. **可選：使用 API 進行掃描** ➝ `scan.py`

### Scan Policies  掃描策略

Nessus 為我們提供了建立掃描策略的選項。本質上，這些都是自訂的掃描，允許我們定義特定的掃描選項，保存策略配置，並在建立新掃描時在`Scan Templates`下提供它們。這使我們能夠為任意數量的場景建立有針對性的掃描，例如速度較慢、更規避性的掃描、以 Web 為中心的掃描，或使用一組或多組憑證針對特定用戶端的掃描。掃描策略可以從其他 Nessus 掃描器匯入，也可以匯出以便稍後匯入到另一個 Nessus 掃描器。

要建立掃描策略，我們可以點擊右上角的`New Policy`按鈕，然後我們將看到預先配置的掃描清單。我們可以選擇一個掃描，例如`Basic Network Scan` ，然後自訂它，或者我們可以建立自己的掃描。我們將選擇`Advanced Scan`來建立完全自訂的掃描，其中沒有內建預先配置的建議。

\


{% embed url="https://docs.tenable.com/nessus/Content/Plugins.htm" %}

### Nessus Plugins  Nessus 插件

\
Nessus 可與使用[Nessus 攻擊腳本語言 (NASL)](https://en.wikipedia.org/wiki/Nessus_Attack_Scripting_Language)編寫的插件配合使用，並可針對新的漏洞和 CVE。這些插件包含漏洞名稱、影響、補救措施以及測試特定問題存在的方法等資訊。

\
插件依嚴重性等級評定： `Critical` 、 `High` 、 `Medium` 、 `Low` 、 `Info` 。在撰寫本文時，Tenable 已發布了`145,973`插件，涵蓋`58,391` CVE ID 和`30,696` [Bugtraq](https://en.wikipedia.org/wiki/Bugtraq) ID。 [Tenable 網站](https://www.tenable.com/plugins)上有一個可搜尋的資料庫，其中包含所有已發佈的插件。

\
Exporting Nessus Scans  匯出 Nessus 掃描

\
可以使用[nessus-report-downloader](https://raw.githubusercontent.com/eelsivart/nessus-report-downloader/master/nessus6-report-downloader.rb)等腳本透過 Nessus REST API 從 CLI 快速下載所有可用格式的掃描結果：\
使用 Nessus 掃描輸出

```shell-session
PikachuN@htb[/htb]$ ./nessus_downloader.rb 

Nessus 6 Report Downloader 1.0

Enter the Nessus Server IP: 127.0.0.1
Enter the Nessus Server Port [8834]: 8834
Enter your Nessus Username: admin
Enter your Nessus Password (will not echo): 

Getting report list...
Scan ID Name                                               Last Modified                  Status         
------- ----                                               -------------                  ------         
1     Windows_basic                                Aug 22, 2020 22:07 +00:00      completed      
         
Enter the report(s) your want to download (comma separate list) or 'all': 1

Choose File Type(s) to Download: 
[0] Nessus (No chapter selection)
[1] HTML
[2] PDF
[3] CSV (No chapter selection)
[4] DB (No chapter selection)
Enter the file type(s) you want to download (comma separate list) or 'all': 3

Path to save reports to (without trailing slash): /assessment_data/inlanefreight/scans/nessus

Downloading report(s). Please wait...

[+] Exporting scan report, scan id: 1, type: csv
[+] Checking export status...
[+] Report ready for download...
[+] Downloading report to: /assessment_data/inlanefreight/scans/nessus/inlanefreight_basic_5y3hxp.csv

Report Download Completed!
```

\
我們還可以編寫自己的腳本來自動化許多 Nessus 功能。
