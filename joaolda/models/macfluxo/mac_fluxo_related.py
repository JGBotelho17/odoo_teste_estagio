from odoo import models, fields


class MacFluxoRelated(models.Model):
    _inherit = 'mac.analitica'

    # Campo related: espelha os BOMs vindos da Conta Analitica Principal.
    x_studio_bom_1 = fields.One2many(
        'mrp.bom',
        string='bom 1',
        related='x_studio_ca.x_studio_boms',
        readonly=True,
        store=False,
    )
