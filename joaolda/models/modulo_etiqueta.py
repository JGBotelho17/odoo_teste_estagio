from odoo import models, fields, api
import datetime


# helper functions are kept inside methods below when needed


class JoaoLdaEtiqueta(models.Model):
    """Etiqueta que identifica a semana do ano em que uma oportunidade foi qualificada.

    A tag é criada automaticamente na primeira vez que alguma oportunidade entra no
    estágio Qualificado. Se já existir uma etiqueta com o nome correspondente à
    semana em curso, ela será reutilizada (não se criam duplicados).
    """

    _name = 'joaolda.etiqueta.nsemana'
    _description = 'Etiqueta por número de semana'
    _order = 'name desc'

    name = fields.Char(string='Etiqueta', required=True, copy=False)
    week_number = fields.Integer(string='Número da Semana', compute='_compute_week_number', store=True)
    observacoes = fields.Text(string='Observações')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Já existe uma etiqueta com este nome.'),
    ]

    @api.depends('name')
    def _compute_week_number(self):
        for rec in self:
            if rec.name and '/' in rec.name:
                try:
                    rec.week_number = int(rec.name.split('/')[1])
                except ValueError:
                    rec.week_number = 0
            else:
                rec.week_number = 0

    def get_or_create_this_week(self):
        """Retorna a etiqueta da semana atual ou cria uma nova se necessário."""
        # compute week number based on today's date in the record's context
        today = fields.Date.context_today(self)
        week = today.isocalendar()[1]
        name = f"W/{week}"
        etiqueta = self.search([('name', '=', name)], limit=1)
        if not etiqueta:
            etiqueta = self.create({'name': name})
        return etiqueta


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    etiqueta_id = fields.Many2one('joaolda.etiqueta.nsemana', string='Etiqueta', readonly=True)

    @api.model
    def create(self, vals):
        lead = super(CrmLead, self).create(vals)
        lead._assign_etiqueta_if_qualified()
        return lead

    def write(self, vals):
        res = super(CrmLead, self).write(vals)
        if 'stage_id' in vals:
            self._assign_etiqueta_if_qualified()
        return res

    def _assign_etiqueta_if_qualified(self):
        """Atribui a etiqueta da semana atual quando o lead entra em estágio qualificado.

        O nome do estágio pode estar em português ou inglês, por isso aceitamos
        qualquer uma das variações mais comuns.
        """
        for lead in self:
            if lead.stage_id:
                name = (lead.stage_id.name or '').strip().lower()
                if name in ('qualificado', 'qualified'):
                    etiqueta = self.env['joaolda.etiqueta.nsemana'].get_or_create_this_week()
                    lead.etiqueta_id = etiqueta
