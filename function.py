import re
from datetime import datetime

def fetch_business_date_from_filename(filename):
    # Regular expression to match dates in YYYYMMDD, YYYY-MM-DD, DD-MM-YYYY, or similar formats
    date_pattern = re.compile(
        r'(?:\D|^)'          # Non-digit character or start of the string
        r'('                 # Start of the capturing group
        r'(?:\d{4}[-/]\d{1,2}[-/]\d{1,2})'  # YYYY-MM-DD or YYYY/MM/DD
        r'|'                 # OR
        r'(?:\d{1,2}[-/]\d{1,2}[-/]\d{4})'  # DD-MM-YYYY or DD/MM/YYYY
        r'|'                 # OR
        r'(?:\d{4}\d{2}\d{2})'              # YYYYMMDD
        r')'                 # End of the capturing group
        r'(?:\D|$)'          # Non-digit character or end of the string
    )

    # Search for the pattern in the filename
    match = date_pattern.search(filename)
    if match:
        date_str = match.group(1)
        # Try parsing the date in different formats
        for fmt in ("%Y-%m-%d", "%Y%m%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y"):
            try:
                date = datetime.strptime(date_str, fmt)
                # Return the date in YYYYMMDD format
                return date.strftime("%Y%m%d")
            except ValueError:
                continue
    # Return None if no date is found or if it cannot be parsed
    return None

# Example usage:
filename = "report_20230329.pdf"
print(fetch_business_date_from_filename(filename))
