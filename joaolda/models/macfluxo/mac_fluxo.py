from odoo import models, fields, api


class MacFluxo(models.Model):
    _name = 'mac.analitica'
    _description = 'MacFluxo'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Descricao do Registo', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Parceiro Relacionado', tracking=True)
    x_studio_ca = fields.Many2one(
        'account.analytic.account',
        string='Conta Analitica Principal',
        ondelete='set null',
    )

    line_ids = fields.One2many(
        'account.analytic.line',
        'mac_analitica_id',
        string='Linhas Analiticas Relacionadas'
    )

    def api_get_analytic_lines(self):
        """Metodo para API: retorna apenas as linhas analiticas do registo."""
        self.ensure_one()
        return self.line_ids.read([
            'id',
            'name',
            'date',
            'amount',
            'unit_amount',
            'account_id',
            'partner_id',
            'company_id',
            'currency_id',
        ])

    @api.model
    def api_list_analytic_lines(self, domain=None, limit=100):
        """Metodo para API: lista registos mac.analitica com apenas linhas analiticas."""
        records = self.search(domain or [], limit=limit)
        return [
            {
                'mac_analitica_id': rec.id,
                'analytic_lines': rec.api_get_analytic_lines(),
            }
            for rec in records
        ]


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    mac_analitica_id = fields.Many2one('mac.analitica', string='Registo Mac')
