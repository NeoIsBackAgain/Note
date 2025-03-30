# DNS

* **網域輸入驗證：**
  * 確保提供域名作為參數；如果沒有，它會顯示使用說明並退出。
* **DNS 記錄查詢：**
  * 定義要查詢的 DNS 記錄類型清單：A、AAAA、MX、NS、TXT、CNAME 和 SOA 。
  * 對於每種記錄類型，使用`dig`命令檢索與網域相關的記錄。
  * 顯示檢索到的記錄或指示是否未找到記錄。
* **反向 DNS 查找：**
  * 對從 A 記錄查詢取得的任何 IPv4 位址執行反向 DNS 查找（PTR 記錄） 。
  * 顯示 PTR 記錄或指示是否未找到任何記錄。
* **DNS 區域傳輸嘗試：**
  * 檢索網域的權威名稱伺服器（NS 記錄） 。
  * 對於每個名稱伺服器，請嘗試使用命令中的 AXFR 查詢類型進行 DNS 區域傳輸`dig`。
  * 如果傳輸成功則顯示區域數據，如果傳輸失敗或不允許則指示。

```sh
#!/bin/bash
# smart_dns.sh
# 检查是否提供了域名参数
# 使用方法: chmod +x smart_dns.sh | ./smart_dns.sh example.com
if [ -z "$1" ]; then
  echo "使用方法: $0 <域名>"
  exit 1
fi

DOMAIN=$1

# 定义要查询的记录类型
RECORD_TYPES=("A" "AAAA" "MX" "NS" "TXT" "CNAME" "SOA")
# A: 检索与域名关联的 IPv4 地址（A 记录）。
# AAAA: 检索与域名关联的 IPv6 地址（AAAA 记录）。
# MX: 寻找负责该域名的邮件服务器（MX 记录）。
# NS: 标识域名的权威名称服务器。
# TXT: 检索与域名相关的任何 TXT 记录。
# CNAME: 检索域名的规范名称（CNAME 记录）。
# SOA: 检索域名的授权起始（SOA 记录）。

# 执行查询并显示结果的函数
perform_query() {
  local type=$1
  echo -e "\n查询 $DOMAIN 的 $type 记录:"
  result=$(dig "$DOMAIN" "$type" +noall +answer)
  if [ -n "$result" ]; then
    echo "$result"
  else
    echo "未找到 $DOMAIN 的 $type 记录。"
  fi
}

# 遍历每种记录类型并执行查询
for TYPE in "${RECORD_TYPES[@]}"; do
  perform_query "$TYPE"
done

# 执行反向解析（PTR 记录）
echo -e "\n执行反向解析（PTR 记录）:"
IPV4_ADDRESSES=$(dig "$DOMAIN" A +short)
if [ -n "$IPV4_ADDRESSES" ]; then
  for IP in $IPV4_ADDRESSES; do
    ptr_result=$(dig -x "$IP" +noall +answer)
    if [ -n "$ptr_result" ]; then
      echo "$ptr_result"
    else
      echo "未找到 IP $IP 的 PTR 记录。"
    fi
  done
else
  echo "未找到 A 记录，跳过反向解析。"
fi

# 执行 DNS 区域传输（AXFR）
echo -e "\n尝试执行 DNS 区域传输（AXFR）:"
# 获取域名的 NS 记录
NS_SERVERS=$(dig "$DOMAIN" NS +short)
if [ -n "$NS_SERVERS" ]; then
  for NS in $NS_SERVERS; do
    echo -e "\n从名称服务器 $NS 获取区域传输数据:"
    axfr_result=$(dig @"$NS" "$DOMAIN" AXFR)
    if [[ $axfr_result == *"Transfer failed."* || $axfr_result == *"XFR size"* ]]; then
      echo "$axfr_result"
    else
      echo "名称服务器 $NS 不允许区域传输或传输失败。"
    fi
  done
else
  echo "未找到 NS 记录，无法尝试区域传输。"
fi

```

