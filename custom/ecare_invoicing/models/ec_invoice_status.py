import werkzeug
from odoo import models, _
from odoo.exceptions import UserError,ValidationError
from odoo.tools.misc import html_escape
from odoo.http import request


import json


class InvoiceStatus(models.AbstractModel):
    _name = 'report.ecare_invoicing.report_invoice_custom'
    _description = 'Proforma Report'

    def _get_report_values(self, docids, data=None):
        # try:
        #     print("japosdfj")
        #     raise
        # except Exception as e:
        docs = self.env['account.move'].browse(docids[0])
        if docs.state == 'draft':
            error = {
                'message': "Draft report cannot be printed",
            }
            res = request.make_response(html_escape(json.dumps(error)))
            raise werkzeug.exceptions.HTTPException(description='Cannot convert into barcode.', response=res)
        else:
            return {
                'doc_ids': docs.ids,
                'doc_model': 'account.move',
                'docs': docs,
            }



