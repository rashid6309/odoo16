from odoo import api, models, fields, _
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class EcMedicalMultiSelection(models.Model):
    _name = 'ec.medical.multi.selection'

    name = fields.Char(string='Name')
    type = fields.Selection(selection=StaticMember.MULTI_SELECTION_FIELD, string='Type')
