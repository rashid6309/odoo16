from odoo import models


class CashDetailXlsx(models.AbstractModel):
    _name = 'report.ec_reporting.cash_detail_reporting'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        worksheet = workbook.add_worksheet(name="Cash Detail Report")

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

        report_heading = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 12,
            'bold': True,
            'fg_color': '#F8CBAD',
            'font_color': 'black',
            'text_wrap': True
        })

        base_column_heads = {
            'border': 1,
            'font_size': 12,
            'bold': 1,
            'bg_color': '#F8CBAD',
            'align': 'left',
            'valign': 'vcenter',
            'text_wrap': True
        }
        base_row_heads = {
            'border': 1,
            'font_size': 10,
            'bold': 0,
            'valign': 'center',
            'align': 'left',

        }

        amount_row_format_config = {
            'border': 1,
            'font_size': 10,
            'bold': 0,
            'valign': 'center',
            'align': 'right',
            'num_format': '#,##0',
        }

        ''' Formats object initialized '''
        column_head_format = workbook.add_format(base_column_heads)
        row_head_format = workbook.add_format(base_row_heads)
        amount_row_format = workbook.add_format(amount_row_format_config)

        ''' Least Required Data for Printing '''
        column_heads = None
        if header := data.get('header'):  # Its 2D array but is 1D so that's why.
            column_heads = header[0]

        if not column_heads:  # If not return just as than it's not possible to print the report.
            return

        ''' Total columns '''
        columns_count = len(column_heads) - 1

        ''' Printing '''


        ''' Column widths '''
        # Column Heads: Date, Patient, Payment Ref, Services, INV #, Mode, INV Amount, Settled Amount, Discount, Status, Last Update By
        # Header

        row, col = 0, 0
        worksheet.set_column(col+1, col + columns_count, 30)

        company_name = self.env.user.company_id.name

        worksheet.set_row(row, 20)
        worksheet.merge_range(row, col, row, col + columns_count, company_name, medicsi_name_format)

        row += 2
        col = 1
        worksheet.write(row, col, 'TOTAL INVOICE', column_head_format)
        col += 1
        worksheet.write(row, col, 'DISCOUNT', column_head_format)
        col += 1
        worksheet.write(row, col, 'REFUND', column_head_format)
        col += 1
        worksheet.write(row, col, 'NET AMT', column_head_format)
        row += 1
        col = 1
        worksheet.write(row, col, data['summary_block'].get('total_amount') or 0, amount_row_format)
        col += 1
        worksheet.write(row, col, data['summary_block'].get('discount') or 0, amount_row_format)
        col += 1
        worksheet.write(row, col, data['summary_block'].get('refund') or 0, amount_row_format)
        col += 1
        worksheet.write(row, col, data['summary_block'].get('net_amount') or 0, amount_row_format)
        row += 1
        col = 1
        worksheet.write(row, col, 'CASH', column_head_format)
        col += 1
        worksheet.write(row, col, 'BY CHEQUE/D.DRAFT', column_head_format)
        col += 1
        worksheet.write(row, col, 'BY C.CARD/D. CARD', column_head_format)
        col += 1
        worksheet.write(row, col, 'ONLINE', column_head_format)
        col += 1
        worksheet.write(row, col, 'OTHERS', column_head_format)
        row += 1
        col = 1
        worksheet.write(row, col, data['summary_block'].get('cash_amount') or 0, amount_row_format)
        col += 1
        worksheet.write(row, col, data['summary_block'].get('cheque_amount') or 0, amount_row_format)
        col += 1
        worksheet.write(row, col, data['summary_block'].get('credit_amount') or 0, amount_row_format)
        col += 1
        worksheet.write(row, col, data['summary_block'].get('online_amount') or 0, amount_row_format)
        col += 1
        worksheet.write(row, col, data['summary_block'].get('other') or 0, amount_row_format)

        row += 2
        col = 0

        # worksheet.set_row(row, 15)
        worksheet.merge_range(row, col, row, col + columns_count, "Cash Detail Report ", report_heading)

        worksheet.set_row(row, 30)


        ''' Header data  '''
        row += 1
        col = 0

        worksheet.set_row(row, 25)
        for column in column_heads:
            worksheet.write(row, col, column, column_head_format)
            col += 1

        if not data.get('data'):
            return

        records = data['data']  # Same it is also in 2D which is not required but still.

        for sr, date, patient, payment_ref, product_name, invoice, \
                journal5, receivable_amt6, paid_amount7, discount8,  last_updated_by in records:
            row += 1

            col = 0
            worksheet.write(row, col, sr or "", row_head_format)
            col += 1
            worksheet.write(row, col, date or "", row_head_format)
            col += 1
            worksheet.write(row, col, patient.strip() if patient else "", row_head_format)
            col += 1
            worksheet.write(row, col, payment_ref or "", row_head_format)
            col += 1
            worksheet.write(row, col, product_name or "", row_head_format)
            col += 1
            worksheet.write(row, col, invoice or "", row_head_format)
            col += 1
            worksheet.write(row, col, journal5 or "", row_head_format)
            col += 1
            worksheet.write(row, col, receivable_amt6 or "", row_head_format)
            col += 1
            worksheet.write(row, col, paid_amount7 or 0, amount_row_format)
            col += 1
            worksheet.write(row, col, discount8 or 0, amount_row_format)
            col += 1
            worksheet.write(row, col, last_updated_by or 0, amount_row_format)

        workbook.close()
