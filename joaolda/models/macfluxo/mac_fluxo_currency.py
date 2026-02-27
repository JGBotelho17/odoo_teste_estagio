from odoo import models, fields

class MacFluxo(models.Model):
    _inherit = 'mac.analitica' 

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )