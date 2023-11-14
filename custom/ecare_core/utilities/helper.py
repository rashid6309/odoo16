from datetime import datetime


class TimeValidation:

    @staticmethod
    def validate_time(time):

        if time[2:3] != ':':
            time = time[:2] + ':' + time[2:]

        if len(time) != 5:
            return None

        return time

    @staticmethod
    def convert_date_to_days_years(convert_date):
        if not convert_date:
            return None

        today = datetime.today().date()
        difference = today - convert_date
        years = difference.days / 365
        left_days = difference.days - (int(years) * 365.25)
        months = (left_days / 31)

        birth_date_day = convert_date.day
        today_day = today.day

        if today_day >= birth_date_day:
            day = today_day - birth_date_day
        else:
            day = 31 - (birth_date_day - today_day)
        if int(years) < 5:
            return str(int(years)) + 'Y ' + str(int(months)) + 'M ' + str(day) + 'D'
        else:
            return str(int(years)) + ' Years'

    @staticmethod
    def _check_tet_value(self):
        if self.tetanus_vacc_date1st:
            if self.tetanus_vacc_date2nd < self.tetanus_vacc_date1st:
                raise UserError('First Tetanus Date is greater than Second')


class CustomNotification:
    @staticmethod
    def notification_time_validation():
        msg = {
            'warning': {
                'title': 'Warning!',
                'message': 'Time should be of 4 numbers.'
            }
        }
        return msg
