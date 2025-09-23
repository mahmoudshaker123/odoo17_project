from odoo import http
from odoo.http import Response
import json

class TestApi(http.Controller):

    @http.route('/api/test', auth='public', type='http', methods=['GET'], csrf=False)
    def test_endpoint(self, **kw):
        return Response(json.dumps({"message": "Hello from Odoo"}), content_type='application/json')
