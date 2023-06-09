import PyPDF2
input_file = 'C:\mytmp\downloads\lqnt-trade-confirmation.pdf'


def getPDFText(pdfH):
    # creating a page object
    pageObj = pdfH.getPage(0)
    # extracting text from page
    print(pageObj.extractText())


def main():
    fileH = open(input_file, 'rb')
    pdfH = PyPDF2.PdfFileReader(fileH)

    # printing number of pages in pdf file
    print("Total number of pages in sample.pdf",pdfH.numPages)

    getPDFText(pdfH)
  
    # closing the pdf file object
    fileH.close()

# --- main ---
if __name__ == '__main__':
    main()
