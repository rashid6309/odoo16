from odoo import models


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    def reverse_moves(self):
        action = super(AccountMoveReversal, self).reverse_moves()
        if action.get('view_mode', None) == 'form':
            action['view_id'] = self.env.ref("ecare_invoicing.refund_view_move_form").id
        return action
