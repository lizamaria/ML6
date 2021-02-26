import pandas as pd
from __future__ import print_function
import fitz
import sys
from operator import itemgetter

#declare the path of your file
# function that returns doc
file_path = "./data/10N_Sodium_Hydroxide_NaOH_40_6_US_EN_sds.pdf"  #/pdf_file/data.pdf
doc = fitz.open(file_path)

def parse_to_html(pdf):
    """
    Parses pdf file to html object
    Use filepath of pdf as argument
    """
    doc = fitz.open(pdf)
    for page in doc:
        html_content = page.getText("html")
    return html_content

def get_font_style_counts(doc, granularity=False):
    """Extracts fonts and their usage in PDF documents.
    :param doc: PDF document to iterate through
    :type doc: <class 'fitz.fitz.Document'>
    :param granularity: also use 'font', 'flags' and 'color' to discriminate text
    :type granularity: bool
    :rtype: [(font_size, count), (font_size, count}], dict
    :return: most used fonts sorted by count, font style information
    """
    styles = {}
    font_counts = {}

    for page in doc:
        blocks = page.getText("dict")["blocks"]
        for b in blocks:  # iterate through the text blocks
            if b['type'] == 0:  # block contains text
                for l in b["lines"]:  # iterate through the text lines
                    for s in l["spans"]:  # iterate through the text spans
                        if granularity:
                            identifier = (int(s['text'].isupper()), int('bold' in s['font'].lower()), float(s['size'])) #"{0}_{1}_{2}_{3}".format(s['size'], s['flags'], s['font'], s['color'])
                            styles[identifier] = {'size': s['size'], 'flags': s['flags'], 'font': s['font'],
                                                  'color': s['color']}
                        else:
                            identifier = "{0}".format(s['size'])
                            styles[identifier] = {'size': s['size'], 'font': s['font']}

                        font_counts[identifier] = font_counts.get(identifier, 0) + 1  # count the fonts usage
    font_counts = sorted(font_counts.items(), key=itemgetter(1), reverse=True)

    if len(font_counts) < 1:
        raise ValueError("Zero discriminating fonts found!")

    return font_counts, styles

def get_font_tags(font_counts, styles):
    """Returns dictionary with font sizes as keys and tags as value.
    :param font_counts: (font_size, count) for all fonts occuring in document
    :type font_counts: list
    :param styles: all styles found in the document
    :type styles: dict
    :rtype: dict
    :return: all element tags based on font-sizes
    """
    p_style = font_counts[0][0] # get style for most used font by count (paragraph)

    # sorting the font sizes high to low, so that we can append the right integer to each tag 
    font_styles = []
    for ((upper, bold, font_size), count) in font_counts:
        font_styles.append((upper, bold, font_size))
    font_styles.sort(key=itemgetter(0,2,1), reverse=True)
#     return font_styles

    # aggregating the tags for each font size
    idx = 0
    style_tag = {}
    for style in font_styles:
        idx += 1
        if style == p_style:
            idx = 0
            style_tag[style] = '<p>'
            continue
        if style[2] > p_style[2]:
            style_tag[style] = '<h{0}>'.format(idx)
        elif style[2] < p_style[2]:
            style_tag[style] = '<s{0}>'.format(idx)
        else:
            style_tag[style] = '<h{0}>'.format(idx)
    return style_tag


def assign_tags_to_content(doc, style_tag):
    """Scrapes headers & paragraphs from PDF and return texts with element tags.
    :param doc: PDF document to iterate through
    :type doc: <class 'fitz.fitz.Document'>
    :param style_tag: textual element tags for each style (uppercase_flag, bold_flag, size)
    :type style_tag: dict
    :rtype: list
    :return: texts with pre-prended element tags
    """
    header_para = []  # list with headers and paragraphs
    first = True  # boolean operator for first header
    previous_s = {}  # previous span

    for page in doc:
        blocks = page.getText("dict")["blocks"]
        i=0
        for b in blocks:  # iterate through the text blocks
#             i+=1
#             if i == 4:
#                 break
#             print(i)
#             pp.pprint(b)

            if b['type'] == 0:  # this block contains text

                # REMEMBER: multiple fonts and sizes are possible IN one block

                block_string = ""  # text found in block
                for l in b["lines"]:  # iterate through the text lines
                    for s in l["spans"]:  # iterate through the text spans
                        if s['text'].strip():  # removing whitespaces:
                            if first:
                                previous_s = s
                                first = False
                                s_key = (int(s['text'].isupper()), int('bold' in s['font'].lower()), float(s['size']))
                                block_string = style_tag[s_key] + s['text']
                            else:
                                s_key = (int(s['text'].isupper()), int('bold' in s['font'].lower()), float(s['size']))
                                previous_key = (int(previous_s['text'].isupper()), int('bold' in previous_s['font'].lower()), float(previous_s['size']))
                                if s_key == previous_key:

                                    if block_string and all((c == "|") for c in block_string):
                                        # block_string only contains pipes
                                        block_string = style_tag[s_key] + s['text']
                                    if block_string == "":
                                        # new block has started, so append size tag
                                        block_string = style_tag[s_key] + s['text']
                                    else:  # in the same block, so concatenate strings
                                        block_string += " " + s['text']

                                else:
                                    header_para.append(block_string)
                                    block_string = style_tag[s_key] + s['text']

                                previous_s = s

                    # new block started, indicating with a pipe
                    block_string += "|"

                header_para.append(block_string)
    return header_para

font_counts, styles = get_font_style_counts(doc, granularity=True)
style_tag = get_font_tags(font_counts, styles)
assign_tags_to_content(doc, style_tag)

