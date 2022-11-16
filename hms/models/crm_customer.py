from odoo import  fields , models , api
from odoo.exceptions import  UserError, ValidationError
from odoo.addons.crm.models.res_partner import Partner
class CRMCustomer(models.Model):
    _inherit = 'res.partner'
    related_patient_id = fields.One2many("hms.patients","linked_customer")
    vat = fields.Char(required=True) #Tax id

    _sql_constraints = [('unique_email', 'UNIQUE (related_patient_id.email)', 'Email already assigned to customer'), ]  # added to db

    @api.constrains("related_patient_id")
    def validate_data(self):
        for record in self:
            if record.vat:
                if len(record.vat) == 0:
                    raise ValidationError('Tax id is required')


    def unlink(self): ## hold list of object
         for record in self:
             print("===== object related_patient_id ",record.related_patient_id )
             if record.related_patient_id :
                 raise UserError("Cannot delete this customer")
             super(Partner, record).unlink()
