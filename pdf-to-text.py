import pandas as pd
import PyPDF2

# todo: #1 make callable function out of this
# todo: #2 convert hard-codings to soft-codings
# todo: #3 fix pypdf2 import problem (may be local)

pyfile=open('23114.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pyfile)

# create page object and extract text
for page in range(11):
    pageObj = pdfReader.getPage(page)
    pageall = pageObj.extractText()

print(pageall)
