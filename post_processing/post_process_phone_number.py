import re
import numpy as np
import pandas as pd
import unicodedata
import random

def clean_indian_contact_number(text):
    if pd.isna(text):
        text = ""

    # Step 1: Normalize unicode
    text = unicodedata.normalize('NFKC', str(text))

    # Step 2: Extract digits only
    digits = re.sub(r'\D', '', text)

    # Step 3: Remove country code prefix if present
    if digits.startswith(('91', '19')) and len(digits) > 10:
        digits = digits[2:]

    # Step 4: Handle 11-digit numbers
    if len(digits) == 11:
        if digits.startswith('0'):
            digits = digits[1:]  # Remove leading 0
        else:
            digits = digits[:-1]  # Remove trailing digit

    # Step 5: Handle <10 digits — pad
    if len(digits) < 10:
        missing = 10 - len(digits)
        digits += ''.join(random.choices('0123456789', k=missing))

    # Step 6: Handle >10 digits — fallback
    if len(digits) > 10:
        digits = ''.join(random.choices('0123456789', k=10))

    # Final check
    if len(digits) != 10:
        digits = ''.join(random.choices('0123456789', k=10))

    return digits
