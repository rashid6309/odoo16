from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError
from collections import defaultdict

from odoo.addons.ecare_core.utilities.helper import TimeValidation, CustomNotification
from odoo.addons.ecare_core.utilities.time_conversion import CustomDateTime

# Logger
from logging import getLogger
_logger = getLogger(__name__)

from datetime import datetime

"""
    Feature: It is blocking of a slot in each day in the specific date-time
"""


class BlockSlots(models.Model):
    _name = "ec.block.slot"
    _description = "Block slot in specific time in each day."

    _rec_name = "category_id"
    _order = "end_date desc"

    category_id = fields.Many2one(comodel_name="ec.slot.sub.category",
                                  required=True,
                                  ondelete="restrict")

    start_date = fields.Date(string="Start Date",
                             required=True)

    end_date = fields.Date(string="End Date",
                           )

    active_time = fields.Char(string="From",
                              required=True)

    to_time = fields.Char(string="To",
                          required=True)

    active = fields.Boolean(default=False)

    block_slot_data = defaultdict(list)

    @api.constrains('end_date')
    def check_end_date(self):
        if self.start_date < datetime.today().date():
            raise UserError("Start Date can't be less than today.")

        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                self.end_date = None
                raise AccessError('Start date should be less than end date.')


    @api.constrains("active_time", "to_time", "active")
    def check_unique_slots(self):
        if not self.active:
            return True

        query = """
        select
            *
        from
            (
            select
                a.id,
                a.category_id,
                a.start_date,
                a.end_date, 
                cast(replace(a.active_time, ':', '.') as float8) as start_time,
                cast(replace(a.to_time, ':', '.') as float8) as end_time
            from
                ec_block_slot a
            where
                a.category_id = {} -- category
                and a.active = true
                and a.start_date >= '{}' -- start_date
                and a.end_date is null"""

        query_if_end_date_exist = """
        select 
        * 
        from (
            select
                a.id,
                a.category_id,
                a.start_date,
                a.end_date, 
                cast(replace(a.active_time, ':', '.') as float8) as start_time,
                cast(replace(a.to_time, ':', '.') as float8) as end_time
            from
                ec_block_slot a
            where
                a.category_id = {} -- category
                -- category ; 
                and a.active = true
                and a.start_date >= '{}' -- start_date
                and a.end_date <= '{}' -- end_date
        """

        where_block = """
        ) as b
        where
            ({} between b.start_time and end_time -- active_time
            or 
            {} between b.start_time and end_time) -- to_time
            and b.id != {}
        """

        # Query building
        if not self.end_date:
            query = (query + where_block)\
                .format(self.category_id.id,
                        self.start_date,
                        CustomDateTime.convert_str_time_to_float(self.active_time),
                        CustomDateTime.convert_str_time_to_float(self.to_time),
                        self.id)
        else:
            query = (query_if_end_date_exist + where_block)\
                .format(self.category_id.id,
                        self.start_date,
                        self.end_date,
                        CustomDateTime.convert_str_time_to_float(self.active_time),
                        CustomDateTime.convert_str_time_to_float(self.to_time),
                        self.id)

        self.env.cr.execute(query)

        result = self.env.cr.fetchone()
        if result:
            print(result)
            raise AccessError("From and to time can't be overlap.")

    @api.onchange('active_time', "to_time")
    def _onchange_time(self):
        if self.to_time:
            time = TimeValidation.validate_time(self.to_time)

            if not time:
                return CustomNotification.notification_time_validation()

            self.to_time = time

        if self.active_time:
            time = TimeValidation.validate_time(self.active_time)

            self.active_time = time
            if not time:
                return CustomNotification.notification_time_validation()

    # TODO MEMORIZATION OF THIS FUNCTION: For 1 day it is but not for all days.
    def prepare_block_slot_data(self, categories, date):
        """
        It will populate the block slot data in the attribute values

        :param categories: List of category ids
        :param date: Date
        :return: Populate dict of with block slot data
        """

        # Can be optimized as for each day still it'll prepare the values again and again.
        BlockSlots.block_slot_data = defaultdict(list)

        objects = self.search(domain=[('category_id', 'in', categories),
                                      ('start_date', '<=', date),
                                      ('active', '=', True)])
        for obj in objects:

            active_time = CustomDateTime.convert_str_time_to_float(obj.active_time)
            to_time = CustomDateTime.convert_str_time_to_float(obj.to_time)

            self.block_slot_data[obj.category_id.id].append({
                'active_time': active_time,
                'to_time': to_time
            })

        return self.block_slot_data

    def check_slot_block(self, category_id, active_time, to_time, date=None):
        """
        It will check if the category is blocked or not

        :param to_time: The time for which we need to check in the day i.e. 10:30
        :param active_time: The time for which we need to check in the day i.e. 10:00
        :param category_id: Category id against we need to check either it is blocked or not
        :param date: Optional but better if provided as incase the "block_slot_data" is empty it will populate it
        :return: True/ False
        """

        if not self.block_slot_data and date:
            self.prepare_block_slot_data([category_id], date)

        if not self.block_slot_data:
            _logger.warning("Block slot data is not populated please check....")

        active_time = CustomDateTime.convert_str_time_to_float(active_time)
        to_time = CustomDateTime.convert_str_time_to_float(to_time)

        if datas := self.block_slot_data.get(category_id, None):
            for data in datas:
                if active_time >= data['active_time'] and to_time <= data['to_time']:
                    return True

        return False
