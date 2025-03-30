# Web 批量分配漏洞 ( Ruby on Rails)

#### **1️⃣ 發現點**

* **Ruby on Rails** 係一個常見會有 Mass Assignment 漏洞嘅 Web Framework。
* **發現方式：**
  * 檢查 API 或 Web 應用程式有冇批次更新用戶資料嘅功能
  * 留意 `user`、`account` 等 JSON 參數，睇下會唔會有隱藏欄位（例如 `admin: true`、`role: "superuser"`）
  * 係 Python / Flask / Django 亦可能有類似問題，特別係 `request.get_json()` 直接存入 ORM 嘅地方

***

#### **2️⃣ 測試 Payload**

**假設有以下 API**

```json
POST /update_user
{
    "user": {
        "username": "hacker",
        "email": "hacker@example.com",
        "admin": true
    }
}
```

**可能伺服器執行：**

```ruby
@user.update(params[:user])
```

* 如果 `update()` 直接接受 `params`，冇白名單保護，就可以 **偷偷加上 `admin: true`**，獲取管理員權限！

***

#### **3️⃣ 利用方式**

**攻擊方法** 1️⃣ **找到 API**

* 用 `Burp Suite` 攔截請求，查看是否可以 `POST / PATCH / PUT` 更新用戶資料
* 嘗試修改 JSON 內嘅 `admin`、`role`、`is_superuser`

2️⃣ **透過 SCP 抓取後端代碼**

* 你用以下指令從目標機器抓 `app.py`，並用 VS Code 查看：

```bash
scp root@10.129.205.15:/opt/asset-manager/app.py .
code app.py &
```

* 檢查 `app.py` 內是否有 **`active`** 參數可以利用

3️⃣ **嘗試修改 `active` 參數**

* 假設 `app.py` 內有：

```python
if request.json["active"]:
    login_user()
```

* 你可以發送：

```json
{
    "username": "hacker",
    "password": "test",
    "active": true
}
```

* **成功繞過登入！**

***

#### **5️⃣ 連鎖漏洞 (Chained Exploitation)**

如果 Mass Assignment 成功，下一步可以： ✅ **橫向移動 (Privilege Escalation)**

* 變成 `admin` 之後，試下可以開 `user list`、改密碼、加 SSH Key

✅ **與 XSS / IDOR 結合**

* 如果 API 允許你修改其他用戶資料，可以試 `IDOR` 變更其他帳號
* 如果可以改 `email`，可能可以配合 `Password Reset` 攻擊

✅ **寫 Shell / 提權**

* 如果 `app.py` 允許 `role=admin` 存取某個 `upload.php`，你可以嘗試上傳 Webshell
