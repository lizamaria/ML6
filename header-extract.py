# This file contains the functions needed to extract the
# top level section headers in a pdf file and outputs them
# as a list of headers

# This is a work in progress
# todo: fix two reference issues (s_key and 'open' in 'init') (see pycharm problems tab)
# todo: test functionality
# todo: write docstring

# packages used in this file
import re
from operator import itemgetter
import fitz


# Standard variables
standard_headers = [
    r"(\d+.*identification)",
    r"(\d+.*hazard)",
    r"(\d+.*composition)",
    r"(\d+.*first.aid)",
    r"(\d+.*fire.fighting)",
    r"(\d+.*accidental release)",
    r"(\d+.*handling)",
    r"(\d+.*exposure)",
    r"(\d+.*physical and chemical)",
    r"(\d+.*stability and reactivity)",
    r"(\d+.*toxicological)",
    r"(\d+.*ecological)",
    r"(\d+.*disposal)",
    r"(\d+.*transport)",
    r"(\d+.*regulatory)",
    r"(\d+.*other information)"
]

# backbone functions


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


def get_candidate_tags(header_dict):
    candidate_tags = list()
    for ht, hl in header_dict.items():
        if(len(hl)>=16):
            candidate_tags.append(ht)
    return candidate_tags


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
    header_dict = {}
    first = True  # boolean operator for first header
    previous_s = {}  # previous span

    for page in doc:
        blocks = page.getText("dict")["blocks"]
        i=0
        for b in blocks:  # iterate through the text blocks
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
                                    if block_string.startswith("<h"):
                                        if style_tag[previous_key] in header_dict:
                                            header_dict[style_tag[previous_key]].append(block_string[block_string.index(">")+1:])
                                        else:
                                            header_dict[style_tag[previous_key]] = [block_string[block_string.index(">")+1:]]
                                    block_string = style_tag[s_key] + s['text']

                                previous_s = s

                    # new block started, indicating with a pipe
                    block_string += "|"

                header_para.append(block_string)
                if block_string.startswith("<h"):
                    if style_tag[s_key] in header_dict:
                        header_dict[style_tag[s_key]].append(block_string[block_string.index(">")+1:])
                    else:
                        header_dict[style_tag[s_key]] = [block_string[block_string.index(">")+1:]]
    return header_para, header_dict


def score_candidate_tags(candidate_tags, header_dict, standard_headers):
    scores = {}
    for ct in candidate_tags:
        num_matches = 0
        for h in header_dict[ct]:
            for pattern in standard_headers:
                if bool(re.search(pattern, h.lower().strip())):
                    num_matches += 1
                    break
        score = num_matches / len(header_dict[ct])
        scores[ct] = score
    return scores


def get_section_header_list(scores, header_dict):
    section_header_tag = sorted(scores.items(), key=itemgetter(1), reverse=True)[0][0]
    return header_dict[section_header_tag]


def filter_headers(header_list, standard_headers):
    output_list = header_list.copy()
    for h in header_list:
        match = False
        for pattern in standard_headers:
            if bool(re.search(pattern, h.lower().strip())):
                match = True
                break
        if not match:
            output_list.remove(h)
    return output_list

# wrapper functions


def extract_headers(file_path):
    with fitz.open(file_path) as doc:
        font_counts, styles = get_font_style_counts(doc, granularity=True)
        style_tag = get_font_tags(font_counts, styles)
        tagged_text, header_dict = assign_tags_to_content(doc, style_tag)
        candidate_tags = get_candidate_tags(header_dict)
        scores = score_candidate_tags(candidate_tags, header_dict, standard_headers)
        section_header_list = get_section_header_list(scores, header_dict)
        headers = filter_headers(section_header_list, standard_headers)
        return headers

# testing grounds


if __name__ == "__main__":
    extract_headers("data/PHTHALIC-ANHYDRIDE--ACS-5KG-pdf.pdf")
    print("You did it!")
