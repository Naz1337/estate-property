from email.policy import default
from odoo import models, fields
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "The model of a property!"
    
    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda _: fields.Date.today() + relativedelta(months=2))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly =True, copy=False)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[("north", "North"), ("south", "South"),
                   ("east", "East"), ("west", "West")])
    state = fields.Selection(
        selection=[("new", "New"), ("offer_received", "Offer Received"),
                   ("offer_accepted", "Offer Accepted"), ("sold", "Sold"),
                   ("canceled", "Canceled")],
        default="new")
    
    active = fields.Boolean(default=True, string="isActive?")
    
    buyer = fields.Many2one(comodel_name="res.partner")
    salesperson = fields.Many2one(comodel_name="res.users", string="Salesman", default=lambda self: self.env.user)
    
    tag_ids = fields.Many2many(comodel_name="estate.property.tag", string="Tags")
    
    offer_ids = fields.One2many(comodel_name="estate.property.offer",inverse_name="property_id", string="Offers")
    