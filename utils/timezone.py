import pytz
from delorean import Delorean
from datetime import datetime
from ..constants import LOCAL_TZ


def taipei_now() -> str:
    """台北時間"""
    ct = datetime.now(pytz.timezone(LOCAL_TZ))
    return Delorean(datetime=ct).shift('Asia/Taipei').datetime.strftime('%Y-%m-%d %H:%M:%S')
