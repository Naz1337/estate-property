from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Hold the type of a property"
    _sql_constraints = [("uniq_name", "unique(name)", "Name must be unique!")]
    
    name = fields.Char(required=True)