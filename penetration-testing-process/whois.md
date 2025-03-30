# Whois

### &#x20;使用 WHOIS

在使用`whois`命令之前，您需要確保它已安裝在您的 Linux 系統上。它是一個可透過 Linux 套件管理器使用的實用程序，如果尚未安裝，可以使用以下命令進行安裝

```shell-session
PikachuN@htb[/htb]$ sudo apt update
PikachuN@htb[/htb]$ sudo apt install whois -y
```

```bash
$ whois 54.164.117.196
```

```bash
$ whois example.com
```

## &#x20;下一個 Whois 使用者介面

```
docker run -d -p 3000:3000 programzmh/next-whois-ui
```

{% embed url="https://github.com/zmh-program/next-whois-ui/blob/main/README_TW.md" %}

1. ✨ **美觀界麵**：採用現代簡約設計的 [Shadcn UI](https://ui.shadcn.com/) 風格。
2. 📱 **響應式設計**：適配手機端✅ / Pad✅ / 桌麵端✅，並支持 PWA 應用。
3. 🌈 **多主題支持**：支持亮/暗色切換，自動檢測繫統主題。
4. 🚀 **靈活查詢**：基於 Next.js，支持無服務器部署，更快查詢速度。
5. 📚 **曆史記錄**：曆史記錄存儲在本地存儲中，方便查看和查詢曆史。
6. 📡 **開放接口**：提供簡單的 whois 查詢 API，易於與其他服務集成。
7. 🌍 **強大支持**：支持 IPv4、IPv6、域名、ASN、CIDR 的 Whois 查詢。
8. 📦 **結果分享**：支持獲取 Whois 查詢結果，方便分享和保存。
9. 📡 **結果緩存**：支持基於 Redis 的 Whois 緩存，提昇查詢速度。
10. 🌍 \[計劃] **國際化**：支持多語言 ([#6](https://github.com/zmh-program/next-whois-ui/issues/6))
