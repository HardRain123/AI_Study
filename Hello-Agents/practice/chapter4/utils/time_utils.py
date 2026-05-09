from datetime import datetime
import pytz


def now_str():
    tz = pytz.timezone("Asia/Seoul")
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M")
