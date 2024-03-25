from odoo import api, models, fields, _

import re
from odoo.exceptions import UserError
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class EcMedicalTVS(models.Model):
    _name = 'ec.medical.tvs'
    _description = "Patient TVS"
    _rec_name = "tvs_patient_id"

    tvs_patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                     string="Patient",
                                     readonly=True)
    tvs_repeat_consultation_id = fields.Many2one(comodel_name='ec.repeat.consultation',
                                                 readonly=True,
                                                 string='Repeat Consultation')

    tvs_cycle_day = fields.Integer(readonly=1, string="Cycle day")

    tvs_uterus_tvs = fields.Selection(selection=StaticMember.UTERUS_TVS,
                                      string='Uterus')

    tvs_uterus_position_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                               relation='tvs_uterus_multi_selection_repeat_position',
                                               column1='tvs_id',
                                               column2='multi_selection_id',
                                               string='Position',
                                               domain="[('type', '=', 'position')]")

    tvs_uterus_tvs_size = fields.Boolean(default=False, string="Size")
    tvs_uterus_tvs_position = fields.Boolean(default=False, string="Position")
    # tvs_uterus_tvs_normal = fields.Boolean(default=False, string="Normal")
    tvs_uterus_tvs_fiobrid = fields.Boolean(default=False, string="Fibroid")

    tvs_uterus_flexion = fields.Selection(selection=StaticMember.UTERUS_FLEXION, string='Uterus Flexion')

    tvs_uterus_size_x = fields.Selection(selection=StaticMember.SIZE_INTEGER,
                                         string='Size X')

    tvs_uterus_size_y= fields.Selection(selection=StaticMember.SIZE_INTEGER,
                                        string='Size Y')



    tvs_uterus_position = fields.Selection(selection=StaticMember.UTERUS_SIZE_POSITION,
                                           string='Position')

    position_to_left = fields.Boolean(string="Deviated to Left", default=False)
    position_to_right = fields.Boolean(string="Deviated to Right", default=False)
    position_a_v = fields.Boolean(string="Av/V", default=False)
    position_r_v = fields.Boolean(string="R/V", default=False)
    position_mid_position = fields.Boolean(string="Mid Position", default=False)

    tvs_linining_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                        relation='repeat_multi_selection_repeat_position',
                                        column1='tvs_id',
                                        column2='multi_selection_id',
                                        string='Endometrial Lining Character',
                                        domain="[('type', '=', 'linining')]")

    tvs_smooth = fields.Boolean(string="Smooth", default=False)
    tvs_distorted = fields.Boolean(string="Distorted", default=False)
    tvs_triple_echo = fields.Boolean(string="Triple Echo", default=False)
    tvs_hyperechoic_solid = fields.Boolean(string="Hyperechoic/Solid", default=False)
    tvs_suspected_cavity_lesion = fields.Boolean(string="Suspected Cavity Lesion", default=False)

    tvs_lining_size = fields.Selection(selection=StaticMember.SIZE_INTEGER,
                                       string='CET')

    tvs_cyst_size_ids = fields.One2many(comodel_name="ec.generic.size",
                                        inverse_name="tvs_fiobrid_id",
                                        string="Fibroid")

    tvs_rov = fields.Char(string='ROV')

    tvs_lov = fields.Char(string='LOV')

    tvs_other_text = fields.Text(string='Other')
    tvs_generic_sizes_ids = fields.One2many(comodel_name="ec.generic.size",
                                            inverse_name="tvs_cyst_size_id",
                                            string="Sizes")

    # tvs_signs_of_ovulation_ids = fields.Many2many(string='Signs of Ovulation',
    #                                               selection=StaticMember.SIGN_OVULATION)
    tvs_signs_of_ovulation_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                                  relation='repeat_multi_selection_repeat_ovulation',
                                                  column1='tvs_ovulation_id',
                                                  column2='multi_selection_id',
                                                  string='Signs of Ovulation',
                                                  domain="[('type', '=', 'ovulation')]")
    tv_diagnosis = fields.Selection(selection=StaticMember.TVS_DIAGNOSIS,
                                    string='Diagnosis of Ultrasound')
    tvs_left_ovary_not_visualised = fields.Boolean(string='Not Visualised', default=False)
    tvs_right_ovary_not_visualised = fields.Boolean(string='Not Visualised', default=False)
    def action_open_tvs_scan(self):
        context = self._context.copy()
        if context:
            field = context.get('default_field')
            if field:
                return {
                    "name": _("TVS Scan"),
                    "type": 'ir.actions.act_window',
                    "res_model": 'ec.medical.tvs.scan',
                    'view_id': self.env.ref('ecare_medical_history.view_ec_medical_tvs_scan_form').id,
                    'view_mode': 'form',
                    "target": 'new',
                    "context": {
                        'default_tvs_id': self.id,
                        'default_field': field
                    },
                }

    def action_open_form_view(self, repeat_consultation_id, target='current'):
        context = self.env.context.copy()
        context['target'] = target

        tvs_exist = self.env['ec.medical.tvs'].search([(
            'tvs_repeat_consultation_id', '=', repeat_consultation_id.id
        )], limit=1)

        if tvs_exist:
            return {
                "name": _("TVS"),
                "type": 'ir.actions.act_window',
                "res_model": 'ec.medical.tvs',
                'view_id': self.env.ref('ecare_medical_history.view_ec_medical_tvs_form').id,
                'view_mode': 'form',
                "target": target,
                "res_id": tvs_exist.id,
                'flags': {'initial_mode': 'edit'},
            }

        context['default_tvs_repeat_consultation_id'] = repeat_consultation_id.id
        context['default_tvs_patient_id'] = repeat_consultation_id.repeat_timeline_id.timeline_patient_id.id

        return {
            "name": _("TVS"),
            "type": 'ir.actions.act_window',
            "res_model": 'ec.medical.tvs',
            'view_id': self.env.ref('ecare_medical_history.view_ec_medical_tvs_form').id,
            'view_mode': 'form',
            "target": target,
            'context': context,
        }


