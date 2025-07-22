from odoo import models, fields


class ResUsers(models.Model):
   _inherit = 'res.users'

   screen_lock_pin = fields.Char(string='Screen Lock PIN', size=4)