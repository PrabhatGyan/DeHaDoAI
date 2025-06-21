import pandas as pd
import re
import random
import string


def get_govid_subset(df):

    # Pivot the table to reshape it
    df_pivot = df.pivot_table(
        index=['tag', 'filename'],
        columns='field_name',
        values='ocr_text',
        aggfunc='first'  # handles cases if there are duplicates
    ).reset_index()

    # Drop the now redundant columns
    df_final = df_pivot[['tag', 'filename', 'government_id_value']].reset_index(drop = True)

    return df_final

def clean_government_id(value):
    if pd.isna(value):
        return value, value  # Return NaN as is for both columns

    cleaned_value = str(value).replace(" ", "")  # Remove spaces
    cleaned_value = re.sub(r'[.,\,-,+]', '', cleaned_value)  # Remove unwanted punctuations

    # If there are alphabet characters but string is too long, replace them with digits
    if len(cleaned_value) > 10 and re.search(r'[A-Za-z]', cleaned_value):
        cleaned_value = re.sub(r'[A-Za-z]', lambda _: random.choice(string.digits), cleaned_value)

    # Clean PAN separately if length < 10 and not all digits
    if not cleaned_value.isdigit() and len(cleaned_value) < 10:
        cleaned_value = add_random_pan(cleaned_value)

    # Replace long digit-only Aadhar > 12
    if cleaned_value.isdigit():
        if len(cleaned_value) > 12:
            cleaned_value = cleaned_value[:12]
        elif len(cleaned_value) < 12:
            cleaned_value = add_random_digits(cleaned_value, 12)

    # Final field name decision: if any alphabet in cleaned value → PAN, else Aadhar
    if re.search(r'[A-Za-z]', cleaned_value):
        field_name = 'pancard'
    else:
        field_name = 'aadhaarcard'

    return field_name, cleaned_value

def add_random_digits(value, target_length):
    """ Add random digits to make the number the desired length. """
    for _ in range(target_length - len(value)):
        pos = random.randint(0, len(value))
        value = value[:pos] + random.choice(string.digits) + value[pos:]
    return value

def add_random_pan(value):
    """ If PAN has less than 10 characters, add random alphanumerics. """
    while len(value) < 10:
        value += random.choice(string.ascii_lowercase + string.digits)
    return value