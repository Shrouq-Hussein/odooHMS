from odoo import  fields , models ,api
from . import log_history
import re
from odoo.exceptions import ValidationError
from datetime import  date



"""
#notes:-
readonly  -> won't saved in db

"""

class Patient(models.Model):
    _name = 'hms.patients'
    _description = 'hms patients model'
    _rec_name ='first_name'

    first_name = fields.Char()
    last_name = fields.Char()
    birthdate = fields.Date()
    blood_type = fields.Selection([('A','A'),('B','B'),('AB','AB'),('O','O')])
    pcr = fields.Boolean()
    address = fields.Char()
    age = fields.Integer(compute="_cal_age",store=True)
    image = fields.Image()
    history = fields.Html()
    cr_ratio = fields.Float()

    department = fields.Many2one("hms.departments")
    department_capacity = fields.Integer(related="department.department_capacity")
    doctors = fields.Many2many("hms.doctors")

    state = fields.Selection([('undetermined','undetermined'),('good','good'),('fair','fair'),('serious','serious')],default='undetermined')
    log_history = fields.One2many("hms.log_history","patient")
    email = fields.Char()

    linked_customer = fields.Many2one("res.partner")



    _sql_constraints = [('unique_email', 'UNIQUE (email)', 'Email already exists'), ]  #added to db
    def change_state(self):

        states=["undetermined","good","fair","serious"]
        current_state_index=states.index(self.state)
        try:
            self.state=states[current_state_index+1]

        except:
            self.state=states[0]
        finally:
            self.env["hms.log_history"].create({
                "description": f"state changed to {self.state}",
                "patient": self.id
            })


    @api.onchange('state')
    def state_changed(self):
            print("sttttttttate changed", self.state)
            self.env["hms.log_history"].create({
                "description" :f"state changed to {self.state}",
                 "patient":self.id
            })

            return {
                "warning": {
                    "title": "state changed",
                    "message": "state changed"
                }
            }

    @api.onchange('age')
    def check_pcr(self):
        if self.age > 30:
            self.pcr = True
            return {
            "warning": {
                "title": "checked pcr",
                "message": "PCR checked"
            }
            }

    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError('Not a valid E-mail')


    @api.constrains("email") #for more complex constraints , not added to dbase constraints
    def validate_data(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                print("invalid email  .... transaction rolled back")
                raise ValidationError('Not a valid E-mail')

    @api.depends('birthdate')
    def _cal_age(self):
        print("calllageee")
        for record in self:
            print(record)
            if record.birthdate:
                print(record.birthdate)
                today = date.today()
                record.age = today.year - record.birthdate.year
