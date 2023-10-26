from odoo import api, models, fields, _


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


    tvs_uterus_tvs_size = fields.Boolean(default=False, string="Size")
    tvs_uterus_tvs_position = fields.Boolean(default=False, string="Position")
    tvs_uterus_tvs_normal = fields.Boolean(default=False, string="Normal")
    tvs_uterus_tvs_fiobrid = fields.Boolean(default=False, string="Fiobrid")

    tvs_uterus_size_x = fields.Selection(selection=StaticMember.SIZE_INTEGER,
                                         string='Size X')

    tvs_uterus_size_y= fields.Selection(selection=StaticMember.SIZE_INTEGER,
                                        string='Size Y')

    tvs_uterus_position = fields.Selection(selection=StaticMember.UTERUS_SIZE_POSITION,
                                           string='Position')

    tvs_lining = fields.Selection(selection=StaticMember.LINING,
                                  string='Lining')
    tvs_lining_size = fields.Selection(selection=StaticMember.SIZE_INTEGER,
                                       string='Size')

    cyst_type = fields.Char(string="Cyst Type")
    cyst_nos = fields.Char(string='Size')

    tvs_rov = fields.Text(string='ROV', readonly=True)

    tvs_lov = fields.Text(string='LOV', readonly=True)

    tvs_other_text = fields.Text(string='Other')
    tvs_generic_sizes_ids = fields.One2many(comodel_name="ec.generic.size",
                                        inverse_name="tvs_fiobrid_id")

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

    def action_tvs_output_process_text(self):
        if self.tvs_id:
            context = self._context.copy()
            record = self.env['ec.medical.tvs'].browse(int(self.tvs_id.id))

            if context and record:
                field = context.get('default_field')
                if field and field == 'tvs_rov':
                    return record.write({
                        'tvs_rov': str(self.display),
                    })
                elif field and field == 'tvs_lov':
                    return record.write({
                        'tvs_lov': str(self.display),
                    })

