from pytz import timezone
from datetime import timedelta, date, datetime


class CustomDateTime:

    @staticmethod
    def convert_user_timezone(user_datetime, time_zone):
        if not time_zone:
            time_zone = 'Asia/Karachi'
        if not user_datetime:
            return False
        return user_datetime.astimezone(timezone(time_zone))

    @staticmethod
    def convert_to_datetime(user_date: date, hours: int, minutes: int, seconds=0) -> datetime:
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)

        ddd = datetime(user_date.year, user_date.month, user_date.day, hours, minutes, seconds)
        return ddd

    @staticmethod
    def convert_str_time_to_float(time: str):
        if not time:
            return None

        if isinstance(time, float):
            time = str(time)

        time = float(time.replace(":", "."))
        return time

    @staticmethod
    def convert_to_time(time: str):
        if isinstance(time, float):
            time = str(time)

        ff = str(time)
        hour, minute = ff.split(':')
        return hour, minute

    @staticmethod
    def get_only_time(timedate):
        hours = timedate.hour
        minutes = timedate.minute
        time = str(f"{hours:02}") + ':' + str(f"{minutes:02}")
        return time


# class CustomDateTime:
        # if not time_zone:
        #     time_zone = 'Asia/Karachi'
        # if not user_datetime:
        #     return False
        # return user_datetime.astimezone(timezone(time_zone))
