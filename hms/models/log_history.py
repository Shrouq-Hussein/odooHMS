from odoo import  fields , models ,api
from datetime import date


class Log(models.Model):
    _name = 'hms.log_history'
    _description = 'hms patients log history model'
    _rec_name ='description'

    #created_by = fields.Char()
    description = fields.Char()
    #date = fields.Date(default=date.today())

    patient = fields.Many2one("hms.patients")
    #@api.model
    #def create(self, vals):
     #   print(f"vals={vals}")
      #  log = super(Log, self).create(vals)
       # return log





