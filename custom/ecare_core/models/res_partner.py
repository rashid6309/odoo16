from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    mr_num = fields.Char(compute="get_mr_number")

    def name_get(self):
        result = []
        for rec in self:
            # This is slow
            patient_id = self.env['ec.medical.patient'].search(domain=[('partner_id', '=', rec.id)], order="id desc",
                                                               limit=1)
            if not patient_id.mr_num:
                continue

            mr_num = patient_id.mr_num + " - " if patient_id.mr_num else ""
            result.append((rec.id, '%s %s' % (mr_num, rec.name)))
        return result
