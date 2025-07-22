from odoo import models, fields, api, _
from collections import defaultdict
from odoo.tools import float_is_zero, float_round, float_repr, float_compare


class POSOrderInherit(models.Model):
    _inherit = "pos.order"

    name1 = fields.Char(string="Name")
    custom_analytic_account_id = fields.Many2one(
        "account.analytic.account",
        related="session_id.custom_analytic_account_id",
        string="Custom Analytic Account",
    )

    def _prepare_invoice_line(self, order_line):
        res = super(POSOrderInherit, self)._prepare_invoice_line(order_line)
        if self.custom_analytic_account_id:
            res.update(
                {
                    "custom_analytic_account_id": self.custom_analytic_account_id.id,
                    "analytic_distribution": {self.custom_analytic_account_id.id: 100},
                }
            )
        return res

    def _prepare_invoice_vals(self):
        res = super(POSOrderInherit, self)._prepare_invoice_vals()
        res.update(
            {
                "custom_analytic_account_id": self.custom_analytic_account_id.id,
            }
        )
        return res


class PosSession(models.Model):
    _inherit = "pos.session"

    custom_analytic_account_id = fields.Many2one(
        "account.analytic.account", string="Custom Analytic Account"
    )

    def _create_combine_account_payment(self, payment_method, amounts, diff_amount):
        outstanding_account = (
            payment_method.outstanding_account_id
            or self.company_id.account_journal_payment_debit_account_id
        )
        destination_account = self._get_receivable_account(payment_method)

        if (
            float_compare(
                amounts["amount"], 0, precision_rounding=self.currency_id.rounding
            )
            < 0
        ):
            # revert the accounts because account.payment doesn't accept negative amount.
            outstanding_account, destination_account = (
                destination_account,
                outstanding_account,
            )

        account_payment = self.env["account.payment"].create(
            {
                "amount": abs(amounts["amount"]),
                "journal_id": payment_method.journal_id.id,
                "force_outstanding_account_id": outstanding_account.id,
                "destination_account_id": destination_account.id,
                "ref": _("Combine %s POS payments from %s")
                % (payment_method.name, self.name),
                "pos_payment_method_id": payment_method.id,
                "pos_session_id": self.id,
                "custom_analytic_account_id": self.custom_analytic_account_id.id
                if self.custom_analytic_account_id
                else False,
            }
        )

        diff_amount_compare_to_zero = self.currency_id.compare_amounts(diff_amount, 0)
        if diff_amount_compare_to_zero != 0:
            self._apply_diff_on_account_payment_move(
                account_payment, payment_method, diff_amount
            )

        account_payment.action_post()
        return account_payment.move_id.line_ids.filtered(
            lambda line: line.account_id == account_payment.destination_account_id
        )

    def _create_split_account_payment(self, payment, amounts):
        payment_method = payment.payment_method_id
        if not payment_method.journal_id:
            return self.env["account.move.line"]
        outstanding_account = (
            payment_method.outstanding_account_id
            or self.company_id.account_journal_payment_debit_account_id
        )
        accounting_partner = self.env["res.partner"]._find_accounting_partner(
            payment.partner_id
        )
        destination_account = accounting_partner.property_account_receivable_id

        if (
            float_compare(
                amounts["amount"], 0, precision_rounding=self.currency_id.rounding
            )
            < 0
        ):
            # revert the accounts because account.payment doesn't accept negative amount.
            outstanding_account, destination_account = (
                destination_account,
                outstanding_account,
            )

        account_payment = self.env["account.payment"].create(
            {
                "amount": abs(amounts["amount"]),
                "partner_id": payment.partner_id.id,
                "journal_id": payment_method.journal_id.id,
                "force_outstanding_account_id": outstanding_account.id,
                "destination_account_id": destination_account.id,
                "ref": _("%s POS payment of %s in %s")
                % (payment_method.name, payment.partner_id.display_name, self.name),
                "pos_payment_method_id": payment_method.id,
                "pos_session_id": self.id,
                "custom_analytic_account_id": self.custom_analytic_account_id.id
                if self.custom_analytic_account_id
                else False,
            }
        )
        account_payment.action_post()
        return account_payment.move_id.line_ids.filtered(
            lambda line: line.account_id == account_payment.destination_account_id
        )

    def _create_diff_account_move_for_split_payment_method(
        self, payment_method, diff_amount
    ):
        self.ensure_one()

        get_diff_vals_result = self._get_diff_vals(payment_method.id, diff_amount)
        if not get_diff_vals_result:
            return

        source_vals, dest_vals = get_diff_vals_result
        diff_move = self.env["account.move"].create(
            {
                "journal_id": payment_method.journal_id.id,
                "date": fields.Date.context_today(self),
                "ref": self._get_diff_account_move_ref(payment_method),
                "line_ids": [Command.create(source_vals), Command.create(dest_vals)],
                "custom_analytic_account_id": self.custom_analytic_account_id.id
                if self.custom_analytic_account_id
                else False,
            }
        )
        diff_move._post()

    def _create_cash_statement_lines_and_cash_move_lines(self, data):
        data = super(PosSession, self)._create_cash_statement_lines_and_cash_move_lines(
            data
        )
        if self.custom_analytic_account_id:
            if data.get("split_cash_statement_lines", False):
                data.get("split_cash_statement_lines").write(
                    {
                        "custom_analytic_account_id": self.custom_analytic_account_id.id,
                    }
                )

            if data.get("split_cash_receivable_lines", False):
                data.get("split_cash_receivable_lines").write(
                    {
                        "custom_analytic_account_id": self.custom_analytic_account_id.id,
                        "analytic_distribution": {
                            self.custom_analytic_account_id.id: 100
                        },
                    }
                )

            if data.get("combine_cash_statement_lines", False):
                data.get("combine_cash_statement_lines").write(
                    {
                        "custom_analytic_account_id": self.custom_analytic_account_id.id,
                    }
                )

            if data.get("combine_cash_receivable_lines", False):
                data.get("combine_cash_receivable_lines").write(
                    {
                        "custom_analytic_account_id": self.custom_analytic_account_id.id,
                        "analytic_distribution": {
                            self.custom_analytic_account_id.id: 100
                        },
                    }
                )

        return data

    def _debit_amounts(
        self,
        partial_move_line_vals,
        amount,
        amount_converted,
        force_company_currency=False,
    ):
        data = super(PosSession, self)._debit_amounts(
            partial_move_line_vals,
            amount,
            amount_converted,
            force_company_currency=force_company_currency,
        )
        if self.custom_analytic_account_id:
            data.update(
                {
                    "custom_analytic_account_id": self.custom_analytic_account_id.id,
                    "analytic_distribution": {self.custom_analytic_account_id.id: 100},
                }
            )

        return data

    def _credit_amounts(
        self,
        partial_move_line_vals,
        amount,
        amount_converted,
        force_company_currency=False,
    ):
        data = super(PosSession, self)._credit_amounts(
            partial_move_line_vals,
            amount,
            amount_converted,
            force_company_currency=force_company_currency,
        )
        if self.custom_analytic_account_id:
            data.update(
                {
                    "custom_analytic_account_id": self.custom_analytic_account_id.id,
                    "analytic_distribution": {self.custom_analytic_account_id.id: 100},
                }
            )

        return data


