# This file contains a function that extracts all text in a pdf
# Useful for doing extraction operations based on only the tex
# of a pdf


# todo: test this function

import PyPDF2


def get_pdf_text(path):
    """Renders all the text, with font informtion
    intact, of a pdf file in specified path

    :parameter: path to pdf file ex "file.pdf"

    :returns: pdf_text variable of type string, containing
    all text in the pdf along with font, paragraph, newline,...
    information
    """
    with open(path, 'rb') as pdf:
        pdf_reader = PyPDF2.PdfFileReader(pdf)
        for page in range(11):
            page_object = pdf_reader.getPage(page)
            pdf_text = page_object.extractText()
        return pdf_text