class EcMedicalTVSScan(models.TransientModel):
    _name = 'ec.medical.tvs.scan'
    _description = "Patient TVS Scan"

    display = fields.Char('Output')
    tvs_id = fields.Many2one(comodel_name='ec.medical.tvs',
                             string='TVS')
    gynae_id = fields.Many2one(comodel_name='ec.medical.gynaecological.examination',
                               string='Gynaecological')

    def action_tvs_output_process_text(self):
        if self.tvs_id:
            context = self._context.copy()
            record = self.tvs_id

            if context and record:
                field = context.get('default_field')
                display = self.display or None
                if display:
                    # Convert the string to a list of elements
                    data_list = display.split(',')

                    # Separate the '+' and '>22' elements
                    plus_elements = [element for element in data_list if element == '+']
                    greater_than_22_elements = [element for element in data_list if element == '>22']

                    # Remove '+' and '>22' elements from the original list
                    data_list = [element for element in data_list if element not in ['+', '>22']]

                    # Sort the remaining elements in ascending order
                    sorted_data = sorted(data_list, key=lambda x: int(x) if x.isdigit() else float('inf'))

                    # Concatenate the '+' elements, sorted elements, and '>22' elements
                    result_list = plus_elements + sorted_data + greater_than_22_elements

                    # Filter out empty strings and join the list back to a string
                    result_str = ','.join(filter(None, result_list))
                    display = result_str
                if field and field == 'tvs_rov':
                    return record.write({
                        'tvs_rov': display,
                    })
                elif field and field == 'tvs_lov':
                    return record.write({
                        'tvs_lov': display,
                    })
        if self.gynae_id:
            context = self._context.copy()
            record = self.gynae_id

            if context and record:
                field = context.get('default_field')
                display = self.display or None
                if display:
                    # Convert the string to a list of elements
                    data_list = display.split(',')

                    # Separate the '+' and '>22' elements
                    plus_elements = [element for element in data_list if element == '+']
                    greater_than_22_elements = [element for element in data_list if element == '>22']

                    # Remove '+' and '>22' elements from the original list
                    data_list = [element for element in data_list if element not in ['+', '>22']]

                    # Sort the remaining elements in ascending order
                    sorted_data = sorted(data_list, key=lambda x: int(x) if x.isdigit() else float('inf'))

                    # Concatenate the '+' elements, sorted elements, and '>22' elements
                    result_list = plus_elements + sorted_data + greater_than_22_elements

                    # Filter out empty strings and join the list back to a string
                    result_str = ','.join(filter(None, result_list))
                    display = result_str
                if field and field == 'gynae_rov':
                    return record.write({
                        'gynae_rov': display,
                    })
                elif field and field == 'gynae_lov':
                    return record.write({
                        'gynae_lov': display,
                    })

    @api.onchange('display')
    def _check_display_input(self):
        for record in self:
            if record.display and not re.match('^[0-9\.,+>]*$', record.display):
                raise UserError("Please enter a valid value.")
