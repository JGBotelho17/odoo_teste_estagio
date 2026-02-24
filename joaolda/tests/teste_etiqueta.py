from odoo.tests.common import TransactionCase
from odoo import fields

class TestEtiquetaSemana(TransactionCase):
    def setUp(self):
        super().setUp()
        self.stage_qual = self.env['crm.stage'].search([('name','ilike','qualificat')], limit=1)
        if not self.stage_qual:
            self.stage_qual = self.env['crm.stage'].create({'name':'Qualificado'})
        self.lead = self.env['crm.lead'].create({'name':'Test','stage_id':self.stage_qual.id})

    def test_create_etiqueta_on_stage(self):
        self.assertTrue(self.lead.etiqueta_id)
        week = fields.Date.context_today(self.env.user).isocalendar()[1]
        self.assertEqual(self.lead.etiqueta_id.name, f'W/{week}')

    def test_change_stage_assign(self):
        other = self.env['crm.stage'].search([('id','!=',self.stage_qual.id)], limit=1) or self.stage_qual
        lead2 = self.env['crm.lead'].create({'name':'Another','stage_id':other.id})
        lead2.stage_id = self.stage_qual
        self.assertEqual(lead2.etiqueta_id.name, f'W/{week}')
        etiquetas = self.env['joaolda.etiqueta.nsemana'].search([('name','=',f'W/{week}')])
        self.assertEqual(len(etiquetas), 1)