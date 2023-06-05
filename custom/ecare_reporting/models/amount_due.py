from odoo import models


class AmountDueXlsx(models.AbstractModel):
    _name = 'report.ec_reporting.amount_due_reporting'
    _inherit = 'report.report_xlsx.abstract'

    def execute_query(self, date):
        query = """
        SELECT
            to_CHAR(am.create_date + interval '5h', 'dd-mm-yyyy HH24:MI:SS'),
            am.invoice_date_due,
            am.amount_total_signed, 
            am.name, 
            string_agg(pt."name"->>'en_US', '\n'),
            rp.display_name, 
            invoice_line.fixed_amount_discount,
            case when am.payment_state = 'not_paid' then 'Not Paid'
            when am.payment_state = 'Paid' then 'Paid'
            else ''
            end
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
        """
        self._cr.execute(query)
        records = self._cr.fetchall()
        return records

    def generate_xlsx_report(self, workbook, data, lines):
        worksheet = workbook.add_worksheet(name="Amount Due Report")

        medicsi_name_format = workbook.add_format({
            'border': 1,
            'valign': 'vcenter',
            'align': 'center',
            'font_size': 16,
            'bold': True,
            'fg_color': '#C55A11',
            'font_color': 'black',
            'text_wrap': True
        })

        times_heading = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 12,
            'bold': True,
            'fg_color': '#F8CBAD',
            'font_color': 'black',
            'text_wrap': True
        })

        department_count = {
            'border': 1,
            'font_size': 10,
            'bold': 0,
            'bg_color': '#69b8b8',
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True
        }
        base_column_heads = {
            'border': 1,
            'font_size': 12,
            'bold': 1,
            'bg_color': '#F8CBAD',
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True
        }
        base_row_heads = {
            'border': 1,
            'font_size': 10,
            'bold': 0,
            'valign': 'center',

        }
        consultant_report_heading = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 12,
            'bold': True,
            'fg_color': '#F8CBAD',
            'font_color': 'black',
            'text_wrap': True
        })

        ''' Formats object initialized '''
        column_head_format = workbook.add_format(base_column_heads)
        row_head_format = workbook.add_format(base_row_heads)
        department_count_format = workbook.add_format(department_count)

        ''' Printing '''
        company_name = self.env.user.company_id.name
        row, col = 0, 0

        worksheet.set_row(row, 20)
        end_col = 6
        worksheet.merge_range(row, col, row, col + end_col, company_name, medicsi_name_format)
        row += 1
        worksheet.set_row(row, 15)
        worksheet.merge_range(row, col, row, col + end_col, "Amount Due Report ",
                              consultant_report_heading)
        # row += 1
        worksheet.set_row(row, 30)

        # worksheet.merge_range(row, col, row, col + end_col,
        #                       "For the period " + str(lines['start_datetime']) + " to " + str(
        #                           lines['end_datetime']),
        #                       times_heading)

        ''' Column widths '''
        # PAYMENT
        # REF
        # SERVICES
        # INV  MODE	INV AMOUNT	SETTLED AMOUNT	DISCOUNT	STATUS
        col = 0
        worksheet.set_column(col, col + 1, 30)  # Date
        col += 1
        worksheet.set_column(col, col, 30)  # Patient
        col += 1
        worksheet.set_column(col, col, 30)  # Payment REF
        col += 1
        worksheet.set_column(col, col, 30)  # Services
        col += 1
        worksheet.set_column(col, col, 30)  # INV #
        col += 1
        worksheet.set_column(col, col, 30)  # MODE
        col += 1
        worksheet.set_column(col, col, 30)  # INV AMOUNT
        col += 1
        worksheet.set_column(col, col, 30)  # SETTLED AMOUNT
        col += 1
        worksheet.set_column(col, col, 30)  # DISCOUNT
        col += 1
        worksheet.set_column(col, col, 30)  # STATUS

        ''' Header data  '''
        # PAYMENT
        # REF
        # SERVICES
        # INV  MODE	INV AMOUNT	SETTLED AMOUNT	DISCOUNT	STATUS
        row += 1
        col = 0
        worksheet.set_row(row, 25)
        worksheet.set_column(col, col, 20)
        worksheet.write(row, col, 'Date', column_head_format)
        col += 1
        worksheet.write(row, col, 'INV AMOUNT', column_head_format)
        col += 1
        worksheet.write(row, col, 'INV #', column_head_format)
        col += 1
        worksheet.write(row, col, 'SERVICES', column_head_format)
        col += 1
        worksheet.write(row, col, 'PATIENT', column_head_format)
        col += 1
        worksheet.write(row, col, 'DISCOUNT', column_head_format)
        col += 1
        worksheet.write(row, col, 'PAYMENT STATE', column_head_format)
        records = self.execute_query(data['date'])
        array_len = len(records)

        if records:
            for rec in records:
                col = 0
                row += 1
                worksheet.write(row, col, str(rec[0]) or "", row_head_format)
                col += 1
                worksheet.write(row, col, rec[1] or "", row_head_format)
                col += 1
                worksheet.write(row, col, rec[2] or "", row_head_format)
                col += 1
                worksheet.write(row, col, rec[3] or "", row_head_format)
                col += 1
                worksheet.write(row, col, rec[4] or "", row_head_format)
                col += 1
                worksheet.write(row, col, rec[5] or "", row_head_format)
                col += 1
                worksheet.write(row, col, rec[6] or "", row_head_format)

        workbook.close()
