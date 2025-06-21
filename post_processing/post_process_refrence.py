import pandas as pd
import re
import random
import string

def clean_reference_text(text):
    if pd.isna(text) or not isinstance(text, str) or text.strip() == "":
        return "Unknown - " + generate_random_mobile()

    text = text.strip()

    # Extract phone part from text by isolating potential phone-like parts
    raw_number = re.findall(r'[\dOoIiLl#\- ]+', text)
    number_part = ''.join(raw_number).lower() if raw_number else ''

    # Normalize characters in the number part
    number_part = number_part.replace('o', '0').replace('i', '1').replace('l', '1')
    number_part = re.sub(r'[^0-9]', '', number_part)  # Remove anything non-digit

    # Handle digit count
    if len(number_part) > 10:
        number_part = number_part[:10]
    elif len(number_part) < 10:
        number_part = add_random_digits(number_part, 10)

    # Extract name by removing phone-like patterns from text
    name = re.sub(r'[\dOoIiLl#\- ]+', ' ', text)
    name = re.sub(r'\s+', ' ', name).strip()

    if not name:
        name = "Unknown"

    return f"{name} - {number_part}"

def generate_random_mobile():
    return ''.join(random.choices(string.digits, k=10))

def add_random_digits(number, target_length):
    while len(number) < target_length:
        insert_pos = random.randint(0, len(number))
        number = number[:insert_pos] + random.choice(string.digits) + number[insert_pos:]
    return number