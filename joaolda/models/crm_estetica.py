from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # Campo padrão do Odoo para cores no Kanban (inteiro)
    color = fields.Integer(string="Cor", compute="_compute_kanban_color", store=True)
    
    # Mantemos o teu campo de nível se quiseres usar em filtros
    poupanca_cor = fields.Selection([
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta')
    ], compute="_compute_poupanca_cor", string="Nível de Poupança", store=True  )

    @api.depends('poupanca_anual_estimada')
    def _compute_kanban_color(self):
        for record in self:
            if record.poupanca_anual_estimada >= 2000:
                record.color = 10  # Verde em Odoo
            elif record.poupanca_anual_estimada >= 500:
                record.color = 2   # Laranja em Odoo
            else:
                record.color = 0   # Sem cor (Cinza/Branco)

    @api.depends('poupanca_anual_estimada')
    def _compute_poupanca_cor(self):
        for record in self:
            if record.poupanca_anual_estimada >= 2000:
                record.poupanca_cor = 'alta'
            elif record.poupanca_anual_estimada >= 500:
                record.poupanca_cor = 'media'
            else:
                record.poupanca_cor = 'baixa'