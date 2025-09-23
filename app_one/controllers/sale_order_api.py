from odoo import http
from odoo.http import request


class Sale(http.Controller):

    @http.route('/my_sale_details' , type="http", auth='public', website=True)
    def get_sale_orders(self, **kwargs):
        sale_details = request.env['sale.order'].sudo().search([])
        return request.render('app_one.sale_details_page',{'details':sale_details})

    @http.route('/new_request_submit' , type="http" , auth='public' , website=True ,csrf=True)
    def request_submit(self, **kwargs):
        def request_submit(self, **kwargs):
            # استلام البيانات من الفورم
            st_name = kwargs.get('st_name')

            if st_name:
                # إنشاء طلب بيع جديد
                request.env['sale.order'].sudo().create({
                    'name': st_name,
                    'partner_id': request.env['res.partner'].sudo().search([], limit=1).id,
                    # هنا جبت أول عميل كـ test – ممكن تخليه ياخد ID من الفورم
                })

            # بعد ما يخلص الإنشاء يرجع للصفحة الرئيسية
            return request.redirect('/my_sale_details')
