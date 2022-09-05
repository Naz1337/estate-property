from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags of property!"
    _order = "name"
    
    name = fields.Char(required=True)
    color = fields.Integer()
    # property_id = fields.Many2many(comodel_name="estate.property")