from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    x_name = fields.Char(
        string='Nome',
        related='name',
        store=True,
        readonly=False,
    )
    x_studio_ca = fields.Many2one(
        'account.analytic.account',
        string='Conta analitica',
        related='account_id',
        store=True,
        readonly=False,
    )
    x_studio_analytic_line = fields.One2many(
        'account.analytic.line',
        string='Linhas Analiticas',
        compute='_compute_x_studio_analytic_line',
        readonly=True,
        store=False,
    )
    x_studio_cliente = fields.Boolean(
        string='Cliente',
        related='mac_is_client',
        store=True,
        readonly=False,
    )
    x_studio_linha_analitica = fields.Many2one(
        'account.analytic.line',
        string='Linha analitica',
        compute='_compute_x_studio_linha_analitica',
        store=True,
        readonly=True,
    )
    x_studio_quantidade = fields.Float(
        string='Quantidade',
        related='unit_amount',
        store=True,
        readonly=False,
    )
    x_studio_quantidade_esperada = fields.Float(
        string='Quantidade esperada',
        related='mac_expected_qty',
        store=True,
        readonly=False,
    )
    x_studio_parceiro = fields.Many2one(
        'res.partner',
        string='Parceiro',
        related='partner_id',
        store=True,
        readonly=False,
    )
    x_studio_currency_1 = fields.Many2one(
        'res.currency',
        string='Currency',
        related='currency_id',
        store=True,
        readonly=False,
    )
    x_currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='currency_id',
        store=True,
        readonly=False,
    )
    x_studio_valor = fields.Monetary(
        string='Valor',
        related='amount',
        currency_field='x_currency_id',
        store=True,
        readonly=False,
    )
    x_studio_valor_esperado = fields.Float(
        string='Valor esperado',
        related='mac_expected_amount',
        store=True,
        readonly=False,
    )
    x_studio_estado_do_pagamento = fields.Selection(
        [('pending', 'Pendente'), ('paid', 'Pago')],
        string='Estado do pagamento',
        related='mac_payment_state',
        store=True,
        readonly=False,
    )
    x_studio_conta_analitica = fields.Many2one(
        'account.analytic.account',
        string='Conta analitica',
        related='x_studio_ca',
        store=True,
        readonly=False,
    )
    x_studio_data_final_do_pagamento = fields.Date(
        string='Data final do pagamento',
        related='mac_payment_end_date',
        store=True,
        readonly=False,
    )
    x_studio_balano = fields.Float(
        string='Balanco',
        related='mac_balance',
        store=True,
        readonly=True,
    )
    x_studio_data = fields.Date(
        string='Data criacao',
        compute='_compute_x_studio_data',
        store=True,
        readonly=True,
    )
    x_studio_data_vencimento_final = fields.Date(
        string='Data vencimento final',
        related='mac_final_due_date',
        store=True,
        readonly=False,
    )
    x_studio_data_esperada = fields.Date(
        string='Data esperada',
        related='mac_expected_date',
        store=True,
        readonly=False,
    )
    x_studio_bom_1 = fields.One2many(
        'mrp.bom',
        string='Lista de BOM',
        related='account_id.x_studio_boms',
        readonly=True,
        store=False,
    )
    x_studio_milestones = fields.One2many(
        'project.milestone',
        string='Lista de Milestones',
        compute='_compute_x_studio_milestones',
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

    @api.depends('account_id')
    def _compute_x_studio_analytic_line(self):
        AnalyticLine = self.env['account.analytic.line']
        for line in self:
            if line.account_id:
                # Lista "Linhas Analiticas": traz todas as linhas que partilham a mesma conta analitica.
                line.x_studio_analytic_line = AnalyticLine.search([
                    ('account_id', '=', line.account_id.id),
                ])
            else:
                line.x_studio_analytic_line = AnalyticLine.browse()

    @api.depends('account_id')
    def _compute_x_studio_milestones(self):
        Milestone = self.env['project.milestone'].sudo()
        Project = self.env['project.project'].sudo()
        # Em alguns ambientes existem campos custom (x_plan*) no projeto com conta analitica.
        # Descobrimos dinamicamente todos os many2one para account.analytic.account.
        analytic_m2o_fields = [
            fname for fname, f in Project._fields.items()
            if getattr(f, 'type', None) == 'many2one'
            and getattr(f, 'comodel_name', None) == 'account.analytic.account'
        ]
        for line in self:
            if line.account_id:
                # Suporta tanto account_id como campos de plano analitico (ex.: x_plan*)
                domain = []
                for idx, fname in enumerate(analytic_m2o_fields):
                    if idx:
                        # Monta OR dinamico: (f1=conta) OR (f2=conta) OR ...
                        domain.insert(0, '|')
                    domain.append((fname, '=', line.account_id.id))

                projects = Project.search(domain) if domain else Project.browse()
                milestones_from_projects = Milestone.search([
                    ('project_id', 'in', projects.ids),
                ]) if projects else Milestone.browse()

                # Fallback pelo relacionamento do proprio account (project_ids -> milestone_ids)
                milestones_from_account = line.account_id.sudo().project_ids.mapped('milestone_ids')

                # Uniao dos dois caminhos para evitar listas vazias por diferencas de modelagem.
                line.x_studio_milestones = (milestones_from_projects | milestones_from_account)
            else:
                line.x_studio_milestones = Milestone.browse()

    @api.depends('name')
    def _compute_x_studio_linha_analitica(self):
        for line in self:
            line.x_studio_linha_analitica = line

    @api.depends('create_date')
    def _compute_x_studio_data(self):
        for line in self:
            # A API externa espera date (sem hora), por isso convertemos de create_date (datetime).
            line.x_studio_data = fields.Date.to_date(line.create_date) if line.create_date else False

    def _mac_api_payload(self):
        self.ensure_one()
        # Contrato central de resposta para integrações externas.
        # Mantemos chaves em PT e valores "seguros" para evitar None inesperado no consumidor.
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
        # Endpoint de listagem: aplica filtros opcionais e devolve payload padronizado por registo.
        records = self.search(domain or [], limit=limit)
        return [record._mac_api_payload() for record in records]

    def api_get_registo_analitico(self):
        # Endpoint unitario: garante que a resposta vem de um unico registo.
        self.ensure_one()
        return self._mac_api_payload()
