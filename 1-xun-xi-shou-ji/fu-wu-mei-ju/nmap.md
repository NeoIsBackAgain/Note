# Nmap

{% embed url="https://nmap.org/book/man-port-scanning-techniques.html" %}
身為汽車維修新手，我可能需要花數小時的時間嘗試使用基本的工具（鐵鎚、膠帶、扳手等）來完成手邊的任務。當我徹底失敗並把我的破車拖到真正的機械師那裡時，他總會在一個巨大的工具箱裡翻找，直到拿出一個完美的小玩意，使這項工作看起來毫不費力。連接埠掃描的技術也類似。專家了解數十種掃描技術，並根據特定任務選擇合適的技術（或組合）。缺乏經驗的使用者和腳本小子， 另一方面 另一方面，嘗試用預設的 SYN 掃描解決每個問題。由於 Nmap 免費，掌握連接埠掃描的唯一障礙就是知識。那 當然比汽車行業要好，因為汽車行業可能需要很高的技能才能 確定你需要一個支柱彈簧壓縮機，那麼你仍然 必須為此付出數千美元。
{% endembed %}



## (1) --> 快速掃描   100 個連接埠

```sh
nmap -T4 -F <目標IP>
```

## (2) --> 特定連接埠掃描

```sh
sudo nmap -p 25 --script vuln,smtp-commands -sC -sV -A -O <目標IP>
```

## (3) -- > 進階全能掃描

```sh
nmap -p- -A -T4 -sC -sV <目標IP>
```



##

## 超強無聲掃描

如果你擔心被防火牆或IDS偵測，可以用「隱形掃描」：

```sh
nmap -p- -A -T3 --min-rate=1000 -sS -Pn <目標IP>
```

## **掃描網路範圍**

```sh
sudo nmap 10.129.2.0/24 -sn -oA tnet | grep for | cut -d" " -f5
```

## &#x20;掃描多個 IP

```sh
sudo nmap -sn -oA tnet 10.129.2.18 10.129.2.19 10.129.2.20| grep for | cut -d" " -f5
```

```sh
sudo nmap 10.129.2.28 -Pn -n --disable-arp-ping --packet-trace -p 445 --reason  -sV
```

***

