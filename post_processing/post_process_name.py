import unicodedata
import re
import pandas as pd


def normalize_unicode(text):
    if pd.isna(text):
        return ''
    return unicodedata.normalize('NFKC', text)


def clean_punctuation(text):
    if pd.isna(text):
        return ''
    return re.sub(r"[^a-zA-Z\s']", '', text)


def collapse_spaces(text):
    if pd.isna(text):
        return ''
    return re.sub(r'\s+', ' ', text).strip()

# def apply_title_case(text):
#     if pd.isna(text):
#         return ''
#     return text.title()

def clean_candidate_name(text):
    text = normalize_unicode(text)
    text = clean_punctuation(text)
    text = collapse_spaces(text)
    # text = apply_title_case(text)
    return text
