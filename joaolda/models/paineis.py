from odoo import models, fields, api

class JoaoLdaPainel(models.Model):
    _name = 'joaolda.painel'
    _description = 'Registo de Painéis Solares'

    name = fields.Char(string='Modelo do Painel', required=True)
    marca = fields.Char(string='Marca')
    potencia_watts = fields.Integer(string='Potência (W)')
    garantia_anos = fields.Integer(string='Garantia (Anos)', default=25)
    notas = fields.Text(string='Observações Técnicas')

    # Campos de Preço
    preco_custo = fields.Float(string='Preço de Custo', default=0.0)
    
    preco_venda_sem_iva = fields.Float(
        string='Venda (Margem 8%)', 
        compute='_compute_precos', 
        store=True
    )
    
    preco_venda_com_iva = fields.Float(
        string='Venda com IVA (23%)', 
        compute='_compute_precos', 
        store=True
    )

    @api.depends('preco_custo')
    def _compute_precos(self):
        for record in self:
            # Margem de 8% -> Preço Custo * 1.08
            venda_sem_iva = record.preco_custo * 1.08
            record.preco_venda_sem_iva = venda_sem_iva
            
            # IVA de 23% sobre o preço com margem
            record.preco_venda_com_iva = venda_sem_iva * 1.23