{% tabs %}
{% tab title="-sS" %}
(TCP SYN 掃描）



SYN 掃描是預設的和最受歡迎的掃描選項，這是有原因的。它可以快速執行，在不受限制性防火牆阻礙的快速網路上每秒掃描數千個連接埠。由於它從不完成 TCP 連接，因此它也相對不引人注目且隱密。 SYN 掃描可針對任何相容的 TCP 堆疊進行工作，而不是像 Nmap 的 FIN/NULL/Xmas、Maimon 和空閒掃描那樣依賴特定平台的特性。它還可以清晰、可靠地區分`open` 、 `closed`並`filtered` 州。





這種技術通常被稱為半開掃描，因為您沒有打開完整的 TCP 連線。您發送一個 SYN 資料包，就好像要打開一個真正的連接，然後等待回應。 SYN/ACK 表示連接埠正在監聽（開啟），而 RST（重設）表示非監聽。如果多次重傳後仍未收到回應，則該連接埠被標記為已過濾。如果收到 ICMP 不可達錯誤（類型 3，代碼 0、1、2、3、9、10 或 13），則該連接埠也會被標記為過濾。如果收到回應的 SYN 封包（沒有 ACK 標誌），則該連接埠也被視為開放。這可能是由於一種極為罕見的 TCP 功能（稱為同時開啟或分割握手連線）造成的（請參閱[ `https://nmap.org/misc/split-handshake.pdf` ](https://nmap.org/misc/split-handshake.pdf)）。

\

{% endtab %}

{% tab title="-sT" %}
(TCP 連線掃描）

當 SYN 掃描不可選時，TCP 連線掃描是預設的 TCP 掃描類型。當使用者沒有原始資料包權限時就會出現這種情況。 Nmap 並不像大多數其他掃描類型那樣寫入原始資料包，而是透過發出`connect`系統呼叫來要求底層作業系統與目標機器和連接埠建立連接。這是 Web 瀏覽器、P2P 用戶端和大多數其他支援網路的應用程式用於建立連接的相同的高級系統呼叫。它是稱為 Berkeley Sockets API 的程式設計介面的一部分。 Nmap 不會讀取線路上的原始資料包回應，而是使用此 API 來取得每次連線嘗試的狀態資訊。

\
當 SYN 掃描可用時，它通常是一個更好的選擇。與原始資料包相比，Nmap 對高階`connect`呼叫的控制較少，因此效率較低。系統呼叫完成與開放目標連接埠的連接，而不是執行 SYN 掃描所做的半開放重置。這不僅需要更長的時間並且需要更多的資料包來獲取相同的信息，而且目標機器更有可能記錄連接。一個好的 IDS 可以捕捉這兩種情況，但是大多數機器沒有這樣的警報系統。當 Nmap 連接然後關閉連接而不發送資料時，普通 Unix 系統上的許多服務都會向系統日誌添加一條註釋，有時還會添加一條神秘的錯誤訊息。當這種情況發生時，服務確實會崩潰，儘管這種情況並不常見。如果管理員在其日誌中看到來自單一系統的大量連線嘗試，就應該知道她已經被連線掃描了。

\

{% endtab %}

{% tab title="-sU" %}
（UDP 掃描）

雖然網路上大多數流行的服務都是透過 TCP 協定運行的，但[UDP](http://www.rfc-editor.org/rfc/rfc768.txt)服務也被廣泛部署。 DNS、SNMP 和 DHCP（註冊連接埠 53、161/162 和 67/68）是最常見的三種。由於 UDP 掃描通常比 TCP 更慢且更困難，因此一些安全審計員會忽略這些連接埠。這是一個錯誤，因為可利用的 UDP 服務非常常見，攻擊者當然不會忽略整個協定。幸運的是，Nmap 可以幫助清點 UDP 連接埠。

\
使用`-sU`選項啟動 UDP 掃描。它可以與 TCP 掃描類型（如 SYN 掃描（ `-sS` ））結合使用，以便在相同運行期間檢查兩種協定。

\
UDP 掃描透過向每個目標連接埠發送 UDP 封包來運作。對於一些常見端口（如 53 和 161），會發送特定於協議的有效負載以提高響應率，但對於大多數端口，除非`--data` ，否則數據包為空。 `--data-string`或`--data-length` 已指定選項。 如果發生 ICMP 連接埠不可達錯誤（類型 3，代碼 3）， 返回後，連接埠已`closed` 。其他 ICMP 不可達錯誤（類型 3，代碼 0、1、2、9、10 或 13）將連接埠標記為`filtered` 。有時，服務會以 UDP 封包回應，證明它是`open` 。如果重新傳輸後仍未收到回應，則該連接埠被歸類為`open|filtered` 。這意味著連接埠可能處於開啟狀態，或者封包過濾器可能阻止了通訊。版本偵測（ `-sV` ）可用於協助區分真正開放的連接埠和被過濾的連接埠。

\
UDP 掃描的一大挑戰是快速完成。開放和過濾的連接埠很少發送任何回應，導致 Nmap 逾時然後進行重新傳輸，以防探測或回應遺失。關閉的連接埠往往會帶來更大的問題。它們通常會發回 ICMP 連接埠不可達錯誤。但與關閉的 TCP 連接埠為回應 SYN 或連線掃描而傳送的 RST 封包不同，許多主機預設會對ICMP 連接埠不可達訊息的速率進行限制。 Linux 和 Solaris 對此尤其嚴格。例如，Linux 2.4.20 核心將目標不可達訊息限制為每秒一條（在`net/ipv4/icmp.c`中）。

\
Nmap 偵測速率限制並相應地減慢速度，以避免網路充斥目標機器將丟棄的無用資料包。不幸的是，Linux 每秒一個資料包的限制使 65,536 個連接埠的掃描需要超過 18 個小時。加快 UDP 掃描速度的想法包括並行掃描更多主機、首先對熱門連接埠進行快速掃描、從防火牆後面掃描以及使用`--host-timeout`跳過速度慢的主機。

\

{% endtab %}

{% tab title="-sY" %}
（SCTP INIT 掃描）

[連續傳輸協定](http://www.rfc-editor.org/rfc/rfc4960.txt) 是 TCP 和 UDP 協定的一個相對較新的替代方案， 結合了 TCP 和 UDP 的大部分特性，並添加了 多宿主和多流等新功能。它主要是 用於 SS7/SIGTRAN 相關服務，但具有潛力 也可用於其他應用程式。 SCTP INIT 掃描是 SCTP 中與 TCP SYN 掃描等效的掃描。 它可以快速執行，每次掃描數千個端口 其次，在一個不受防火牆限制的快速網路上。 與 SYN 掃描類似，INIT 掃描相對不引人注目且隱秘， 因為它從未完成 SCTP 關聯。它還允許清晰地 可靠區分`open`的， `closed`並`filtered` 州。

\
這種技術通常被稱為半開掃描，因為您沒有開啟完整的 SCTP 關聯。您發送一個 INIT 區塊，就好像您要開啟一個真正的關聯，然後等待回應。 INIT-ACK 區塊表示連接埠正在監聽（開啟），而 ABORT 區塊表示非監聽者。如果多次重傳後仍未收到回應，則該連接埠被標記為已過濾。如果收到 ICMP 不可達錯誤（類型 3，代碼 0、1、2、3、9、10 或 13），則該連接埠也會被標記為過濾。

\

{% endtab %}

{% tab title="-sN" %}
（TCP NULL、FIN 和 Xmas 掃描）

這三種掃描類型（下一節將介紹使用`--scanflags`選項的掃描類型），利用[TCP RFC](http://www.rfc-editor.org/rfc/rfc793.txt)中的一個微妙漏洞來區分`open`和 `closed`連接埠。 RFC 793 第 65 頁指出「如果 \[目標] 連接埠狀態為 CLOSED... 那麼不包含 RST 的傳入段將導致發送 RST 作為回應。 」然後下一頁討論了發送到開放連接埠且未設定 SYN、RST 或 ACK 位元的封包，指出： 「您不太可能到達這裡，但如果您到達了，請丟棄該段並返回。 」

\
當掃描符合此 RFC 文字的系統時，如果連接埠關閉，則任何不包含 SYN、RST 或 ACK 位元的封包都會導致傳回 RST，如果連接埠打開，則根本不會有任何回應。只要不包含這三位中的任何一位，其他三個（FIN、PSH 和 URG）的任意組合都是可以的。 Nmap 利用三種掃描類型來利用這一點：

\
Null scan (`-sN`)\
空掃描（ `-sN` ）

Does not set any bits (TCP flag header is 0)\
不設定任何位元（TCP 標誌頭為 0）

FIN scan (`-sF`)\
FIN 掃描（ `-sF` ）

Sets just the TCP FIN bit.\
僅設定 TCP FIN 位元。

Xmas scan (`-sX`)\
聖誕節掃描 ( `-sX` )

Sets the FIN, PSH, and URG flags, lighting the packet up like a Christmas tree.\
設定 FIN、PSH 和 URG 標誌，讓資料包像聖誕樹一樣亮起來。
{% endtab %}

{% tab title="-sA" %}
(TCP ACK 掃描）

這種掃描不同於目前討論過的其他掃描，因為它從來不確定`open` （甚至 `open|filtered` ）連接埠。它用於映射防火牆規則集，確定它們是否有狀態以及哪些連接埠被過濾。

\

{% endtab %}

{% tab title="-sW" %}
（TCP 視窗掃描）



此掃描依賴少數人的實作細節 系統在網路上，所以你不能總是信任它。系統 不支援它通常會返回所有端口 `closed` 。當然，機器 確實沒有開放連接埠。如果大多數掃描的連接埠 如果某些連接埠號碼（例如 22、25、53） `closed` ，但一些常用連接埠號碼（例如 22、25、53）已`filtered` ，則系統很容易受到攻擊。有時，系統甚至會表現出完全相反的行為。如果您的掃描顯示 1,000 個開放端口和 3 個關閉或過濾的端口，那麼這三個端口很可能是真正開放的端口。

\
視窗掃描與 ACK 掃描完全相同，只是它 利用某些系統的實作細節來區分 從關閉的端口打開端口，而不是總是打印 當返回 RST 時， `unfiltered` 。它透過檢查傳回的 RST 封包的 TCP 視窗欄位來實現此目的。在某些系統上，開放埠使用正視窗大小（即使對於 RST 封包也是如此），而關閉連接埠的視窗為零。因此，當視窗掃描收到 RST 時，它不會始終將連接埠列為`unfiltered` ，而是將連接埠列為`open`或 如果該重設中的 TCP 視窗值為正或零，則`closed` 。

\

{% endtab %}

{% tab title="-sM" %}
（TCP Maimon 掃描）

Maimon 掃描以其發現者 Uriel Maimon 的名字命名。他&#x5728;_《Phrac&#x6B;_&#x96DC;誌》第 49 期（1996 年 11 月）中描述了這項技術。包含此項技術的 Nmap 在之後的兩個版本中發布。技術與 NULL、FIN 和 Xmas 掃描完全相同，只是探測是 FIN/ACK。根據[RFC 793](http://www.rfc-editor.org/rfc/rfc793.txt) （TCP），無論連接埠是開啟還是關閉，都應產生一個 RST 封包來回應此類探測。然而，Uriel 注意到，如果連接埠開放，許多 BSD 衍生系統就會直接丟棄封包。

\

{% endtab %}

{% tab title="-sZ" %}
（SCTP COOKIE ECHO 掃描）

\
SCTP COOKIE ECHO 掃描是一種更高階的 SCTP 掃描。它利用了這樣一個事實：SCTP 實作應該在開放連接埠上悄悄丟棄包含 COOKIE ECHO 區塊的資料包，但如果連接埠關閉則發送 ABORT。這種掃描類型的優點是，它不像 INIT 掃描那樣明顯是連接埠掃描。此外，可能存在非狀態防火牆規則集阻止 INIT 區塊，但不會阻止 COOKIE ECHO 區塊。不要誤以為這會使連接埠掃描變得不可見；好的 IDS 也能夠偵測 SCTP COOKIE ECHO 掃描。缺點是 SCTP COOKIE ECHO 掃描無法區分`open`端口和`filtered`端口，導致兩種情況下的狀態都是`open|filtered` 。

\

{% endtab %}

{% tab title="--scanflags " %}
(自訂 TCP 掃描）

真正高級的 Nmap 用戶不需要將自己局限於所提供的固定掃描類型。 `--scanflags`選項可讓您透過指定任意 TCP 標誌來設計自己的掃描。讓您的創造力源源不絕，同時逃避入侵偵測系統，其供應商只需翻閱 Nmap 手冊頁添加特定規則！

`--scanflags`參數可以是數字標誌值，例如 9（PSH 和 FIN），但使用符號名稱更簡單。只需將`URG`的任意組合混合在一起， `ACK` , `PSH` , `RST` 、 `SYN`和 `FIN` 。例如， `--scanflags URGACKPSHRSTSYNFIN` 設定所有內容，儘管它對於掃描來說不是很有用。指定這些的順序無關緊要。

\
除了指定所需的標誌之外，您還可以指定 TCP 掃描類型（例如`-sA`或`-sF` ）。 該基本類型告訴 Nmap 如何解釋回應。為了 例如，SYN 掃描認為無回應表示 `filtered`端口，而 FIN 掃描將其視為 `open|filtered` 。 Nmap 的行為與基本掃描類型相同，只是它將使用您指定的 TCP 標誌。如果您未指定基本類型，則使用 SYN 掃描。
{% endtab %}

{% tab title="-sI" %}
（空閒掃描）

這種先進的掃描方法可以對目標進行真正的盲 TCP 連接埠掃描（意味著不會從您的真實 IP 位址向目標發送任何封包）。相反，獨特的側通道攻擊利用殭屍主機上可預測的 IP 碎片 ID 序列產生來收集有關目標上開放連接埠的資訊。 IDS 系統將顯示來自您指定的殭屍機器（機器必須啟動並滿足某些條件）的掃描。這種有趣的掃描類型的完整詳細資訊位於[「TCP 空閒掃描（ `-sI` ）」部分](https://nmap.org/book/idlescan.html)。

\
除了極度隱蔽（由於其 盲目性），這種掃描類型允許映射 機器之間基於 IP 的信任關係。港口 列表顯示開放埠 _從殭屍宿主的角度來看。_&#x56E0;此，您可以嘗試使用您認為可能可信任的各種殭屍（透過路由器/封包過濾規則）掃描目標。

\
如果您希望偵測殭屍主機上某個特定連接埠的 IP ID 變化，您可以向殭屍主機新增冒號，後面接著連接埠號碼。否則，Nmap 將使用其預設使用的連接埠進行 TCP ping（80）。
{% endtab %}

{% tab title="-sO" %}
（IP 協定掃描)

IP 協定掃描可讓您確定哪些 IP 協定 （TCP、ICMP、IGMP 等）受目標機器支援。這不是 從技術上來說，這是一種連接埠掃描，因為它會循環使用 IP 協定號 而不是 TCP 或 UDP 連接埠號碼。但它仍然使用 `-p`選項選擇掃描的協定號，以正常連接埠表格式報告其結果，甚至使用與真正的連接埠掃描方法相同的底層掃描引擎。所以它足夠接近連接埠掃描，所以它屬於這裡。

\
協定掃描除了本身有用之外，還展示了開源軟體的強大功能。雖然基本想法很簡單，但我並沒有想到要添加它，也沒有收到任何有關此類功能的請求。然後在 2000 年夏天，Gerhard Rieger構思了這個想法，編寫了一個出色的補丁來實現它，並將其發送&#x5230;_&#x516C;&#x544A;_&#x90F5;件列表（當時稱&#x70BA;_&#x6E;map-hackers_ ）。我將該補丁合併到 Nmap 樹中並於第二天發布了新版本。很少有商業軟體擁有足夠熱情的使用者來設計和貢獻自己的改進！

\
協定掃描的工作方式與 UDP 掃描類似。反而 遍歷 UDP 封包的連接埠號碼字段，它會發送 IP 封包頭並遍歷八位元 IP 協定欄位。 標頭通常是空的，不包含任何數據，甚至不包含 所聲明協議的正確標頭。例外情況包括 TCP、 UDP、ICMP、SCTP 和 IGMP。包含適當的協議標頭，因為 有些系統不會發送它們，因為 Nmap 已經 函數來創建它們。無需監視 ICMP 端口 無法存取的訊息，協定掃描正在尋找 ICMP _協&#x8B70;_&#x4E0D;可達訊息。如果 Nmap 從目標主機收到任何協定的回應，Nmap 會將該協定標記為`open` 。 ICMP 協定不可達 錯誤（類型 3，代碼 2）導致協定被標記為 當連接埠不可達（類型 3，代碼 3）時，協定`closed` ，標誌著協定`open` 。其他 ICMP 不可達錯誤（類型 3，代碼 0、1、9、10 或 13）導致協議被標記 `filtered` （儘管他們證明 ICMP 是 同時`open` ）。如果沒有收到回覆 重傳後，協議被標記 `open|filtered`

\

{% endtab %}

{% tab title="-b" %}
(FTP 反彈掃描）

FTP 協定（ [RFC 959](http://www.rfc-editor.org/rfc/rfc959.txt) ）的一個有趣特性是支援所謂的代理 FTP 連線。這允許用戶連接到一個 FTP 伺服器，然後要求將檔案傳送到第三方伺服器。這樣的功能在許多層面上都很容易被濫用，因此大多數伺服器已經停止支援它。此功能允許的濫用之一是導致 FTP 伺服器對其他主機進行連接埠掃描。只需要求 FTP 伺服器依序向目標主機的每個感興趣的連接埠發送檔案。錯誤訊息會描述連接埠是否開放。這是一種繞過防火牆的好方法，因為組織的 FTP 伺服器通常放置在比任何舊的 Internet 主機更容易存取其他內部主機的地方。 Nmap 使用`-b`選項支援 FTP 反彈掃描。它需要一個論點 形式 _`<username>`_ : _`<password>`_ @ _`<server>`_ : _`<port>`_ 。 _`<Server>`_&#x662F; 存在漏洞的 FTP 伺服器。與普通 URL 一樣，你可以省略 _`<username>`_ : _`<password>`_ , 在這種情況下匿名登入憑證（使用者： `anonymous`密碼： `-wwwuser@` ) 被使用。連接埠號碼（和前面的冒號）可以省略，因為 那麼，在這種情況下， 已使&#x7528;_`<server>`_ 。

\

{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="-sV " %}
### 服務版本檢測

\
完整的連接埠掃描需要相當長的時間。要查看掃描狀態，我們可以在掃描過程中按`[Space Bar]` ，這將導致`Nmap`向我們顯示掃描狀態。

\
建議首先執行快速連接埠掃描，這將為我們提供有關可用連接埠的簡要概述。這會大大減少流量，這對我們來說是有利的，因為否則我們可能會被安全機制發現和阻止。我們可以先處理這些問題，並在背景執行連接埠掃描，顯示所有開放連接埠（ `-p-` ）。我們可以使用版本掃描來掃描特定連接埠的服務及其版本（ `-sV` ）。
{% endtab %}

{% tab title="-v / -vv " %}
我們還可以增加`verbosity level` （ `-v` / `-vv` ），當`Nmap`偵測到開放連接埠時，它將直接向我們顯示這些連接埠。
{% endtab %}

{% tab title="--O" %}
作業系統偵測
{% endtab %}

{% tab title="--traceroute" %}
追蹤路由
{% endtab %}

{% tab title="-A" %}
| 執行服務偵測、作業系統偵測、追蹤路由並使用預設腳本掃描目標。 |
| ------------------------------ |

\

{% endtab %}

{% tab title="-sA" %}
| 對指定連接埠執行 ACK 掃描。 |
| ---------------- |
|                  |

\

{% endtab %}

{% tab title="-sS	" %}
| 對指定連接埠執行 SYN 掃描。 |
| ---------------- |
|                  |

\

{% endtab %}

{% tab title="-Pn	" %}
| 禁用 ICMP Echo 請求。 |
| ---------------- |
|                  |

\

{% endtab %}

{% tab title="-n" %}
| Disables DNS resolution.  禁用 DNS 解析。 |
| ------------------------------------ |
|                                      |

\

{% endtab %}

{% tab title="--disable-arp-ping	" %}
| Disables ARP ping.  禁用 ARP ping。 |
| -------------------------------- |
|                                  |

\

{% endtab %}
{% endtabs %}

{% tabs %}
{% tab title="--source-port 53	" %}
| 從指定的來源連接埠執行掃描。 |
| -------------- |

\

{% endtab %}

{% tab title="-e tun0	" %}
| 透過指定的介面發送所有請求。 |
| -------------- |

\

{% endtab %}

{% tab title="-O	" %}
| 執行作業系統檢測掃描。 |
| ----------- |
|             |

\

{% endtab %}

{% tab title="-S" %}
| 使用不同的來源IP位址掃描目標。 |
| ---------------- |
|                  |

\

{% endtab %}

{% tab title=" -D " %}
存在管理員原則上阻止不同區域的特定子網路的情況。這將阻止對目標網路的任何存取。另一個例子是當 IPS 應該阻止我們時。因此，誘餌掃描方法（ `-D` ）是正確的選擇。透過這種方法，Nmap 會產生各種隨機 IP 位址插入 IP 頭中，以掩蓋發送的封包的來源。透過這種方法，我們可以隨機產生（ `RND` ）特定數量（例如： `5` ）的 IP 位址，並以冒號（ `:`分隔。然後，我們的真實 IP 位址將隨機放置在產生的 IP 位址之間。在下一個例子中，我們的真實 IP 位址因此被放在第二個位置。另一個關鍵點是誘餌必須是活的。否則，由於 SYN 泛洪安全機制，目標上的服務可能變得無法存取。

| `-D RND:5` | <p>Generates five random IP addresses that indicates the source IP the connection comes from.<br>產生五個隨機 IP 位址，指示連接來自的來源 IP。</p> |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------- |

\

{% endtab %}

{% tab title="-oA " %}
## Saving the Results  保存結果

我們也可以指定選項（ `-oA` ）以所有格式儲存結果。該指令可能如下所示：

```shell-session
PikachuN@htb[/htb]$ sudo nmap 10.129.2.28 -p- -oA target

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-16 12:14 CEST
Nmap scan report for 10.129.2.28
Host is up (0.0091s latency).
Not shown: 65525 closed ports
PORT      STATE SERVICE
22/tcp    open  ssh
25/tcp    open  smtp
80/tcp    open  http
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in 10.22 seconds
```
{% endtab %}
{% endtabs %}

## Nmap腳本引擎

```shell-session
sudo nmap 10.129.2.28 -p 25 --script banner,smtp-commands
```

```shell-session
sudo nmap 10.129.2.28 -p 80 -sV --script vuln 
```

| **類別**      | **描述**                                  |
| ----------- | --------------------------------------- |
| `auth`      | 確定身份驗證憑證。                               |
| `broadcast` | 透過廣播來發現主機的腳本以及發現的主機可以自動添加到剩餘的掃描中。       |
| `brute`     | 執行腳本，嘗試透過使用憑證進行暴力破解來登入相應的服務。            |
| `default`   | 使用該`-sC`選項執行的預設腳本。                      |
| `discovery` | 無障礙服務的評估。                               |
| `dos`       | 這些腳本用於檢查服務是否有拒絕服務漏洞，由於它會損害服務，因此使用較少。    |
| `exploit`   | 此類腳本嘗試利用掃描連接埠的已知漏洞。                     |
| `external`  | 使用外部服務進行進一步處理的腳本。                       |
| `fuzzer`    | 這使用腳本透過發送不同的欄位來識別漏洞和意外的資料包處理，這可能需要很長時間。 |
| `intrusive` | 可能對目標系統產生負面影響的侵入性腳本。                    |
| `malware`   | 檢查某些惡意軟體是否感染了目標系統。                      |
| `safe`      | 不執行侵入性和破壞性存取的防禦腳本。                      |
| `version`   | 服務檢測的擴展。                                |
| `vuln`      | 識別特定的漏洞。                                |

## Debug

**Tcpdump  傳輸控制包**

```shell-session
PikachuN@htb[/htb]$ sudo tcpdump -i eth0 host 10.10.14.2 and 10.129.2.28

tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
```

**Tcpdump – 攔截流量**

\
&#x20; Service Enumeration  服務枚舉

```shell-session
18:28:07.128564 IP 10.10.14.2.59618 > 10.129.2.28.smtp: Flags [S], seq 1798872233, win 65535, options [mss 1460,nop,wscale 6,nop,nop,TS val 331260178 ecr 0,sackOK,eol], length 0
18:28:07.255151 IP 10.129.2.28.smtp > 10.10.14.2.59618: Flags [S.], seq 1130574379, ack 1798872234, win 65160, options [mss 1460,sackOK,TS val 1800383922 ecr 331260178,nop,wscale 7], length 0
18:28:07.255281 IP 10.10.14.2.59618 > 10.129.2.28.smtp: Flags [.], ack 1, win 2058, options [nop,nop,TS val 331260304 ecr 1800383922], length 0
18:28:07.319306 IP 10.129.2.28.smtp > 10.10.14.2.59618: Flags [P.], seq 1:36, ack 1, win 510, options [nop,nop,TS val 1800383985 ecr 331260304], length 35: SMTP: 220 inlane ESMTP Postfix (Ubuntu)
18:28:07.319426 IP 10.10.14.2.59618 > 10.129.2.28.smtp: Flags [.], ack 36, win 2058, options [nop,nop,TS val 331260368 ecr 1800383985], length 0
```

The first three lines show us the three-way handshake.\
前三行向我們展示了三次握手。

<table><thead><tr><th width="48.21875"></th><th width="89.33984375"></th><th></th></tr></thead><tbody><tr><td>1.</td><td><code>[SYN]</code></td><td><code>18:28:07.128564 IP 10.10.14.2.59618 > 10.129.2.28.smtp: Flags [S], &#x3C;SNIP></code></td></tr><tr><td>2.</td><td><code>[SYN-ACK]</code></td><td><code>18:28:07.255151 IP 10.129.2.28.smtp > 10.10.14.2.59618: Flags [S.], &#x3C;SNIP></code></td></tr><tr><td>3.</td><td><code>[ACK]</code></td><td><code>18:28:07.255281 IP 10.10.14.2.59618 > 10.129.2.28.smtp: Flags [.], &#x3C;SNIP></code></td></tr></tbody></table>

