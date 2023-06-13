from odoo import models, fields, api, tools


class MoveLineReport(models.Model):
    _name = 'report.account.move.line'
    _description = "Account Move Line Report"
    _auto = False


    patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                 string="Patient")

    product_template_id = fields.Many2one(comodel_name="product.template",
                                          string="Product")

    create_date = fields.Datetime(string="Datetime")

    service_type = fields.Char(string="Service Type")

    price_subtotal = fields.Float(string="Sub Total")

    discount = fields.Float(string="Discount")

    refund = fields.Float(string="Refund")

    # sub_total = fields.Float(string="Balance")

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW %s AS (
            select
            	row_number() over (order by aml.id) as id,
            	emp.id patient_id,
                pt.id product_template_id, 
                aml.create_date ,
                pt.service_type,
                aml.fixed_amount_discount as discount,
                aml.refund_amount as refund,
                am.move_type ,
                case when am.move_type = 'out_refund'
                then aml.price_subtotal * -1 
                else aml.price_subtotal end price_subtotal
            from
                account_move_line aml
            inner join account_move am 
            on
                aml.move_id = am.id
                and am.state = 'posted'
                and am.payment_state = 'paid'
            inner join product_product pp 
            on
                pp.id = aml.product_id
            inner join product_template pt 
            on
                pt.id = pp.product_tmpl_id
            inner join ec_medical_patient emp 
            on 
               emp.partner_id = aml.partner_id
            )''' % (self._table,)
        )

