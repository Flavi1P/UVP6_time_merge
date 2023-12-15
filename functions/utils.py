import re

def extract_date(text):
    matches = re.findall("[0-9]{8}", text)
    if matches:
        return matches[-1]
    else:
        return None
