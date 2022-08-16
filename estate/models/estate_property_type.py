from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Hold the type of a property"
    
    name = fields.Char(required=True)