class TimeValidation:

    @staticmethod
    def validate_time(time):

        if time[2:3] != ':':
            time = time[:2] + ':' + time[2:]

        if len(time) != 5:
            return None

        return time


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
