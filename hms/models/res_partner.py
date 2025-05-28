from odoo import fields , models ,api
from odoo.exceptions import ValidationError , UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string="Related Patient")

    @api.constrains('email')
    def _check_email_not_in_patients(self):
        Patient = self.env['hms.patient']
        for rec in self:
            if rec.email:
                patient=Patient.search([('email','=',rec.email)], limit=1)
                if patient :
                    raise  ValidationError("This email address is already linked to a patient and cannot be used for this customer.")


    @api.model
    def unlink(self):
        for rec in self :
            if rec.related_patient_id:
                raise UserError("You cannot delete a customer linked to a patient.")
        return super(ResPartner, self).unlink()

    # @api.constrains('vat', 'customer_rank')
    # def _check_tax_id_for_customers(self):
    #     for rec in self:
    #         if rec.customer_rank > 0:
    #             if not rec.vat:
    #                 raise ValidationError("The Tax ID (VAT) field is mandatory for CRM Customers.")
