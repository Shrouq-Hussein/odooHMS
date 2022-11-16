from odoo import  fields , models

class Doctor(models.Model):
    _name = 'hms.doctors'
    _description = 'hms doctor model'
    _rec_name ='first_name'

    first_name = fields.Char()
    last_name = fields.Char()
    image = fields.Image()
    patients = fields.Many2many("hms.patients")