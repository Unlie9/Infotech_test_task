import datetime


def get_start_end_dates_for_filter_bookings(date: datetime, hours_diff: int):
    start = date - datetime.timedelta(hours=hours_diff)
    end = date + datetime.timedelta(hours=hours_diff)

    return start, end

