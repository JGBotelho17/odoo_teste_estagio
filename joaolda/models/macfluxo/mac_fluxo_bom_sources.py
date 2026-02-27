from odoo import models, fields


class AccountAnalyticAccountMacFlow(models.Model):
    _inherit = 'account.analytic.account'

    x_studio_boms = fields.One2many(
        'mrp.bom',
        'analytic_account_id',
        string='BOMs',
    )


class MrpBomMacFlow(models.Model):
    _inherit = 'mrp.bom'

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytical Account',
        help='Analytical Account for the BOM',
        ondelete='set null',
        index=True,
        copy=True,
    )
