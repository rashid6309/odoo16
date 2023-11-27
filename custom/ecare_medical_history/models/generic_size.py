from odoo import models, fields

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class GenericSizes(models.Model):
    _name = "ec.generic.size"
    _description = "Generic Sizes "
    _rec_name = "type"

    type = fields.Selection(selection=StaticMember.OVARY_TYPE, string="Location")

    generic_size_x = fields.Selection(selection=StaticMember.SIZE_INTEGER,
                                      string='Size (cm)', required=True)

    generic_size_y = fields.Selection(selection=StaticMember.SIZE_INTEGER,
                                      string='Size (cm)', required=True)

    tvs_fiobrid_id = fields.Many2one(comodel_name="ec.medical.tvs")
    gynaecological_fiobrid_id = fields.Many2one(comodel_name="ec.medical.tvs")
    tvs_cyst_size_id = fields.Many2one(comodel_name="ec.medical.tvs")
    
    gynaecological_left_size_id = fields.Many2one(comodel_name="ec.medical.gynaecological.examination")
    gynaecological_right_size_id = fields.Many2one(comodel_name="ec.medical.gynaecological.examination")
