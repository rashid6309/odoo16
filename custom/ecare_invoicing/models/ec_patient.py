from odoo import models, _
from odoo.exceptions import UserError


class Patient(models.Model):
    _inherit = "ec.medical.patient"

    def action_advance_payment(self):
        open_payments = self.env['account.payment'].search(domain=[('is_reconciled', '=', False),
                                                                 ('partner_id', '=', self.partner_id.id)])

        if not self.mr_num:
            raise UserError("Please generate MR No.")

        if not open_payments:
            raise UserError("No advance payments")

        partner_id = self.partner_id
        context = self._context.copy()
        context.update({
            'default_partner_id': partner_id.id,
        })

        return{
            "name": _("Advance Payments"),
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'view_mode': 'tree,form',
            'target': 'current',
            'context': context,
            'views': [(self.env.ref('account.view_account_payment_tree').id, 'tree'),
                      (self.env.ref('account.view_account_payment_form').id, 'form')
                      ],
            'domain': [('id', 'in', open_payments.ids)]
        }

    def action_open_invoice_line_history(self):
        query = '''
        select
            aml.create_date datetime,
            emp.id patient_id,	
            aml.product_id product_id,
            aml.move_id move_id,
            case am.move_type 
            when 'out_invoice' then 'Invoice'
            when 'out_refund' then 'Refund' 
            else '' end as invoice_type,
			-1 * aml.balance amount,
            INITCAP(am.payment_state) payment_state
        from
            account_move_line aml
        inner join account_move am on am.id = aml.move_id
        inner join ec_medical_patient emp on emp.partner_id = aml.partner_id
        where
            aml.partner_id = %(partner_id)s
            and aml.product_id is not null
            and am.state = 'posted'
        order by
            aml.create_date desc;
        '''

        self._cr.execute(query, {'partner_id': self.partner_id.id})
        values = self._cr.dictfetchall()

        patient_move_line_history = self.env['patient.account.move.line.history'].create(values)

        return {
            "name": _("Services"),
            "type": 'ir.actions.act_window',
            "res_model": 'patient.account.move.line.history',
            "view_id": self.env.ref("ecare_invoicing.patient_move_line_history_tree_view").id,
            'view_mode': 'tree',
            "target": 'current',
            'domain': [('id', 'in', patient_move_line_history.ids),
                       ('patient_id', '=', self.id)],
        }
