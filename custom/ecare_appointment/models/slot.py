# TODO: Check if it is being used and if not REMOVE.

from odoo import models, api, fields

class SlotRecord(models.Model):
    _name = "ec.record.slot"
    _description = "Record of Slot"

    category = fields.Many2one('ec.slot.category')
    sub_category = fields.Many2one('ec.slot.sub.category')
    # days_availability

    # timeslot = fields.Many2one()

