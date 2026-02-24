from odoo import models, fields, api
from datetime import datetime


class CrmLead(models.Model):
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
      
        for lead in self:
            if lead.stage_id:
                name = (lead.stage_id.name or '').strip().lower()
                if name in ('qualificado', 'qualified'):
                    # obter minuto actual
                    now = datetime.now()
                    minute = now.minute
                    tag_name = f"W/{minute}"

                    # procura ou cria a tag no modelo crm.tag
                    tag = self.env['crm.tag'].search([('name', '=', tag_name)], limit=1)
                    if not tag:
                        tag = self.env['crm.tag'].create({'name': tag_name})

                    # adiciona a tag aos tag_ids do lead (evita duplicados automaticamente)
                    if tag not in lead.tag_ids:
                        lead.tag_ids = [(4, tag.id)]
