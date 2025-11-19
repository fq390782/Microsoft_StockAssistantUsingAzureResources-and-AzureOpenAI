from datetime import datetime, timedelta
from dateutil import parser  # pip install python-dateutil

def time_ago(dt_str: str | datetime) -> str:
    """
    Mon, 10 Nov 2025 11:13:00 +0900 --> 1분전, 1일전, 1주 전  등과 같이 변환.
    """
    if isinstance(dt_str, str):
        dt = parser.parse(dt_str)
    else:
        dt = dt_str
    now = datetime.now(dt.tzinfo)
    diff = now - dt

    seconds = diff.total_seconds()
    minutes = seconds // 60
    hours = seconds // 3600
    days = seconds // 86400

    if seconds < 60:
        return "방금 전"
    elif minutes < 60:
        return f"{int(minutes)}분 전"
    elif hours < 24:
        return f"{int(hours)}시간 전"
    elif days < 7:
        return f"{int(days)}일 전"
    elif days < 30:
        weeks = days // 7
        return f"{int(weeks)}주 전"
    elif days < 365:
        months = days // 30
        return f"{int(months)}개월 전"
    else:
        years = days // 365
        return f"{int(years)}년 전"
    
