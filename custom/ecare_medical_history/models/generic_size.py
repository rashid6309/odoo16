from odoo import models, fields

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class GenericSizes(models.Model):
    _name = "ec.generic.size"
    _description = "Generic Sizes "
    _rec_name = "type"

    location_or_features = fields.Char(string='Location or features', required=True)
    distorting_endometrium = fields.Selection(selection=StaticMember.CHOICE_YES_NO, string="Distorting Endometrium")
    type = fields.Selection(selection=StaticMember.OVARY_TYPE, string="Location", required=True)

    generic_size_x = fields.Selection(selection=StaticMember.SIZE_INTEGER,
                                      string='Size (cm)')

    generic_size_y = fields.Selection(selection=StaticMember.SIZE_INTEGER,
                                      string='Size (cm)')

    tvs_fiobrid_id = fields.Many2one(comodel_name="ec.medical.tvs")
    gynaecological_fiobrid_id = fields.Many2one(comodel_name="ec.medical.gynaecological.examination")
    tvs_cyst_size_id = fields.Many2one(comodel_name="ec.medical.tvs")
    
    gynaecological_left_size_id = fields.Many2one(comodel_name="ec.medical.gynaecological.examination")
    gynaecological_right_size_id = fields.Many2one(comodel_name="ec.medical.gynaecological.examination")
