from odoo import models, fields

#Add policy Category for posible future reporting
class FinalOutcome(models.Model):
    _name = 'final.outcome'
    _description = 'Final Outcome'
    _order = 'name' # this is to order by name

    name = fields.Char("Name", required=True)