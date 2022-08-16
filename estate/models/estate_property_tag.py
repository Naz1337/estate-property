from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags of property!"
    
    name = fields.Char(required=True)
    # property_id = fields.Many2many(comodel_name="estate.property")