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
        worksheet.set_column(col, col + columns_count, 30)

        company_name = self.env.user.company_id.name

        worksheet.set_row(row, 20)
        worksheet.merge_range(row, col, row, col + columns_count, company_name, medicsi_name_format)

        row += 1

        worksheet.set_row(row, 15)
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

        for rec in records:
            col = 0
            row += 1
            worksheet.write(row, col, str(rec[0]) or "", row_head_format)
            col += 1
            worksheet.write(row, col, rec[1].strip() if rec[1] else "", row_head_format)
            col += 1
            worksheet.write(row, col, rec[2] or "", row_head_format)
            col += 1
            worksheet.write(row, col, rec[3] or "", row_head_format)
            col += 1
            worksheet.write(row, col, rec[4] or "", row_head_format)
            col += 1
            worksheet.write(row, col, rec[5] or "", row_head_format)
            col += 1
            worksheet.write(row, col, rec[6] or 0, amount_row_format)
            col += 1
            worksheet.write(row, col, rec[7] or 0, amount_row_format)
            col += 1
            worksheet.write(row, col, rec[8] or 0, amount_row_format)
            col += 1
            worksheet.write(row, col, rec[9] or "", row_head_format)

        workbook.close()
