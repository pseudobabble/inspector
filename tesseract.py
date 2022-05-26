from pdf2image import convert_from_path
import sys
#import PyPDF2
#from PIL import Image

import pytesseract

# creating a pdf file object
# pdfFileObj = open('./Ahmed_Cheema.pdf', 'rb')
# # creating a pdf reader object
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
# # printing number of pages in pdf file
# print(pdfReader.numPages)

# # creating a page object
# pageObj = pdfReader.getPage(0)

# # extracting text from page
# print(pageObj.extractText())

 
# Simple image to string
images = convert_from_path(sys.argv[1])
for i in images:
    print(pytesseract.image_to_string(i))
    #print(pytesseract.image_to_data(i))
    #print(pytesseract.image_to_alto_xml(i))
#    print(pytesseract.image_to_string(Image.open('./.png')))
