# FinalRecon

```shell-session
./finalrecon.py --headers --whois --url http://inlanefreight.com
```

```sh
PikachuN@htb[/htb]$ git clone https://github.com/thewhiteh4t/FinalRecon.git
PikachuN@htb[/htb]$ cd FinalRecon
PikachuN@htb[/htb]$ pip3 install -r requirements.txt
PikachuN@htb[/htb]$ chmod +x ./finalrecon.py
PikachuN@htb[/htb]$ ./finalrecon.py --help

usage: finalrecon.py [-h] [--url URL] [--headers] [--sslinfo] [--whois]
                     [--crawl] [--dns] [--sub] [--dir] [--wayback] [--ps]
                     [--full] [-nb] [-dt DT] [-pt PT] [-T T] [-w W] [-r] [-s]
                     [-sp SP] [-d D] [-e E] [-o O] [-cd CD] [-k K]

FinalRecon - All in One Web Recon | v1.1.6

optional arguments:
  -h, --help  show this help message and exit
  --url URL   Target URL
  --headers   Header Information
  --sslinfo   SSL Certificate Information
  --whois     Whois Lookup
  --crawl     Crawl Target
  --dns       DNS Enumeration
  --sub       Sub-Domain Enumeration
  --dir       Directory Search
  --wayback   Wayback URLs
  --ps        Fast Port Scan
  --full      Full Recon

Extra Options:
  -nb         Hide Banner
  -dt DT      Number of threads for directory enum [ Default : 30 ]
  -pt PT      Number of threads for port scan [ Default : 50 ]
  -T T        Request Timeout [ Default : 30.0 ]
  -w W        Path to Wordlist [ Default : wordlists/dirb_common.txt ]
  -r          Allow Redirect [ Default : False ]
  -s          Toggle SSL Verification [ Default : True ]
  -sp SP      Specify SSL Port [ Default : 443 ]
  -d D        Custom DNS Servers [ Default : 1.1.1.1 ]
  -e E        File Extensions [ Example : txt, xml, php ]
  -o O        Export Format [ Default : txt ]
  -cd CD      Change export directory [ Default : ~/.local/share/finalrecon ]
  -k K        Add API key [ Example : shodan@key ]
```

<table data-header-hidden><thead><tr><th width="145.859375"></th><th width="40"></th><th></th></tr></thead><tbody><tr><td>選項</td><td></td><td>描述</td></tr><tr><td><code>-h</code>，<code>--help</code></td><td></td><td>顯示幫助資訊並退出。</td></tr><tr><td><code>--url</code></td><td></td><td>指定目標 URL。</td></tr><tr><td><code>--headers</code></td><td></td><td>檢索目標 URL 的標頭資訊。</td></tr><tr><td><code>--sslinfo</code></td><td></td><td>取得目標 URL 的 SSL 憑證資訊。</td></tr><tr><td><code>--whois</code></td><td></td><td>對目標網域執行 Whois 查詢。</td></tr><tr><td><code>--crawl</code></td><td></td><td>抓取目標網站。</td></tr><tr><td><code>--dns</code></td><td></td><td>對目標網域執行 DNS 枚舉。</td></tr><tr><td><code>--sub</code></td><td></td><td>枚舉目標域的子域。</td></tr><tr><td><code>--dir</code></td><td></td><td>搜尋目標網站上的目錄。</td></tr><tr><td><code>--wayback</code></td><td></td><td>檢索目標的 Wayback URL。</td></tr><tr><td><code>--ps</code></td><td></td><td>對目標執行快速連接埠掃描。</td></tr><tr><td><code>--full</code></td><td></td><td>對目標進行全面偵察掃描。</td></tr></tbody></table>
