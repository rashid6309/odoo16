from odoo import models, api, fields
from datetime import timedelta, datetime
from odoo.addons.ecare_core.utilities.time_conversion import CustomDateTime

import calendar


class Category(models.Model):
    _name = "ec.slot.category"
    _description = "Category configuration"
    _inherit = ['mail.thread']

    _rec_name = "name"
    _order = "order desc"

    name = fields.Char(string='Name',
                       required=True,
                       tracking=True)

    order = fields.Integer(string='Order Number')

    parent_category_id = fields.Many2one(comodel_name="ec.slot.category",
                                         string="Primary Category",
                                         domain=[('parent_category_id', '=', False)])

    active = fields.Boolean(default=True)

    # not required now, *Remove* this in future.
    # product_ids = fields.Many2many(comodel_name="product.product",
    #                                column1="slot_category_id",
    #                                column2="product_id",
    #                                relation="slot_category_product_id",
    #                                string="Available Products",
    #                                domain=[('detailed_type', '=', 'service')]
    #                                )

    def get_category_required_data(self, categories):
        values = []
        if not categories:
            return values

        for category in categories:
            values.append({
                'category_id': category.id,
                'category_name': category.name,
            })
        return values

    def get_sub_categories_data(self, sub_categories_total):
        sub_categories = []

        sub_categories_total = sorted(sub_categories_total, key=lambda x: x['order']) # Sort

        for rec in sub_categories_total:
            sub_category = {
                'sub_category_id': rec.id,
                'sub_category_name': rec.name + " \n " + rec.description if rec.description else rec.name,
            }
            sub_categories.append(sub_category)

        return sub_categories

    def get_relevant_categories(self, parent_category_id, active_category_id):
        """
        It will fetch the parent and categories and will send those.

        This is only when the localstorage of browse has some id saved
        which is not in the system then system will just assign the first from the list of categories.

        Test case: test_session_inactive_categories

        :param parent_category_id: Parent category which client side user has selected
        :param active_category_id: Active category which client side user has selected

        :return:
        parent_category_ids (list of objects), active_parent_category_id (Integer Id),
        fetch-category( list of objects), category_id (Single Object)

        """

        parent_category_ids = self.env['ec.slot.category'].search(domain=[('active', '=', True),
                                                                         ('parent_category_id', '=', False)],
                                                                  order="order asc")
        active_parent_category_id = None

        if parent_category_id == 'null' or parent_category_id is None or parent_category_id == 0:  # If invalid
            if parent_category_ids:
                active_parent_category_id = parent_category_ids[0]
        else:
            active_parent_category_id = self.env['ec.slot.category'].search([('id', '=', parent_category_id),
                                                                             ('active', '=', True)])

        """ 
        Incase the value found in session but that doesn't exist in the DB 
        Validation but still the issue can be that the parent and active both can't be present.
        Incase the category is not found or been in-active 
        """
        if not active_parent_category_id and parent_category_ids:
            active_parent_category_id = parent_category_ids[0]

        fetch_category = None
        if active_parent_category_id:
            fetch_category = self.env['ec.slot.category'].search(domain=[('active', '=', True),
                                                                       ('parent_category_id',
                                                                        '=', active_parent_category_id.id)],
                                                                 order="order asc")

        category_id = None

        if active_category_id == 'null' or active_category_id is None or active_category_id == 0:  # If invalid
            if fetch_category:
                category_id = fetch_category[0]
        else:
            category_id = self.env['ec.slot.category'].search(domain=[('id', '=', active_category_id),
                                                               ('active', '=', True)])

        ''' Incase the value found in session but that doesn't exist in the DB '''
        ''' Validation but still the issue can be that the parent and active both can't be present. '''

        if not category_id and fetch_category:
            category_id = fetch_category[0]

        ''' Checks end here'''

        if active_parent_category_id: # Get the id
            active_parent_category_id = active_parent_category_id.id

        return parent_category_ids, active_parent_category_id, fetch_category, category_id

    def inactive_category_appointment(self, date, category_id, sub_categories):
        query = """ 
        select
            distinct(sub_category)
        from 
            ec_booked_slot_record
        where
          state = 'Booked'
          and
          date >= '{}'
          and
          category = {}
          and
          sub_category not in ({}) 
         """.format(date, category_id, sub_categories)

        self._cr.execute(query)
        # FIXME or TEST
        # It is to get the ids in the list instead of tuple.
        return [r[0] for r in self._cr.fetchall()]

    @staticmethod
    def get_activity_state(date):
        """
        It just checks if the date is of past or present/future.
        * If past activity_status will be inactive
        * if present/future will be active

        On the basis of this following will be decided:-
        1. If the slot if of the past then it will always be "inactive"
        2. If the slot is from present future, but it has been blocked then again it will be "inactive"

        :param date: Date for which dashboard values will be get prepared.
        :return: "Active"/"Inactive"

        """
        if date >= datetime.today().date():
            return "active"

        return "inactive"


    @api.model
    def get_slots_record_category_day_data(self, day, active_category_id, parent_category_id=None):

        block_slot_obj = self.env['ec.block.slot']

        configurator_id = None

        sub_category_name = []
        slot_record_list = []

        notification = None

        today = datetime.strptime(day, '%Y-%m-%d').date()
        day = today.weekday()
        day_name = calendar.day_name[day]

        parent_category_ids, active_parent_category_id, fetch_category, category_id =\
            self.get_relevant_categories(parent_category_id, active_category_id)

        primary_categories_data = self.get_category_required_data(parent_category_ids)
        category_data = self.get_category_required_data(fetch_category)

        if not category_data:
            notification = 'No Category Found!'
        else:
            if not category_id:  # Although this should not trigger
                notification = 'No Category Found!'
            else:
                active_category_id = category_id.id

                category_configurator = self.env['ec.slot.configurator'].search([
                    ('category', '=', category_id.id),
                    ('state', '!=', 'draft'),
                    ('start_date', '<=', today),
                    '|', ('end_date', '>=', today),
                    ('end_date', '=', None)
                ])

                if not category_configurator.sub_category:
                    notification = 'No Sub-Categories Found!'
                else:
                    sub_cat_list = str(category_configurator.sub_category.ids)[1:-1]
                    total_records = self.inactive_category_appointment(today, active_category_id, sub_cat_list)

                    sub_categories_total = category_configurator.sub_category

                    if total_records:  # If in-active categories after some time so dashboard in past should show that.
                        sub_categories = self.env['ec.slot.sub.category'].search([
                            ('id', 'in', total_records),
                        ])
                        sub_categories_total = category_configurator.sub_category + sub_categories

                    sub_category_name = self.get_sub_categories_data(sub_categories_total)

                    # It will prepare the block_slot data for the day for the required sub_categories
                    block_slot_obj.prepare_block_slot_data(categories=sub_categories_total.ids, date=today)

                    configurator_id = category_configurator.id
                    if not category_configurator:
                        notification = "Configuration Setting for " + str(category_id.name) + " category is not added."
                    else:
                        day_schedule = self.env['ec.slot.schedule'].search([
                            ('day', '=', day),
                            ('configurator', '=', category_configurator.id)
                        ])
                        if not day_schedule:
                            # notification = 'Schedule is not added for the day in configurator.'
                            pass
                        else:
                            for rec in day_schedule:
                                hour, minute = CustomDateTime.convert_to_time(rec.active_time)
                                start = CustomDateTime.convert_to_datetime(today, hour, minute)
                                end_hour, end_minute = CustomDateTime.convert_to_time(rec.to_time)
                                end = CustomDateTime.convert_to_datetime(today, end_hour, end_minute)
                                # time_difference = end - start
                                timespan = category_configurator.timespan
                                while start <= end:
                                    start_time = CustomDateTime.get_only_time(start)
                                    end_time = CustomDateTime.get_only_time(start + timedelta(minutes=timespan))

                                    slot_list = []
                                    slot_record = {
                                        'start_time': start_time,
                                        'end_time': end_time,
                                        'category_id': category_id.id,
                                    }
                                    for value in sub_categories_total:
                                        booked_slots = self.env['ec.booked.slot.record'].search_slots(start_time,
                                                                                                      end_time,
                                                                                                      today,
                                                                                                      category_id.id,
                                                                                                      value.id)

                                        if booked_slots:
                                            slots = {'locationId': 1,
                                                     'status': booked_slots.state,
                                                     'booked_slot_id': booked_slots.id,
                                                     'patient_name': booked_slots.partner_id.name,
                                                     'partner_id': booked_slots.partner_id.partner_id.id,
                                                     'patient_id': booked_slots.partner_id.id,
                                                     'email_wife': booked_slots.partner_id.email_wife,
                                                     'wife_dob': booked_slots.partner_id.wife_dob,
                                                     'wife_age': booked_slots.partner_id.wife_age,
                                                     'email_husband': booked_slots.partner_id.email_husband,
                                                     'husband_dob': booked_slots.partner_id.husband_dob,
                                                     'husband_age': booked_slots.partner_id.husband_age,
                                                     'mobile_wife': booked_slots.partner_id.mobile_wife,
                                                     'mobile_husband': booked_slots.partner_id.mobile_husband,
                                                     'patientName': booked_slots.partner_id.name,
                                                     'consultantName': booked_slots.consultant_id.name,
                                                     'comment': booked_slots.comment,
                                                     'slotCode': 'slot1',
                                                     'sub_category': value.id,
                                                     'date': today, "activity_state": Category.get_activity_state(today),
                                                     'product': booked_slots.product_id.name if booked_slots.product_id else '',
                                                     'mr_no': booked_slots.partner_id.mr_num,
                                                     'preferred_mobile': booked_slots.partner_id.preferred_mobile,
                                                     }
                                            slot_list.append(slots)
                                        else:
                                            status = "Available"

                                            activity_state = Category.get_activity_state(today)
                                            if block_slot_obj.check_slot_block(category_id=value.id,
                                                                               active_time=start_time,
                                                                               to_time=end_time,
                                                                               date=today) \
                                                    and activity_state == 'active': # and check is not mandatory at all
                                                activity_state = "inactive"

                                            # Search if the slot is not blocked
                                            slots = {'locationId': 1,
                                                     'status': status,
                                                     'patient_name': '',
                                                     'patient_id': '',
                                                     'email_wife': '',
                                                     'wife_dob': '',
                                                     'wife_age': '',
                                                     'email_husband': '',
                                                     'husband_dob': '',
                                                     'husband_age': '',
                                                     'mobile_wife': '',
                                                     'mobile_husband': '',
                                                     'patientName': '',
                                                     'consultantName': '',
                                                     'slotCode': 'slot1',
                                                     'sub_category': value.id,
                                                     'date': today,
                                                     'comment': '',
                                                     "activity_state": activity_state,
                                                     "product": "",
                                                     "mr_no": "",
                                                     'preferred_mobile': "",
                                                     }
                                            slot_list.append(slots)
                                    slot_record.update({'slots': slot_list})
                                    slot_record_list.append(slot_record)
                                    start += timedelta(minutes=timespan)
                                if slot_record_list:
                                    del slot_record_list[-1]

        return {
            "primary_categories": primary_categories_data,
            'active_parent_category_id': active_parent_category_id,
            'appointment_sub_categories': sub_category_name,
            'appointment_categories': category_data,
            'slot_record_list': slot_record_list,
            'notification': notification,
            'date_picker_field': today,
            'configurator_id': configurator_id,
            'day_name': day_name,
            'active_category_id': active_category_id,
            'total_appointment_categories': len(category_data)
        }


