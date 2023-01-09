import pytz
import datetime


def timezone_diff(tz1, tz2):
    tz1 = pytz.timezone(tz1)
    tz2 = pytz.timezone(tz2)
    dt = datetime.datetime.now()
    
    delta_time = tz1.utcoffset(dt) - tz2.utcoffset(dt)
    delta_minutes = delta_time.total_seconds() / 60

    delta_str = '+' if delta_minutes >= 0 else '-'
    delta_str += f"{int(abs(delta_minutes / 60)):02}:"
    delta_str += f"{int(abs(delta_minutes % 60)):02}"

    return delta_minutes, delta_str

