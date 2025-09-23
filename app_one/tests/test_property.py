from odoo.tests.common import TransactionCase
from odoo import fields


class TestProperty(TransactionCase):

    def setUp(self, *args , **kwargs):
        super(TestProperty,self).setUp()

        self.property_01_record = self.env['property'].create({
            'name': 'Test Villa',
            'description': 'Nice villa with garden',
            'postcode': '44556',
            'expected_price': 500000.0,
            'selling_price': 450000.0,
            'bedrooms': 3,
            'date_availability': fields.Date.today(),
            'living_area': 150.0,
            'garage': True,
            'garden': True,
            'garden_orientation': 'east',
            'garden_area': 50.0,
        })


    def test_01_property_values(self):
        property_id= self.property_01_record

        self.assertRecordValues(property_id,[{
            'name': 'Test Villa',
            'description': 'Nice villa with garden',
            'postcode': '44556',
            'expected_price': 500000.0,
            'selling_price': 450000.0,
            'bedrooms': 3,
            'date_availability': fields.Date.today(),
            'living_area': 150.0,
            'garage': True,
            'garden': True,
            'garden_orientation': 'east',
            'garden_area': 50.0,
        }])
