import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

# EC Lab


class EcHMedicalLab(models.Model):
    _name = 'ec.medical.labs'
    _description = "Medical Labs"
    _order = 'name asc'

    name = fields.Char(string='Name',
                       required=True)

    _sql_constraints = [
        ('name_unique', 'unique (name)',
         'Lab name already exists!'),
    ]
