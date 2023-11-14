from odoo.exceptions import AccessError, UserError
from odoo import fields


class DateValidation:
    
    @staticmethod
    def _date_validation(date):
        if date:
            today = fields.Date.today()
            if date > today:
                raise UserError('Date is greater than today!')
