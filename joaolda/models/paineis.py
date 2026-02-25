from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    telhado_m2 = fields.Float(string="Área do Telhado (m²)")
    consumo_mensal_kwh = fields.Float(string="Consumo Mensal (kWh)")
    orientacao = fields.Selection([
        ('sul', 'Sul (Ideal)'), ('norte', 'Norte'), ('este', 'Este'), ('oeste', 'Oeste')
    ], string="Orientação Solar", default='sul')

    paineis_estimados = fields.Integer(string="Qtd. Painéis", compute="_compute_estudo_solar", store=True)
    potencia_instalada_kwp = fields.Float(string="Potência (kWp)", compute="_compute_estudo_solar", store=True)
    poupanca_anual_estimada = fields.Float(string="Poupança Anual (€)", compute="_compute_estudo_solar", store=True)
    
    poupanca_cor = fields.Selection([
        ('baixa', 'Baixa'), ('media', 'Média'), ('alta', 'Alta')
    ], string="Nível de Poupança", compute="_compute_poupanca_cor", store=True)

    @api.depends('telhado_m2', 'consumo_mensal_kwh')
    def _compute_estudo_solar(self):
        for record in self:
            qtd = int((record.telhado_m2 * 0.8) / 1.7) if record.telhado_m2 > 0 else 0
            record.paineis_estimados = qtd
            record.potencia_instalada_kwp = qtd * 0.45
            producao = record.potencia_instalada_kwp * 1500
            record.poupanca_anual_estimada = producao * 0.20

    @api.depends('poupanca_anual_estimada')
    def _compute_poupanca_cor(self):
        for record in self:
            if record.poupanca_anual_estimada > 1000: record.poupanca_cor = 'alta'
            elif record.poupanca_anual_estimada > 500: record.poupanca_cor = 'media'
            else: record.poupanca_cor = 'baixa'