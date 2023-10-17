from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class EcMedicalTVS(models.Model):
    _name = 'ec.medical.tvs'
    _description = "Patient TVS"
    _rec_name = "patient_id"

    patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                 string="Patient",
                                 readonly=True)
    repeat_consultation_id = fields.Many2one(comodel_name='ec.repeat.consultation',
                                             readonly=True,
                                             string='Repeat Consultation')

    date = fields.Date(string='Date',
                       default=fields.Datetime.now,
                       readonly=True)

    lmp = fields.Date(string='LMP')

    day_of_cycle = fields.Selection(selection=StaticMember.DAY_OF_CYCLE,
                                    string='Day of Cycle')

    uterus_tvs = fields.Selection(selection=StaticMember.UTERUS_TVS, string='Uterus')

    lining = fields.Selection(selection=StaticMember.LINING, string='Lining')
    lining_size = fields.Char(string='Size')

    # tуре_tvs = fields.Selection([
    #     ('type1', 'Type 1'),
    #     ('type2', 'Type 2'),
    # ], string='Туре')
    cyst_type = fields.Char(string="Cyst Type")
    cyst_nos = fields.Char(string='Size')

    rov = fields.Text(string='ROV')

    lov = fields.Text(string='LOV')

    other_text = fields.Text(string='Other')

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
            'repeat_consultation_id', '=', repeat_consultation_id.id
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

        context['default_repeat_consultation_id'] = repeat_consultation_id.id
        context['default_patient_id'] = repeat_consultation_id.repeat_timeline_id.timeline_patient_id.id

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
                if field and field == 'rov':
                    return record.write({
                        'rov': str(self.display),
                    })
                elif field and field == 'lov':
                    return record.write({
                        'lov': str(self.display),
                    })

