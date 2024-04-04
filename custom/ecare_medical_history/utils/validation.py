from datetime import datetime

from odoo.exceptions import AccessError, UserError
from odoo import fields


class Validation:

    REGEX_FLOAT_2_DP = '^[0-9]+(\.[0-9]{1,2})?$'
    REGEX_INTEGER_SIMPLE = '^[0-9]+(\[0-9])?$'
    REGEX_INTEGER_WITH_CHAR = r'^[0-9\-./\\]+$'

    @staticmethod
    def _date_validation(date):
        if date:
            today = fields.Date.today()
            if date > today:
                raise UserError('Date is greater than today!')

    @staticmethod
    def _year_validation(year):
        if year:
            entered_year = int(year.year) or False
            current_year = int(datetime.now().year)
            if entered_year > current_year:
                raise UserError("Year cannot be greater than the current year")
