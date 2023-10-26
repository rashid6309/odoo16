from odoo import models, fields

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class GenericSizes(models.Model):
    _name = "ec.generic.size"
    _description = "Generic Sizes "

    generic_size_x = fields.Selection(selection=StaticMember.SIZE_INTEGER,
                                      string='Size X')

    generic_size_y = fields.Selection(selection=StaticMember.SIZE_INTEGER,
                                      string='Size Y')

    tvs_fiobrid_id = fields.Many2one(comodel_name="ec.medical.tvs")
    tvs_cyst_size_id = fields.Many2one(comodel_name="ec.medical.tvs")
