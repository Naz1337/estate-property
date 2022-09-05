from email.policy import default
from typing import Iterable
from odoo import fields, models, api
from .estate_property import EstateProperty

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Hold the type of a property"
    _sql_constraints = [("uniq_name", "unique(name)", "Name must be unique!")]
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="property_type")
    sequence = fields.Integer("Sequence", default=1)
    
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_type_id")
    offer_count = fields.Integer(compute='_compute_offer_count')
    
    @api.depends("property_ids")
    def _compute_offer_count(self):
        for record in self:
            properties: Iterable[EstateProperty] = record.mapped("property_ids")
            
            offer_count = 0
            for property in properties:
                offer_count += len(property.mapped("offer_ids"))
            
            record.offer_count = offer_count
            
