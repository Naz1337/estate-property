from datetime import datetime
from odoo import fields, models, api, exceptions
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Holding offers!"
    _sql_constraints = [
        ("pos_off_price", "CHECK (price > 0)", "Offering Price must be above zero!")]
    _order = "price desc"
    
    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False)
    partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    property_id = fields.Many2one(comodel_name="estate.property", required=True)
    
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_set_deadline")
    
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type", related="property_id.property_type", string="Property Type", store=True)
    
    
    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date == False:
                record.date_deadline = (datetime.now() + relativedelta(days=record.validity)).date()
            else:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
    
    # @api.depends("create_date", "validity")
    def _set_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days
            
    def do_accept(self):
        for record in self:
            record.property_id.selling_price = record.price
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            
            record.property_id.buyer = record.partner_id
            
            for offer in self.property_id.mapped("offer_ids"):
                if offer == record:
                    continue
                
                offer.status = "refused"

        return True

    def do_reject(self):
        for record in self:
            record.status = "refused"
            for offer in record.property_id.mapped("offer_ids"):
                if offer.status == "accepted":
                    break
            else:
                record.property_id.state = "offer_received"
            
            if record.property_id.buyer == record.partner_id:
                record.property_id.buyer = False

            # record.property_id.selling_price = 0.
        return True
    
    @api.model
    def create(self, vals: dict):
        # vals -> {'price': 600,
        # 'partner_id': 26, 'validity': 7, 
        # 'date_deadline': '2022-09-12', 
        # 'status': False, 'property_id': 12}
        max_offer_price = max(offer.price for offer in self.env["estate.property"].browse(vals['property_id']).offer_ids)
        
        if vals['price'] < max_offer_price:  # TODO: use odoo float util
            raise exceptions.UserError(f"Can not offer less than the current highest offer! {max_offer_price}")
        return super().create(vals)
    