class PosPayment(models.Model):
    _inherit = "pos.payment"

    custom_analytic_account_id = fields.Many2one(
        "account.analytic.account", related="session_id.custom_analytic_account_id"
    )

    def _create_payment_moves(self):
        result = self.env["account.move"]
        for payment in self:
            order = payment.pos_order_id
            payment_method = payment.payment_method_id
            if payment_method.type == "pay_later" or float_is_zero(
                payment.amount, precision_rounding=order.currency_id.rounding
            ):
                continue
            accounting_partner = self.env["res.partner"]._find_accounting_partner(
                payment.partner_id
            )
            pos_session = order.session_id
            journal = pos_session.config_id.journal_id
            payment_move = (
                self.env["account.move"]
                .with_context(default_journal_id=journal.id)
                .create(
                    {
                        "journal_id": journal.id,
                        "date": fields.Date.context_today(payment),
                        "ref": _("Invoice payment for %s (%s) using %s")
                        % (order.name, order.account_move.name, payment_method.name),
                        "pos_payment_ids": payment.ids,
                        "custom_analytic_account_id": self.custom_analytic_account_id.id
                        if self.custom_analytic_account_id
                        else False,
                    }
                )
            )
            result |= payment_move
            payment.write({"account_move_id": payment_move.id})
            amounts = pos_session._update_amounts(
                {"amount": 0, "amount_converted": 0},
                {"amount": payment.amount},
                payment.payment_date,
            )
            credit_line_vals = pos_session._credit_amounts(
                {
                    "account_id": accounting_partner.with_company(
                        order.company_id
                    ).property_account_receivable_id.id,  # The field being company dependant, we need to make sure the right value is received.
                    "partner_id": accounting_partner.id,
                    "move_id": payment_move.id,
                },
                amounts["amount"],
                amounts["amount_converted"],
            )
            debit_line_vals = pos_session._debit_amounts(
                {
                    "account_id": pos_session.company_id.account_default_pos_receivable_account_id.id,
                    "move_id": payment_move.id,
                },
                amounts["amount"],
                amounts["amount_converted"],
            )

            if self.custom_analytic_account_id:
                credit_line_vals.update(
                    {
                        "custom_analytic_account_id": self.custom_analytic_account_id.id,
                        "analytic_distribution": {
                            self.custom_analytic_account_id.id: 100
                        },
                    }
                )
                debit_line_vals.update(
                    {
                        "custom_analytic_account_id": self.custom_analytic_account_id.id,
                        "analytic_distribution": {
                            self.custom_analytic_account_id.id: 100
                        },
                    }
                )

            self.env["account.move.line"].with_context(
                check_move_validity=False
            ).create([credit_line_vals, debit_line_vals])
            payment_move._post()
        return result


