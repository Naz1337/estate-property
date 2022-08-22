from datetime import datetime
from odoo import fields, models, api
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Holding offers!"
    _sql_constraints = [
        ("pos_off_price", "CHECK (price > 0)", "Offering Price must be above zero!")]
    
    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False)
    partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    property_id = fields.Many2one(comodel_name="estate.property", required=True)
    
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_set_deadline")
    
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
            
            record.property_id.buyer = record.partner_id
            
            for offer in self.mapped("property_id.offer_ids"):
                if offer == record:
                    continue
                
                offer.status = "refused"

        return True

    def do_reject(self):
        for record in self:
            record.status = "refused"
            
            if record.property_id.buyer == record.partner_id:
                record.property_id.buyer = False

            # record.property_id.selling_price = 0.
        return True
    