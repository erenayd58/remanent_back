
import datetime

def generate_id(prefix="REM"):
    today = datetime.date.today()
    return f"{prefix}-{today.year}-{today.month:02d}-{today.day:02d}-{today.strftime('%j')}"  # unique-ish per day
