import re

import pandas as pd
import unicodedata
from unidecode import unidecode
from rapidfuzz import process, fuzz


from dateutil import parser
from datetime import datetime
from difflib import get_close_matches


'''
Post-Processing Functions
1. Nationality
2. Gender
3. Martial Status
4. Blood Group
5. Qualifications
'''

#==============================
# Valid Options for all fields
#==============================

valid_nationality = ['indian']
valid_genders = ['male', 'female']
valid_statuses = ['married', 'single']
valid_blood_groups = ['a+', 'a-', 'ab-', 'ab+', 'o-', 'b+', 'b-', 'o+', 'o+ve']

valid_qualifications = [
    '10th pass', '12th pass', 'graduate', 'post-graduate',
    'diploma', 'phd', 'integrated m.tech', 'b.tech'
]

#==============================
# Genral Cleaning Function
#==============================

# Common cleaning
# 1. Convert into lower case
# 2. Remove all whitespaces

def recommended_cleaning(value):
    """
    Cleans a single string value by:
    1. Converting to lowercase
    2. Removing all whitespaces (spaces, tabs, newlines)
    """
    if pd.isna(value):
        return value
    value = str(value).lower()
    value = re.sub(r'\s+', '', value)
    return value

# General Cleaning of the OCR Text
def clean_ocr_text(text):
    if not isinstance(text, str):
        return None

    # Unicode normalization
    text = unicodedata.normalize('NFKC', text)

    # Lowercase
    text = text.lower()

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove non-alphanumeric characters (except dots, hyphens, etc. based on use case)
    text = re.sub(r"[^\w\s\.-]", '', text)

    # Replace multiple dots or hyphens
    text = re.sub(r'\.{2,}', '.', text)
    text = re.sub(r'-{2,}', '-', text)

    # Remove leading/trailing dots/hyphens
    text = text.strip('.-')

    # Fix common OCR character swaps
    # text = text.replace('0', 'o').replace('1', 'l').replace('5', 's')

    # Remove known junk patterns
    text = re.sub(r'\b(na|n/a|none|nil|--|___|\.\.\.|unknown)\b', '', text)

    # Normalize spaces again
    text = re.sub(r'\s+', ' ', text).strip()

    return text if text else None

#==============================
# Nationality
#==============================

def clean_nationality(val):
    if pd.isna(val):
        return 'indian'
    
    val_clean = str(val).lower().strip()
    
    # Rule 1: if 'ind' in text → assign 'indian'
    if 'ind' in val_clean:
        return 'indian'
    
    # Rule 2: if exact match to valid list
    if val_clean in valid_nationality:
        return val_clean
    
    # Rule 3: fuzzy match with valid list
    match = get_close_matches(val_clean, valid_nationality, n=1, cutoff=0.85)
    if match:
        return match[0]
    
    # Rule 4: fallback
    return 'indian'

#==============================
# MARITAL STATUS
#==============================

# Cleaning function
def clean_marital_status(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z]', '', text)  # remove punctuation, digits, spaces

    # Optional manual corrections
    manual_map = {
        'unmarried': 'single',
        'singlefemale': 'single',
        'bingle': 'single',
        'singl': 'single',
        'engle': 'single',
        'maggied': 'married',
        'marrived': 'married',
    }
    if text in manual_map:
        return manual_map[text]

    # Fuzzy matching
    match, score, _ = process.extractOne(text, valid_statuses, scorer=fuzz.ratio)
    return match if score >= 70 else 'na'  # can adjust threshold

#==============================
# Gender
#==============================

# Manual fixes for common OCR mistakes
MANUAL_CORRECTIONS = {
    'm': 'male',
    'f': 'female',
    'femba': 'female',
    'fembe': 'female',
    'fema le': 'female',
    'mak': 'male',
    'make': 'male',
    'hale': 'male',
    'made': 'male',
    'mala': 'female',  # Depending on context; could be male too
    'malik': 'male',
    'mode': 'male',    # Ambiguous; assuming "male"
    'tamil': 'male',   # Very likely a location misread
}

