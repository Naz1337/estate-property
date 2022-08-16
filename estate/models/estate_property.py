from odoo import models, fields, api
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
    
    total_area = fields.Integer(compute="_compute_total_area")
    
    best_price = fields.Float(compute="_compute_best_price")
    
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            if len(prices) != 0:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0
    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_orientation = "north"
            self.garden_area = 10
        else:
            self.garden_orientation = False
            self.garden_area = False