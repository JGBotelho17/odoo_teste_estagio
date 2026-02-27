from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    x_studio_ca = fields.Many2one(
        'account.analytic.account',
        string='Conta analitica',
        related='account_id',
        store=True,
        readonly=False,
    )
    x_studio_bom_1 = fields.One2many(
        'mrp.bom',
        string='Lista de BOM',
        related='x_studio_ca.x_studio_boms',
        readonly=True,
        store=False,
    )
    x_studio_milestones = fields.One2many(
        'project.milestone',
        string='Lista de Milestones',
        related='x_studio_ca.project_ids.milestone_ids',
        readonly=True,
        store=False,
    )
    mac_is_client = fields.Boolean(string='Cliente')
    mac_expected_qty = fields.Float(string='Quantidade Esperada')
    mac_expected_amount = fields.Float(string='Valor Esperado')
    mac_expected_date = fields.Date(string='Data esperada')
    mac_final_due_date = fields.Date(string='Data Vencimento Final')
    mac_payment_end_date = fields.Date(string='Data Final do Pagamento')
    mac_payment_state = fields.Selection(
        [
            ('pending', 'Pendente'),
            ('paid', 'Pago'),
        ],
        string='Estado do pagamento',
        default='pending',
    )
    mac_balance = fields.Float(string='Balanco', compute='_compute_mac_balance')

    @api.depends('amount')
    def _compute_mac_balance(self):
        for line in self:
            line.mac_balance = line.amount or 0.0

    def _mac_api_payload(self):
        self.ensure_one()
        return {
            'cliente': self.mac_is_client,
            'linha_analitica': self.name or '',
            'quantidade': self.unit_amount or 0.0,
            'quantidade_esperada': self.mac_expected_qty or 0.0,
            'parceiro': self.partner_id.display_name or '',
            'currency': self.currency_id.name or '',
            'valor': self.amount or 0.0,
            'valor_esperado': self.mac_expected_amount or 0.0,
            'estado_de_pagamento': self.mac_payment_state or '',
            'conta_analitica': self.x_studio_ca.display_name or '',
            'data_final_do_pagamento': self.mac_payment_end_date or False,
            'balanco': self.mac_balance or 0.0,
            'data_criacao': self.create_date or False,
            'data_vencimento_final': self.mac_final_due_date or False,
            'data_esperada': self.mac_expected_date or False,
        }

    @api.model
    def api_list_registos_analiticos(self, domain=None, limit=100):
        records = self.search(domain or [], limit=limit)
        return [record._mac_api_payload() for record in records]

    def api_get_registo_analitico(self):
        self.ensure_one()
        return self._mac_api_payload()