class pos_analytic_account_bank_statement_line(models.Model):
    _inherit = "account.bank.statement.line"

    custom_analytic_account_id = fields.Many2one(
        "account.analytic.account", related="pos_session_id.custom_analytic_account_id"
    )

    def _prepare_move_line_default_vals(self, counterpart_account_id=None):
        """Prepare the dictionary to create the default account.move.lines for the current account.bank.statement.line
        record.
        :return: A list of python dictionary to be passed to the account.move.line's 'create' method.
        """
        self.ensure_one()

        if not counterpart_account_id:
            counterpart_account_id = self.journal_id.suspense_account_id.id

        if not counterpart_account_id:
            raise UserError(
                _(
                    "You can't create a new statement line without a suspense account set on the %s journal.",
                    self.journal_id.display_name,
                )
            )

        (
            company_amount,
            _company_currency,
            journal_amount,
            journal_currency,
            transaction_amount,
            foreign_currency,
        ) = self._get_amounts_with_currencies()

        liquidity_line_vals = {
            "name": self.payment_ref,
            "move_id": self.move_id.id,
            "partner_id": self.partner_id.id,
            "account_id": self.journal_id.default_account_id.id,
            "currency_id": journal_currency.id,
            "amount_currency": journal_amount,
            "debit": company_amount > 0 and company_amount or 0.0,
            "credit": company_amount < 0 and -company_amount or 0.0,
            "custom_analytic_account_id": self.custom_analytic_account_id.id,
        }

        # Create the counterpart line values.
        counterpart_line_vals = {
            "name": self.payment_ref,
            "account_id": counterpart_account_id,
            "move_id": self.move_id.id,
            "partner_id": self.partner_id.id,
            "currency_id": foreign_currency.id,
            "amount_currency": -transaction_amount,
            "debit": -company_amount if company_amount < 0.0 else 0.0,
            "credit": company_amount if company_amount > 0.0 else 0.0,
            "custom_analytic_account_id": self.custom_analytic_account_id.id,
        }
        return [liquidity_line_vals, counterpart_line_vals]

    # def _prepare_reconciliation_move_line(self, move, amount):

    # 	company_currency = self.journal_id.company_id.currency_id
    # 	statement_currency = self.journal_id.currency_id or company_currency
    # 	st_line_currency = self.currency_id or statement_currency
    # 	amount_currency = False
    # 	st_line_currency_rate = self.currency_id and (self.amount_currency / self.amount) or False
    # 	if isinstance(move, dict):
    # 		amount_sum = sum(x[2].get('amount_currency', 0) for x in move['line_ids'])
    # 	else:
    # 		amount_sum = sum(x.amount_currency for x in move.line_ids)

    # 	if st_line_currency != company_currency and st_line_currency == statement_currency:

    # 		amount_currency = -amount_sum
    # 	elif st_line_currency != company_currency and statement_currency == company_currency:

    # 		amount_currency = -amount_sum
    # 	elif st_line_currency != company_currency and st_line_currency != statement_currency:

    # 		amount_currency = -amount_sum/st_line_currency_rate
    # 	elif st_line_currency == company_currency and statement_currency != company_currency:

    # 		amount_currency = amount/st_line_currency_rate

    # 	account_id = amount >= 0 \
    # 		and self.statement_id.journal_id.default_credit_account_id.id \
    # 		or self.statement_id.journal_id.default_debit_account_id.id

    # 	if not account_id:
    # 		raise UserError(_('No default debit and credit account defined on journal %s (ids: %s).' % (self.statement_id.journal_id.name, self.statement_id.journal_id.ids)))

    # 	aml_dict = {
    # 		'name': self.name,
    # 		'partner_id': self.partner_id and self.partner_id.id or False,
    # 		'account_id': account_id,
    # 		'credit': amount < 0 and -amount or 0.0,
    # 		'debit': amount > 0 and amount or 0.0,
    # 		'statement_line_id': self.id,
    # 		'currency_id': statement_currency != company_currency and statement_currency.id or (st_line_currency != company_currency and st_line_currency.id or False),
    # 		'amount_currency': amount_currency,
    # 	}
    # 	if aml_dict:
    # 		if self.custom_analytic_account_id.id:
    # 			aml_dict.update({'custom_analytic_account_id':self.custom_analytic_account_id.id})
    # 	if isinstance(move, self.env['account.move'].__class__):
    # 		aml_dict['move_id'] = move.id
    # 	return aml_dict


