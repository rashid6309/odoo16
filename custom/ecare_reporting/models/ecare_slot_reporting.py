from odoo import api, fields, models, _
import math

from collections import defaultdict


class EcareSlotsReporting(models.TransientModel):
    _name = 'ec.slot.reporting'
    _description = 'Slots Reporting'

    start_datetime = fields.Date(string='Start DateTime', default=fields.Date.today())
    end_datetime = fields.Date(string='End DateTime', default=fields.Date.today())
    report_name = fields.Char('Name')

    def name_get(self):
        return [(self.id, 'Slot Report')]

    ''' Slot Report is triggered from the Dashboard --> "Report" Action '''
    @api.model
    def print_slot_report(self, day_name,
                          appointment_sub_categories, slot_record_list,
                          date_picker_field, local_activeId):

        category_name_search = self.env['ec.slot.category'].browse(int(local_activeId))
        category_name = None
        if category_name_search:
            category_name = category_name_search.name
            tem_obj = self.env['ec.slot.reporting'].sudo().create(
                {'report_name': str(category_name) + " - " + str(date_picker_field)})

        total_sub_cat = len(appointment_sub_categories)
        total_slot_rec = len(slot_record_list)
        total_slots = total_sub_cat * total_slot_rec
        slot_count = 0
        list_sub_categories = []
        list_slots = []
        table = {}
        list_tables = []
        list_tables_list = []
        table_count = 0
        while total_slots != slot_count:
            table_count += 1
            sub_cat_count = 1
            sub_cat_copy = appointment_sub_categories.copy()
            for sub_cat in sub_cat_copy:
                if sub_cat_count == 3 or sub_cat == appointment_sub_categories[-1]:
                    list_sub_categories.append(sub_cat)
                    appointment_sub_categories.pop(0)
                    break
                else:
                    list_sub_categories.append(sub_cat)
                    appointment_sub_categories.pop(0)
                    sub_cat_count += 1

            for slot in slot_record_list:
                time = str(str(slot['start_time']) + ' - ' + str(slot['end_time']))
                split = 1
                slots_copy = slot['slots'].copy()
                for list_item in slots_copy:
                    slot_count += 1
                    # if list_item['sub_category'] == sub_category['sub_category_id']:
                    if split != 3 or slot_count == total_slots:
                        list_slots.append(list_item)
                        slot['slots'].pop(0)
                        split += 1
                    elif split == 3 or slot_count == total_slots:
                        list_slots.append(list_item)
                        slot['slots'].pop(0)
                        break
                table.update({'time': time})
                table.update({'slots': list_slots})
                list_slots = []
                list_tables.append(table)
                table = {}
            new_dict = {
                'sub_categories': list_sub_categories,
                'data': list_tables
            }

            list_tables_list.append(new_dict)
            list_tables = []
            list_sub_categories = []
            new_dict = {}

        slots = {
            'day_name': day_name,
            'slot_record_list': list_tables_list,
            'date_picker_field': date_picker_field,
            'category_name': category_name,
            'report_name': tem_obj.report_name,
        }
        return self.env.ref('ecare_reporting.ec_slot_report').report_action(self, data=slots)

    ''' Helper Methods '''

    def get_journals(self):
        payment_method_query = """ 
        SELECT 
            json_agg(aj.name) as journal_name 
        FROM 
            account_journal aj 
        where 
            aj."type"  in ('cash', 'bank')
            and aj.active = True;
        """
        self._cr.execute(payment_method_query)
        return self._cr.fetchone()


    @staticmethod
    def handle_single_value_tuple(value):
        if len(value) == 1 and isinstance(value[0], str):
            return "('" + str(value[0]) + "')"
        elif len(value) == 1:
            return "(" + str(value[0]) + ")"
        return value

    ''' Cash Report '''

    def cash_detail_total_count(self,
                                user_query_param,
                                date, date_end,
                                payment_mode_query_param, invoice_type_query_param):
        # Get the total number of records
        total_query = """
                    SELECT COUNT(*)
                        FROM
                    account_payment payment
                JOIN account_move move ON
                    move.id = payment.move_id
                JOIN account_move_line line ON
                    line.move_id = move.id 
                JOIN account_partial_reconcile part ON
                    part.debit_move_id = line.id
                    OR
                        part.credit_move_id = line.id
                JOIN account_move_line counterpart_line ON
                    part.debit_move_id = counterpart_line.id
                    OR
                        part.credit_move_id = counterpart_line.id
                JOIN account_move invoice ON
                    invoice.id = counterpart_line.move_id
                join account_move_line invoice_line on
                invoice.id = invoice_line.move_id
                join product_product pp
                on invoice_line.product_id   = pp.id
                join product_template pt
                on pp.product_tmpl_id  = pt.id
                JOIN account_account account ON
                    account.id = line.account_id
                join account_journal aj
                on aj.id = line.journal_id
                join res_partner rp
                on line.partner_id = rp.id
                WHERE
                    payment.write_uid in {}
                    and
                    date(payment.create_date) >= '{}'
                    and 
                    date(payment.create_date) <= '{}'
                    AND
                    account.account_type IN ('asset_receivable', 'liability_payable')
                    AND aj."name" in {} 
                    AND 
                    line.id != counterpart_line.id
                    AND invoice.move_type IN {}
                    GROUP BY payment.create_date,move."name", rp.display_name, 
                    part.amount , move.state,invoice.name,aj.name,invoice.amount_total     
            """.format(user_query_param, date, date_end, payment_mode_query_param, invoice_type_query_param)
        self._cr.execute(total_query)
        total_records = self._cr.fetchall()

        if total_records:
            return len(total_records)

        return 0

    def _get_users(self, user: int, date, date_end):

        def _get_users_list(self):
            """
            Products and Services are same words in the system.
            :return:
            """
            query = """
            select 
            ru.id, rp.display_name as name 
            from 
            res_users ru 
            inner join 
            res_partner rp on rp.id = ru.partner_id
            where 
            ru.id in (
                select distinct ap.write_uid from account_payment ap
                where date(ap.create_date) between '{}' and '{}'
                )
            order by 
                rp.display_name;
            ;
            """
            query = query.format(date, date_end)
            self._cr.execute(query)
            return self._cr.dictfetchall()

        user_list = _get_users_list(self)
        user_dropdown = EcareSlotsReporting.products_build_dropdown_values(user_list, user)
        user_dropdown_query_param = EcareSlotsReporting.handle_single_value_tuple(user_dropdown)
        return user_list, user_dropdown_query_param

    def build_cash_report_param(self, invoice_type, payment_mode, client_user_id, date, date_end):
        payment_methods = self.get_journals()

        invoice_types = ['out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt']
        invoice_types = EcareSlotsReporting.build_dropdown_values(key=invoice_type, values=invoice_types)
        payment_modes = EcareSlotsReporting.build_dropdown_values(key=payment_mode, values=payment_methods[0])

        user_list, user_query_param = self._get_users(client_user_id, date, date_end)
        invoice_type_query_param = EcareSlotsReporting.handle_single_value_tuple(invoice_types)
        payment_mode_query_param = EcareSlotsReporting.handle_single_value_tuple(payment_modes)
        return user_list, user_query_param, invoice_type_query_param, payment_mode_query_param, payment_methods


    def build_fetch_cash_report_data(self, report: bool, limit: int, offset: int,
                                     payment_mode: list, invoice_type: list,
                                     date, date_end,
                                     client_user_id: int):
        """
        :param report: True if data is being prepared for the report else 0. If False only then it'll do pagination
        :param limit:  parameter: To show
        :param offset: Pagination Parameter: To offset
        :param payment_mode: Payment mode selection not usable when report
        :param invoice_type: Invoice type: (Refund, Cancel) not usable when report
        :param date: From date
        :param date_end: End date
        :param client_user_id: For specific user not usable when report
        :return: Prepared data
        """

        user_list, user_query_param, invoice_type_query_param, payment_mode_query_param, payment_methods = \
            self.build_cash_report_param(invoice_type, payment_mode, client_user_id, date, date_end)

        total_pages = 1
        if not report:
            total_records = self.cash_detail_total_count(user_query_param,
                                                         date, date_end,
                                                         payment_mode_query_param,
                                                         invoice_type_query_param)
            # Calculate total pages
            if total_records > 0:
                total_pages = math.ceil(total_records / limit)

            query_offset = int(offset) * limit

        # Get the records with pagination
        query = """
                SELECT json_build_object(
                    'header', (SELECT json_build_array(
                        'SR.', -- Add the Serial Number column to the header
                        'Date',
                        'Patient',
                        'Payment Ref',
                        'Services',
                        'INV #',
                        'Mode',
                        'INV Amount',
                        'Settled Amount',
                        'Discount',
                        'Last Update By'
                    ) FROM account_move LIMIT 1),
                    'data', json_build_array(
                        row_number() over(),
                        to_CHAR(payment.create_date + interval '5h', 'dd-mm-yyyy HH24:MI:SS'),
                        rp.display_name,
                        move.name,
                        string_agg(pt."name"->>'en_US', '\n'),
                        invoice.name, 
                        aj."name",
                        invoice.amount_total_signed::int,
                        part.amount::int,
                        invoice_line.fixed_amount_discount,
                      	write_uid_partner.display_name
                    )
                ) AS result
            """

        query += EcareSlotsReporting.cash_flow_report_from_part_query()
        query += EcareSlotsReporting.cash_flow_where_clause_query()

        if not report:
            query +=  """ LIMIT {} -- param6
                          OFFSET {} """
            query = query.format(user_query_param,
                       date, date_end,
                       payment_mode_query_param,
                       invoice_type_query_param,
                       limit, query_offset)
        else:
            query = query.format(user_query_param,
                                 date, date_end,
                                 payment_mode_query_param,
                                 invoice_type_query_param)

        records = []
        if user_query_param:
            self._cr.execute(query)
            records = self._cr.fetchall()

        return records, total_pages, payment_methods, user_list

    @classmethod
    def cash_flow_report_from_part_query(cls):
        query = """
                FROM
                    account_payment payment
                JOIN account_move move ON
                    move.id = payment.move_id
                JOIN account_move_line line ON
                    line.move_id = move.id 
                JOIN account_partial_reconcile part ON
                    part.debit_move_id = line.id
                    OR
                        part.credit_move_id = line.id
                JOIN account_move_line counterpart_line ON
                    part.debit_move_id = counterpart_line.id
                    OR
                        part.credit_move_id = counterpart_line.id
                JOIN account_move invoice ON
                    invoice.id = counterpart_line.move_id
                join account_move_line invoice_line on
                invoice.id = invoice_line.move_id
                join product_product pp
                on invoice_line.product_id   = pp.id
                join product_template pt
                on pp.product_tmpl_id  = pt.id
                JOIN account_account account ON
                    account.id = line.account_id
                join account_journal aj
                on aj.id = line.journal_id
                join res_partner rp
                on line.partner_id = rp.id
                left join res_users ru
                on ru.id = payment.create_uid
                left join res_partner write_uid_partner
                on write_uid_partner.id = ru.partner_id  
        """
        return query

    @classmethod
    def cash_flow_where_clause_query(cls, with_group_by=True):
        query = """
                WHERE
                    payment.write_uid in {}
                    and
                    date(payment.create_date) >= '{}'
                    and 
                    date(payment.create_date) <= '{}'
                    AND
                    account.account_type IN ('asset_receivable', 'liability_payable')
                    AND aj."name" in {} 
                    AND 
                    line.id != counterpart_line.id
                    AND invoice.move_type IN {}
        """
        if with_group_by:
            query  += """
                        GROUP BY payment.create_date,move."name", rp.display_name, 
                        part.amount , move.state,invoice.name,aj.name, invoice.amount_total_signed, write_uid_partner.display_name,
                        invoice_line.fixed_amount_discount
                        order by payment.create_date desc
            """

        return query


    @api.model
    def cash_detail_report(self, limit, offset,
                           payment_mode, invoice_type,
                           date, date_end,
                           client_user_id):

        # Get the data without any pagination for summary
        without_pagination_records, total_pages, payment_methods, user_list = \
            self.build_fetch_cash_report_data(True, limit, offset,
                                              payment_mode, invoice_type,
                                              date, date_end,
                                              client_user_id)

        data = [record[0]['data'] for record in without_pagination_records]

        """
            CASH: Cash
            Online: Online
            Cards:- Debit + Credit
            Cheque/D.Draft: Cheque + D.Draft 
            Other: Rest
        """
        summary_block = defaultdict(float)

        for _, _, _, _, _, _, \
                journal5, receivable_amt6, paid_amount7, discount8,  _ in data:

            summary_block['net_amount'] += receivable_amt6  # It'll (-) the refund amount which is added later on.
            summary_block['discount'] += discount8
            summary_block['refund'] += paid_amount7 if receivable_amt6 < 0 else 0

            ''' If change keys to this than remember to change in the xml as well '''

            # if journal5 == 'Bank':
            #     summary_block['bank_amount'] += receivable_amt6
            if journal5 in ['Cheque', 'Demand Draft']:
                summary_block['cheque_amount'] += receivable_amt6
            elif journal5 == 'Online':
                summary_block['online_amount'] += receivable_amt6
            elif journal5 == 'Cash':
                summary_block['cash_amount'] += receivable_amt6
            elif journal5 in ['Credit Card', 'Debit Card']:
                summary_block['credit_amount'] += receivable_amt6
            else:
                summary_block['other'] += receivable_amt6

        summary_block['total_amount'] = summary_block['net_amount'] \
                                        + summary_block['discount'] \
                                        + abs(summary_block['refund'])

        header = []
        data = []

        if without_pagination_records:
            records, total_pages, _, _ = \
                self.build_fetch_cash_report_data(False, limit, offset,
                                                  payment_mode, invoice_type,
                                                  date, date_end,
                                                  client_user_id)

            header = [record[0]['header'] for record in records]
            data = [record[0]['data'] for record in records]

        notification = None
        if not data:
            notification = "No Record Exist."

        result = {
            'notification': notification,
            'header': header,
            'data': data,
            'date_picker_field': date,
            'date_picker_field_end': date_end,
            'payment_methods': payment_methods[0],
            'invoice_type': invoice_type,
            'payment_mode': payment_mode,
            'total_pages': total_pages,
            'active_page': offset,
            'summary_block': summary_block,
            'users_list': user_list,
            'selected_user_id': client_user_id
        }
        return result
    
    def _get_services_list(self):
        query = """
        select
            json_agg(pt."name" -> 'en_US') as values
        from
            product_template pt
        where
            pt."detailed_type" = 'service'
            and pt.active = true; 
        """
        self._cr.execute(query)
        return self._cr.fetchone()

    @staticmethod
    def _get_str_from_list(values):
        """
        It will convert the list of string to single string
        Example:
        ["Customer Invoices", "Out Refund"]

        "'Customer Invoices, 'Out Refund'"
        Purpose: To use it in the sql queries.

        :param values:
        :return:
        """
        if values:
            values = str(values)[1:-1]

        return values

    def _get_products(self, product):
        """
        Products and Services are same words in the system.
        :return:
        """
        def _get_products_list(self):
            query = """
            select
                pt.id, (pt."name" -> 'en_US') as name
            from
                product_template pt
            where
                pt."detailed_type" = 'service'
                and pt.active = true
            order by 
                pt."name" -> 'en_US'
            """

            self._cr.execute(query)
            return self._cr.dictfetchall()

        product_list = _get_products_list(self)
        product_dropdown = EcareSlotsReporting.products_build_dropdown_values(product_list=product_list,
                                                                              product_id=product)
        product_dropdown_query_param = EcareSlotsReporting.handle_single_value_tuple(product_dropdown)
        return product_list, product_dropdown_query_param

    @staticmethod
    def build_dropdown_values(key: str, values: tuple):
        """
        Refactored:
        Beforehand it was the str of values which was being used in the query, but it should be tuple instead
        :param key: from client
        :param values: Total values
        :return: value in the dropdown at client side and to be use in query next time.
        """
        KEYS = ["All Types", "All Modes", "All"]

        if key in KEYS:
            if not isinstance(values, tuple):
                values = tuple(values)

            dropdown_selected = values
        else: # Here is exception if it is not "str"
            if isinstance(key, str):
                dropdown_selected = tuple([key])
            else:
                dropdown_selected = tuple(key)

        return dropdown_selected

    @staticmethod
    def products_build_dropdown_values(product_list : list, product_id: int):
        search_product = None
        if product_id != "All":
            product_id = int(product_id)
            if product_list:
                search_product = [product for product in product_list if product.get('id') == product_id]

        if not search_product: # It means to fetch all the products list
            # build ids including all
            product_list_ids = [product.get('id', None) for product in product_list]
            dropdown_values = EcareSlotsReporting.build_dropdown_values(key="All", values=product_list_ids)
        else:
            # Here key will not be used in the build_dropdown_values
            search_product = [product.get('id', None) for product in search_product]
            dropdown_values = EcareSlotsReporting.build_dropdown_values(key=search_product, values=search_product)

        return dropdown_values

    def build_fetch_services_report_data(self, report: bool,
                                         limit: int, offset: int,
                                         payment_mode: list, invoice_type: list,
                                         date, date_end,
                                         client_product_id: int):

        payment_methods = self.get_journals()

        invoice_types = ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
        invoice_types = EcareSlotsReporting.build_dropdown_values(key=invoice_type, values=invoice_types)
        payment_modes = EcareSlotsReporting.build_dropdown_values(key=payment_mode, values=payment_methods[0])

        invoice_types_query_param = EcareSlotsReporting.handle_single_value_tuple(invoice_types)
        payment_modes_query_param = EcareSlotsReporting.handle_single_value_tuple(payment_modes)

        product_list, product_dropdown_query_param = self._get_products(client_product_id)

        total_pages = 1
        if not report:
            # Calculate total pages
            total_records = self._total_count_records(product_dropdown_query_param, date, date_end,
                                                      payment_modes_query_param, invoice_types_query_param)
            if total_records > 0:
                total_pages = math.ceil(total_records / limit)

            query_offset = int(offset) * limit

        # Get the records with pagination
        query = """
                SELECT json_build_object(
                    'header', (SELECT json_build_array(
                        'Date',
                        'Patient',
                        'Payment Ref',
                        'Services',
                        'INV #',
                        'Mode',
                        'Amount',
                        'Discount',
                        'Last Update By'
                    ) FROM account_move LIMIT 1),
                    'data', json_build_array(
                        to_CHAR(payment.create_date + interval '5h', 'dd-mm-yyyy HH24:MI:SS'),
                        rp.display_name,
                        move.name,
                        string_agg(pt."name"->>'en_US', '\n'),
                        invoice.name, 
                        aj."name",
                        -1 * invoice_line.balance::int,
                        invoice_line .fixed_amount_discount,
                        pp.id,
                      	write_uid_partner.display_name
                    )
                ) AS result
                FROM
                    account_payment payment
                JOIN account_move move ON
                    move.id = payment.move_id
                JOIN account_move_line line ON
                    line.move_id = move.id 
                JOIN account_partial_reconcile part ON
                    part.debit_move_id = line.id
                    OR
                        part.credit_move_id = line.id
                JOIN account_move_line counterpart_line ON
                    part.debit_move_id = counterpart_line.id
                    OR
                        part.credit_move_id = counterpart_line.id
                JOIN account_move invoice ON
                    invoice.id = counterpart_line.move_id
                join account_move_line invoice_line on
                invoice.id = invoice_line.move_id
                join product_product pp
                on invoice_line.product_id   = pp.id
                join product_template pt
                on pp.product_tmpl_id  = pt.id
                JOIN account_account account ON
                    account.id = line.account_id
                join account_journal aj
                on aj.id = line.journal_id
                join res_partner rp
                on line.partner_id = rp.id
                left join res_users ru
                on ru.id = payment.create_uid
                left join res_partner write_uid_partner
                on write_uid_partner.id = ru.partner_id  
                WHERE
                    pt.id IN {} -- param1
                    and
                    date(payment.create_date) >= '{}' -- param2
                    and
                    date(payment.create_date) <= '{}' -- param3
                    AND
                    account.account_type IN ('asset_receivable', 'liability_payable')
                    AND 
                    aj."name" in {}  -- param4
                    AND 
                    line.id != counterpart_line.id --param4
                    AND invoice.move_type IN {} --param5
                    GROUP by pp.id, payment.create_date,move."name", rp.display_name,
                    invoice_line.balance ,
                    move.state,invoice.name, aj.name, invoice_line.fixed_amount_discount,
                    write_uid_partner.display_name
                    order by pp.id asc, payment.create_date desc
                     
                """
        if not report:
            query += """ LIMIT {} -- param6 
                         OFFSET {} -- param7 """
            query = query.format(product_dropdown_query_param, # --param1
                       date, # --param2
                       date_end, # --param3
                       payment_modes_query_param, # --param4
                       invoice_types_query_param, # --param5
                       limit, # --param6
                       query_offset # --param7
                       )
        else:
            query = query.format(product_dropdown_query_param, # --param1
                                 date, # --param2
                                 date_end, # --param3
                                 payment_modes_query_param, # --param4
                                 invoice_types_query_param, # --param5
                                )

        self._cr.execute(query)
        records = self._cr.fetchall()
        return records, payment_methods, product_list, total_pages

    @api.model
    def services_cash_report(self, limit, offset,
                             payment_mode, invoice_type,
                             date, date_end=None,
                             client_product_id=None):

        # For summary pagination is not required
        without_pagination_records, payment_methods, product_list, total_pages = \
            self.build_fetch_services_report_data(True,
                                                  limit, offset,
                                                  payment_mode, invoice_type,
                                                  date, date_end, client_product_id)
        summary_block = defaultdict(float)

        data = [record[0]['data'] for record in without_pagination_records]

        for _, _,  _, _, _, \
                journal5, receivable_amt6,  discount8,  _,  _ in data:

            summary_block['net_amount'] += receivable_amt6  # It'll (-) the refund amount which is added later on.
            summary_block['discount'] += discount8
            summary_block['refund'] += receivable_amt6 if receivable_amt6 < 0 else 0

            ''' If change keys to this than remember to change in the xml as well '''

            # if journal5 == 'Bank':
            #     summary_block['bank_amount'] += receivable_amt6
            if journal5 in ['Cheque', 'Demand Draft']:
                summary_block['cheque_amount'] += receivable_amt6
            elif journal5 == 'Online':
                summary_block['online_amount'] += receivable_amt6
            elif journal5 == 'Cash':
                summary_block['cash_amount'] += receivable_amt6
            elif journal5 in ['Credit Card', 'Debit Card']:
                summary_block['credit_amount'] += receivable_amt6
            else:
                summary_block['other'] += receivable_amt6

        summary_block['total_amount'] = summary_block['net_amount'] \
                                        + summary_block['discount'] \
                                        + abs(summary_block['refund'])

        # Get the data with pagination --> Same query with limit and offset parameter
        header = []
        data = []

        if without_pagination_records:
            records, _, _, total_pages = \
                self.build_fetch_services_report_data(False,
                                                      limit, offset,
                                                      payment_mode, invoice_type,
                                                      date, date_end, client_product_id)

            header = [record[0]['header'] for record in records]
            data = [record[0]['data'] for record in records]

        notification = None
        if not data:
            notification = "No Record Exist."

        result = {
            'notification': notification,
            'header': header,
            'data': data,
            'date_picker_field': date,
            'date_picker_field_end': date_end,
            'payment_methods': payment_methods[0], # List of payment method
            'payment_mode': payment_mode, # Selected payment method at client side
            'invoice_type': invoice_type,
            'product_list': product_list,
            'selected_product_id': client_product_id,
            'total_pages': total_pages,
            'active_page': offset,
            'summary_block': summary_block,
        }
        return result

    def _total_count_records(self, products, date, date_end, payment_modes_query_param, invoice_types_query_param):
        total_query = """
                    SELECT COUNT(*)
                    FROM
                    account_payment payment
                    JOIN account_move move ON
                        move.id = payment.move_id
                    JOIN account_move_line line ON
                        line.move_id = move.id 
                    JOIN account_partial_reconcile part ON
                        part.debit_move_id = line.id
                        OR
                            part.credit_move_id = line.id
                    JOIN account_move_line counterpart_line ON
                        part.debit_move_id = counterpart_line.id
                        OR
                            part.credit_move_id = counterpart_line.id
                    JOIN account_move invoice ON
                        invoice.id = counterpart_line.move_id
                    join account_move_line invoice_line on
                    invoice.id = invoice_line.move_id
                    join product_product pp
                    on invoice_line.product_id   = pp.id
                    join product_template pt
                    on pp.product_tmpl_id  = pt.id
                    JOIN account_account account ON
                        account.id = line.account_id
                    join account_journal aj
                    on aj.id = line.journal_id
                    join res_partner rp
                    on line.partner_id = rp.id
                    WHERE
                        pt.id IN {} -- param1
                        AND
                        date(payment.create_date) >= '{}' -- param2
                        and
                        date(payment.create_date) <= '{}' -- param3
                        AND
                        account.account_type IN ('asset_receivable', 'liability_payable')
                        AND 
                        aj."name" in {}  -- param4
                        AND 
                        line.id != counterpart_line.id
                        AND invoice.move_type IN {} --param5
                        GROUP by pp.id, payment.create_date,move."name", rp.display_name,
                        part.amount , move.state,invoice.name,aj.name,invoice.amount_total_signed    
                """.format(products, # --param1
                           date, # --param2
                           date_end, # --param3
                           payment_modes_query_param, # --param4
                           invoice_types_query_param, # --param5
                          )
        self._cr.execute(total_query)
        total_records = self._cr.fetchall()

        if total_records:
            return len(total_records)
        return 0

    @api.model
    def amount_due_cases(self, limit, offset, report=False):
        # Get the total number of records
        total_pages = 0
        total_records = 0
        if not report:
            total_query = """
                            SELECT COUNT(*)
                            FROM
                            account_move am
                            join res_partner rp
                            on am.partner_id = rp.id
                            join account_move_line invoice_line on
                            am.id = invoice_line.move_id
                            join product_product pp on 
                            invoice_line.product_id   = pp.id
                            join product_template pt
                            on pp.product_tmpl_id  = pt.id
                            where am.payment_state = 'not_paid'
                            GROUP BY am."name", am.amount_total, rp.display_name, 
                            am.payment_state, am.state,am.invoice_date_due 
                            """

            self._cr.execute(total_query)
            total_records = self._cr.fetchall()

            # Calculate total pages
            total_pages = math.ceil(len(total_records) / limit)

        # Get the records with pagination
        query = """
                SELECT json_build_object(
                    'header', (SELECT json_build_array(
                        'Date',
                        'INV Amount',
                        'INV #',
                        'Services',
                        'Patient',
                        'Discount',
                        'Payment State'
                    ) FROM account_move LIMIT 1),
                    'data', json_build_array(
                            to_CHAR(am.create_date + interval '5h', 'dd-mm-yyyy HH24:MI:SS'),
                            am.amount_total_signed, 
                            am.name, 
                            string_agg(pt."name"->>'en_US', '\n'),
                            rp.display_name, 
                            invoice_line.fixed_amount_discount,
                            case when am.payment_state = 'not_paid' then 'Not Paid'
                            when am.payment_state = 'Paid' then 'Paid'
                            else ''
                            end
                    )
                ) AS result
                    FROM
                        account_move am
                        join res_partner rp
                        on am.partner_id = rp.id
                        join account_move_line invoice_line on
                        am.id = invoice_line.move_id
                        join product_product pp on 
                        invoice_line.product_id   = pp.id
                        join product_template pt
                        on pp.product_tmpl_id  = pt.id
                        where am.payment_state = 'not_paid'
                        GROUP BY am."name", am.amount_total_signed, rp.display_name, 
                        am.payment_state, am.state,am.create_date,
                        invoice_line.fixed_amount_discount
                        order by am.create_date desc
                """

        if not report:
            query += """ LIMIT {} OFFSET {} """
            query = query.format(limit, offset)

        self._cr.execute(query)
        records = self._cr.fetchall()

        header = [record[0]['header'] for record in records]
        data = [record[0]['data'] for record in records]

        total_amount = 0
        total_discount = 0

        for rec in data:
            total_amount += rec[1]
            total_discount += rec[5]

        notification = None
        if not data:
            notification = "No Record Exist."
        result = {
            'notification': notification,
            'header': header,
            'data': data,
            'total_records': total_records,
            'total_pages': total_pages,
            'active_page': offset,
            'total_amount': int(total_amount),
            'total_discount': int(total_discount),
        }
        return result


    """ Report Print Methods """

    @api.model
    def print_amount_due_report(self, due_payment_date):
        result = self.amount_due_cases(None, None , True)

        return self.env.ref('ecare_reporting.ec_amount_due_report').report_action(self, data=result)

    # Reports (PDF/Excel) of cash and services

    @api.model
    def print_amount_due_report_excel(self, date):
        data = {
            'date': date
        }
        return self.env.ref('ecare_reporting.ec_amount_due_excel_report').report_action(self, data=data)

        result = self.amount_due_cases(None,None , True) # TODO as we have now migrated it due cases to odoo default report.

    def get_cash_report_data(self, date, date_end, payment_mode, invoice_type, user_id):
        records, _, _, _ = self.build_fetch_cash_report_data(True, None, None, payment_mode, invoice_type, date, date_end, user_id)

        header = [record[0]['header'] for record in records]

        data = [record[0]['data'] for record in records]

        return {
            'header': header,
            'data': data,
            'payment_date': date,
            'date_end': date_end
        }

    @api.model
    def print_cash_report(self, date, date_end, payment_mode, invoice_type, user_id):
        result = self.get_cash_report_data(date, date_end, payment_mode, invoice_type, user_id)
        return self.env.ref('ecare_reporting.ec_cash_report').report_action(self, data=result)

    @api.model
    def print_cash_report_excel(self, date, date_end, payment_mode, invoice_type, user_id):
        result = self.get_cash_report_data(date, date_end, payment_mode, invoice_type, user_id)
        return self.env.ref('ecare_reporting.ec_cash_excel_report').report_action(self, data=result)

    def get_services_report_data(self, date, date_end, payment_mode, invoice_type, product_id):
        records, _, _, _ = self.build_fetch_services_report_data(True,
                                                                 None, None,
                                                                 payment_mode, invoice_type,
                                                                 date, date_end,
                                                                 product_id)

        header = [record[0]['header'] for record in records]
        data = [record[0]['data'] for record in records]

        return {
            'header': header,
            'data': data,
            'services_payment_date': date
        }

    @api.model
    def print_services_report(self, date, date_end, payment_mode, invoice_type, product_id):
        result = self.get_services_report_data(date, date_end, payment_mode, invoice_type, product_id)
        return self.env.ref('ecare_reporting.ec_services_report').report_action(self, data=result)

    @api.model
    def print_services_report_excel(self, date, date_end, payment_mode, invoice_type, product_id):
        result = self.get_services_report_data(date, date_end, payment_mode, invoice_type, product_id)
        return self.env.ref('ecare_reporting.ec_services_excel_report').report_action(self, data=result)
