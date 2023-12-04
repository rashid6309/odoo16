from odoo.exceptions import AccessError, UserError
from odoo import fields


class Validation:

    REGEX_FLOAT_2_DP = '^[0-9]+(\.[0-9]{1,2})?$'

    @staticmethod
    def _date_validation(date):
        if date:
            today = fields.Date.today()
            if date > today:
                raise UserError('Date is greater than today!')
