from odoo import  fields , models , api

class Department(models.Model):
    _name = 'hms.departments'
    _description = 'hms departments model'


    name = fields.Char()
    is_opened = fields.Boolean()
    department_capacity = fields.Integer()
    patients = fields.One2many("hms.patients","department")



    @api.onchange('patients')
    def calc_department_capacity(self):
        if self.patients:
            print("===========================",len(self.patients))
            self.department_capacity = len(self.patients)
            return {
            "warning": {
                "title": "change dept capacity",
                "message": "department capacity changed"
            }
            }


