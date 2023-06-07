from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    def name_get(self):
        result = []
        # We can improve this further but for now it's good.
        for rec in self:
            patient_id = self.env['ec.medical.patient'].search(domain=[('partner_id', '=', rec.id)], order="id desc",
                                                               limit=1)
            if not patient_id.mr_num:
                continue

            result.append((rec.id, '%s' % (rec.name)))
        return result