class account_payment(models.Model):
    _inherit = "account.payment"

    custom_analytic_account_id = fields.Many2one(
        "account.analytic.account", string="Analytic Account on POS Order"
    )

    @api.model
    def create(self, vals_list):
        result = super(account_payment, self).create(vals_list)
        if result:
            if vals_list.get("communication"):
                pos = self.env["pos.session"].search(
                    [
                        "|",
                        ("name", "=", vals_list.get("communication")),
                        ("name", "=ilike", vals_list.get("communication")),
                    ]
                )
                if pos:
                    if pos.custom_analytic_account_id:
                        result.update(
                            {
                                "custom_analytic_account_id": pos.custom_analytic_account_id.id
                            }
                        )
        return result


class AccountMove(models.Model):
    _inherit = "account.move"

    custom_analytic_account_id = fields.Many2one(
        "account.analytic.account", string="Analytic Account on POS Order"
    )

    @api.model
    def create(self, vals_list):
        rec = super(AccountMove, self).create(vals_list)
        if rec:
            if vals_list.get("origin") or vals_list.get("ref"):
                session_name = vals_list.get("origin") or vals_list.get("ref")
                pos = self.env["pos.session"].search([("name", "=", session_name)])
                if pos:
                    if pos.custom_analytic_account_id:
                        rec.update(
                            {
                                "custom_analytic_account_id": pos.custom_analytic_account_id.id,
                            }
                        )
        return rec


class account_payment_line(models.Model):
    _inherit = "account.move.line"

    custom_analytic_account_id = fields.Many2one(
        "account.analytic.account",
        string="Analytic Account",
        related="move_id.custom_analytic_account_id",
    )
