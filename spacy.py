#import json
#import pickle
import random

#spacy.prefer_gpu()
#nlp = spacy.load("en_core_web_sm")

try:
    import spacy
    import json
except Exception as e:
    print(e)


class EntityGenerator(object):
    _slots__ = ['text']

    def __init__(self, text=None):
        self.text = text

    def get(self):
        """
        Return a Json
        """
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.text)
        text = [ent.text for ent in doc.ents]
        entity = [ent.label_ for ent in doc.ents]

        from collections import Counter
        import json

        data = Counter(zip(entity))
        unique_entity = list(data.keys())
        unique_entity = [x[0] for x in unique_entity]

        d = {}
        for val in unique_entity:
            d[val] = []

        for key, val in dict(zip(text, entity)).items():
            if val in unique_entity:
                d[val].append(key)
        return d


try:
    import PyPDF2
    import requests
    import json
except Exception:
    pass


class Resume(object):
    def __init__(self, filename=None):
        self.filename = filename

    def get(self):
        """

        """
        fFileObj = open(self.filename, 'rb')
        pdfReader = PyPDF2.PdfFileReader(fFileObj)
        pageObj = pdfReader.getPage(0)
        print("Total Pages : {} ".format(pdfReader.numPages))

        resume = pageObj.extractText()
        return resume


resume = Resume(filename="580076.pdf")
response_text = resume.get()

response_text


helper = EntityGenerator(text = response_text)
response = helper.get()
print(json.dumps(response, indent=3))

latin_letters = {}


def is_latin(uchr):
    try:
        return latin_letters[uchr]
    except KeyError:
        try:
            return latin_letters.setdefault(
                uchr, 'LATIN' in ud.name(uchr))
        except:
            print(uchr)
            raise Exception()


def only_roman_chars(unistr):
    return all(is_latin(uchr) for uchr in unistr if uchr.isalpha())


data = ResumeParser("580076.pdf").get_extracted_data()

ners = ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE',
        'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']

# The ners we are most interested in
# ners_small = ['PERSON', 'EVENT', 'PERCENT']

nlp = spacy.load("en_core_web_sm")

data['ner'] = data['Description'].apply(lambda desc: dict(Counter([ent.label_ for ent in nlp(desc).ents])))
