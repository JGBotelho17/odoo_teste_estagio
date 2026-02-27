from odoo import models, fields


class AccountAnalyticLineLink(models.Model):
    _inherit = 'account.analytic.line'

    mac_analitica_id = fields.Many2one('mac.analitica', string='Registo Mac')
