import datetime as datetime_obj
from datetime import datetime
from typing import Tuple


def get_start_end_dates_for_filter_bookings(
    date: datetime, 
    hours_diff: int
) -> Tuple[datetime, datetime]:
    
    start = date - datetime_obj.timedelta(hours=hours_diff)
    end = date + datetime_obj.timedelta(hours=hours_diff)

    return start, end

