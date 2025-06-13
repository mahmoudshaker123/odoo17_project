from odoo import http
from odoo.http import request
import io
import xlsxwriter
from ast import literal_eval


class XlsxPropertyReport(http.Controller):

    @http.route('/property/excel/report/<string:property_ids>', type='http', auth='user')
    def download_property_excel_report(self,property_ids):
        property_ids =request.env['property'].browse(literal_eval(property_ids))
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output ,{'in_memory':True})
        worksheet = workbook.add_worksheet('Properties')

        # Formats
        header_format = workbook.add_format({'bold':True,'bg_color':'#D3D3D3','border':1,'align':'center'})

        headers = ['Name' , 'Postcode' , 'Selling Price' ,'Garden']
        for col_num ,header in enumerate(headers):
            worksheet.write(0,col_num,header,header_format )

        workbook.close()
        output.seek(0)

        file_name ='Property Report.xlsx'

        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition',f'attachment; filename={file_name}')
            ]
        )