class SubCategory(models.Model):
    _name = "ec.slot.sub.category"
    _description = "Tertiary Categories"

    name = fields.Char('Name')
    description = fields.Char('Description')
    active = fields.Boolean(string='Active',
                            default=True)

    order = fields.Integer(string='Order Number')


class SubCategoryConfiguration(models.TransientModel):
    _name = "ec.slot.sub.category.configurator"
    _description = "Sub Categories Configurator"

    sub_category = fields.Many2many('ec.slot.sub.category')
    configurator = fields.Many2one('ec.slot.configurator')

    @api.model_create_multi
    def create(self, vals_list):
        res = super(SubCategoryConfiguration, self).create(vals_list)
        deleted_sub_config_ids = list(set(res.configurator.sub_category.ids) - set(res.sub_category.ids))
        if deleted_sub_config_ids:
            affected_appointments = self.env['ec.booked.slot.record'].search([
                        ('configurator', '=', res.configurator.id),
                        ('sub_category', 'in', deleted_sub_config_ids),
                        ('date', '>=', datetime.now())
                    ])
            if affected_appointments:
                for rec in affected_appointments:
                    rec.state = 'Rescheduled Required'
                    rec.configurator = res.configurator.id

        res.configurator.write({
            'sub_category': [(6, 0, res.sub_category.ids)]
        })
        return res
