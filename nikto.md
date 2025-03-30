# Nikto

## Nikto

`Nikto`是一個功能強大的開源網路伺服器掃描器。除了作為漏洞評估工具的主要功能外， `Nikto's`指紋辨識功能還可以提供對網站技術堆疊的洞察。

```sh
PikachuN@htb[/htb]$ sudo apt update && sudo apt install -y perl
PikachuN@htb[/htb]$ git clone https://github.com/sullo/nikto
PikachuN@htb[/htb]$ cd nikto/program
PikachuN@htb[/htb]$ chmod +x ./nikto.pl
```

```sh
PikachuN@htb[/htb]$ nikto -h inlanefreight.com -Tuning b
```

## Scrapy

```shell-session
PikachuN@htb[/htb]$ pip3 install scrapy
```

```shell-session
PikachuN@htb[/htb]$ wget -O ReconSpider.zip https://academy.hackthebox.com/storage/modules/144/ReconSpider.v1.2.zip
PikachuN@htb[/htb]$ unzip ReconSpider.zip 
```
