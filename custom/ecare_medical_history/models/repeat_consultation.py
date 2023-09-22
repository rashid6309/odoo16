from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class RepeatConsultation(models.Model):
    _name = 'ec.repeat.consultation'
    _description = "Patient First Consultation"



