from datetime import datetime, timezone


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


def get_datetime(
    str_date: str, str_time: str = "00:00:00"
) -> datetime:  # str_date YYYY-MM-DD     |    str_time  HH:MI:SS
    result: datetime = None

    date = str_date + " " + str_time
    try:
        result = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        print(e)
        result = None

    return result


def get_date_string(date: datetime):
    return date.strftime("%Y-%m-%d %H:%M:%S")
