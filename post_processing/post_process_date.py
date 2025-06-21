import pandas as pd
import random
import re
from datetime import datetime, timedelta

def clean_and_parse_date(text):
    if pd.isna(text):
        return generate_random_date_str()

    # Step 1: Basic cleaning
    text = str(text).strip()
    text = re.sub(r'[^0-9/-]', '', text)  # keep only digits, hyphen, slash
    text = text.replace('-', '/').replace(' ', '')  # normalize separator

    # Step 2: Try strict formats
    known_formats = ['%m/%d/%Y', '%d/%m/%Y']
    for fmt in known_formats:
        try:
            dt = datetime.strptime(text, fmt)
            return dt.strftime(fmt)
        except:
            continue

    # Step 3: Try pandas flexible parse
    try:
        dt = pd.to_datetime(text, dayfirst=True, errors='coerce')
        if pd.notna(dt) and dt.year >= 1980:
            return dt.strftime('%d/%m/%Y')
    except:
        pass

    # Step 4: Fallback to random date
    return generate_random_date_str()

def generate_random_date_str(start_year=1980, end_year=datetime.today().year):
    """ Generate a random realistic date between Jan 1, 1980 and today. """
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime('%m/%d/%Y')
