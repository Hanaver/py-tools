import PyPDF2
import os
import time
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

def add_watermark(input_pdf, output_pdf, watermark_image, page_number):
    # Open the PDF file
    with open(input_pdf, 'rb') as input_file:
        reader = PyPDF2.PdfReader(input_file)
        writer = PyPDF2.PdfWriter()

        # Create a PDF canvas
        c = canvas.Canvas("temp_watermark.pdf", pagesize=letter)

        # Add the watermark image
        c.drawImage(watermark_image, 1 * inch, 1 * inch, width=100, height=100, preserveAspectRatio=True, mask='auto')
        

        # Save the canvas as PDF
        c.save()

        # Open the watermark PDF
        watermark_pdf = PyPDF2.PdfReader("temp_watermark.pdf")

        # Merge the watermark PDF with the original PDF
        pdf_page_num = len(reader.pages)
        current_page = 0
        keywords = ['订购合同', 'SALES CONTRACT']
        while (current_page < pdf_page_num):
            # print(current_page)
            page = reader.pages[current_page]
            page_text = page.extract_text()
            # print(page_text)
            if any(keyword in page_text for keyword in keywords):
                page.merge_page(watermark_pdf.pages[page_number])
                
            writer.add_page(page)
            current_page += 1

        # Write the output PDF file
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

        # Clean up temporary file
        os.remove("temp_watermark.pdf")

# Example usage
# input_directory = './sources/'
# output_directory = './news/'
# watermark_image = './logo.png'
# page_number = 0  # 页码从0开始

# for filename in os.listdir(input_directory):
#     if filename.endswith('.pdf'):
#         input_pdf_path = os.path.join(input_directory, filename)
#         output_pdf_path = os.path.join(output_directory, filename)
        
#         # Add watermark to the PDF file
#         add_watermark(input_pdf_path, output_pdf_path, watermark_image, page_number)

def process_directory(directory_path, output_directory, watermark_image_path):
    # Iterate through each file and directory in the given directory path
    for root, _, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith('.pdf'):
                input_pdf_path = os.path.join(root, filename)
                output_pdf_path = os.path.join(output_directory, os.path.relpath(input_pdf_path, directory_path))
                
                # Create output directory if it does not exist
                os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
                
                # Add watermark to the PDF file
                add_watermark(input_pdf_path, output_pdf_path, watermark_image_path, 0)


input_directory = './sources/'
output_directory = './news/'
watermark_image = './logo.png'
page_number = 0  # 页码从0开始

process_directory(input_directory, output_directory, watermark_image)
print('执行成功')
time.sleep(10)