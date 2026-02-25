from odoo import models, fields, api

class TesteFlow(models.Model):
    _name = 'teste.flow'
    _description = 'Fluxo de Teste'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Adicionado para suporte a mensagens/chatter

    name = fields.Char(string="Descrição", required=True)
    partner_id = fields.Many2one('res.partner', string="Cliente")
    x_studio_ca = fields.Many2one('account.analytic.account', string="Conta Analítica")

    # One2many: O 2º argumento é o campo Many2one definido nas classes abaixo
    x_studio_milestones = fields.One2many('project.milestone', 'x_studio_testeflow_id', string="Milestones")
    x_studio_bom_1 = fields.One2many('mrp.bom', 'x_studio_testeflow_id', string="BoMs")

    @api.model_create_multi
    def create(self, vals_list):
        records = super(TesteFlow, self).create(vals_list)
        for record in records:
            record.action_generate_analytic_account()
        return records

    def action_generate_analytic_account(self):
        for record in self:
            if not record.x_studio_ca:
                ca = self.env['account.analytic.account'].create({
                    'name': f"CA - {record.name}",
                })
                record.x_studio_ca = ca.id
            
            # Atualiza os registos filhos com a nova Conta Analítica
            if record.x_studio_bom_1:
                record.x_studio_bom_1.write({'analytic_account_id': record.x_studio_ca.id})
            
            if record.x_studio_milestones:
                record.x_studio_milestones.write({'x_studio_ca_id': record.x_studio_ca.id})

# --- EXTENSÕES DOS MODELOS NATIVOS ---

class ProjectMilestone(models.Model):
    _inherit = 'project.milestone'
    x_studio_testeflow_id = fields.Many2one('teste.flow', string="Fluxo Origem")
    x_studio_ca_id = fields.Many2one('account.analytic.account', string="Conta Analítica")

class MrpBom(models.Model):
    _inherit = 'mrp.bom'
    x_studio_testeflow_id = fields.Many2one('teste.flow', string="Fluxo Origem")