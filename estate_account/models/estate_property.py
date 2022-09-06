from odoo import fields, models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"
    
    def do_sold(self):
        res = super().do_sold()  # we do this first because we want the property 
                                 # to be set sold first -> create invoice
        journal = self.env["account.move"].with_context(default_move_type='out_invoice')._get_default_journal()
        
        for record in self:
            self.env["account.move"].create({'partner_id': record.buyer.id,
                                            'move_type': 'out_invoice',
                                            'journal_id': journal.id,
                                            'invoice_line_ids':[
                                                Command.create({
                                                    'name': record.name,
                                                    'quantity': 1.,
                                                    'price_unit': record.selling_price * 0.06
                                                }),
                                                Command.create({
                                                    'name': 'Administrative fees',
                                                    'quantity': 1.,
                                                    'price_unit': 100.
                                                })]})
        
        return res