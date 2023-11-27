import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

# EC Lab


class EcHMedicalLab(models.Model):
    _name = 'ec.medical.labs'
    _description = "Information about the labs"
    _order = 'create_date desc'

    name = fields.Char(string='Name',
                       required=True)