def clean_gender(text):
    # Step 1: Normalize
    text = str(text).strip().lower()
    
    # Step 2: Remove non-letters
    text = re.sub(r'[^a-z]', '', text)

    # Step 3: Manual rule-based corrections
    if text in MANUAL_CORRECTIONS:
        return MANUAL_CORRECTIONS[text]

    # Step 4: Fuzzy match fallback
    match, score, _ = process.extractOne(text, valid_genders, scorer=fuzz.ratio)
    return match if score >= 70 else 'na'

#==============================
# Blood Group
#==============================

# Preprocessing function for blood group

def clean_blood_group(text, fallback_mode='o+'):
    if not isinstance(text, str):
        return fallback_mode  # Or return None

    text = text.lower()
    text = text.strip()

    # Replace common OCR errors
    text = text.replace('0', 'o')
    text = text.replace('1', 'l')
    text = text.replace('ve', '+')
    text = re.sub(r'[^a-z+-]', '', text)  # Keep only valid characters

    # Fix spacing and variations
    text = text.replace('ab', 'ab').replace('at', 'a+').replace('bt', 'b+')
    text = re.sub(r'(a|b|ab|o)[\s-]*(\+|plus)', r'\1+', text)
    text = re.sub(r'(a|b|ab|o)[\s-]*(\-|minus)', r'\1-', text)

    # Default a/b/o to positive
    if text in ['a', 'b', 'o']:
        text += '+'

    # Fuzzy match if not directly valid
    if text in valid_blood_groups:
        return text
    else:
        match = get_close_matches(text, valid_blood_groups, n=1, cutoff=0.7)
        return match[0] if match else fallback_mode  # Or return None

#==============================
# Qualifications
#==============================  

MANUAL_CORRECTIONS = {
    # Standard variations
    '10th': '10th pass', 'tenth pass': '10th pass', '10th class': '10th pass', 
    '10th standard': '10th pass', '10th pan': '10th pass', '10th paris': '10th pass',
    'l0thpass': '10th pass', '10th paas': '10th pass', '10th pgs': '10th pass',

    '12th': '12th pass', '12th standard': '12th pass', '12th class': '12th pass',
    '12th q&a': '12th pass', '12th par': '12th pass', '12th pais': '12th pass',
    '12th passing': '12th pass', '12th paul': '12th pass', '12th pam': '12th pass',

    'graduation': 'graduate', 'graduated': 'graduate', 'graduat': 'graduate',
    'graduado': 'graduate', 'graduate @': 'graduate',

    'post graduate': 'post-graduate', 'post - graduate': 'post-graduate',
    'post- graduate': 'post-graduate', 'postgraduate': 'post-graduate',
    'post-graduates': 'post-graduate', 'past - graduate': 'post-graduate',
    'post - graduation': 'post-graduate', 'post-graduation': 'post-graduate',

    'bsc computer science': 'graduate', 'bsc graduates': 'graduate',
    'b.sc': 'graduate', 'b.sc. graduation': 'graduate',

    'ph.d': 'phd', 'ph.d.': 'phd', 'ph d': 'phd', 'ph. d': 'phd',
    'b.ph.d': 'phd', 'pnd': 'phd',

    'integrated mtech': 'integrated m.tech', 'integrated m.tech': 'integrated m.tech',

    'b.t': 'b.tech', 'btech': 'b.tech',

    'diplom': 'diploma', 'jiploma': 'diploma',
    
    # Irrelevant or ambiguous mappings
    'doctor': 'phd',
    'mba': 'post-graduate',
    'currently pursuing be - ece': 'b.tech',
    'to be passed': None,
    'with pan': None,
    'with pass': None,
    'birla': None,
    'lahori darbar': None,
    'best-grocery': None,
    'craaluwa': None,
    'tatti pass': None,
}

def clean_qualification(text):
    if not isinstance(text, str):
        return None

    # Normalize
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s\.-]', '', text)  # keep letters, digits, dash, dot

    # Manual corrections
    if text in MANUAL_CORRECTIONS:
        return MANUAL_CORRECTIONS[text]

    # Fuzzy match
    match, score, _ = process.extractOne(text, valid_qualifications, scorer=fuzz.token_sort_ratio)
    return match if score >= 70 else None
