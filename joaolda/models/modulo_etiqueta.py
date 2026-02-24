from odoo import models, fields, api
import datetime


class CrmLead(models.Model):
    """Herança do CRM para adicionar automatismo de etiqueta semanal.
    
    Quando um lead entra no estágio 'Qualificado', uma tag W/<semana> é 
    automaticamente criada (se não existir já) e adicionada ao campo 
    'tag_ids' (Etiquetas) do Odoo nativo.
    """
    _inherit = 'crm.lead'

    @api.model
    def create(self, vals):
        lead = super(CrmLead, self).create(vals)
        lead._assign_tag_if_qualified()
        return lead

    def write(self, vals):
        res = super(CrmLead, self).write(vals)
        if 'stage_id' in vals:
            self._assign_tag_if_qualified()
        return res

    def _assign_tag_if_qualified(self):
        """Atribui a tag/etiqueta da semana atual quando o lead entra no estágio qualificado.

        O nome do estágio pode estar em português ('Qualificado') ou inglês ('Qualified').
        Usa o modelo nativo 'crm.tag' e adiciona a tag ao campo 'tag_ids' do lead.
        """
        for lead in self:
            if lead.stage_id:
                name = (lead.stage_id.name or '').strip().lower()
                if name in ('qualificado', 'qualified'):
                    # compute week number based on today's date
                    today = fields.Date.context_today(self)
                    week = today.isocalendar()[1]
                    tag_name = f"W/{week}"

                    # procura ou cria a tag no modelo crm.tag
                    tag = self.env['crm.tag'].search([('name', '=', tag_name)], limit=1)
                    if not tag:
                        tag = self.env['crm.tag'].create({'name': tag_name})

                    # adiciona a tag aos tag_ids do lead (evita duplicados automaticamente)
                    if tag not in lead.tag_ids:
                        lead.tag_ids = [(4, tag.id)]
