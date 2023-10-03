import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

# Health Center


class EcHealthCenters(models.Model):
    _name = 'ec.medical.health.center'
    _description = "Information about the health centers"

    name = fields.Char(string='Name',
                       required=True)
