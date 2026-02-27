from odoo import models, api


class MacFluxoApi(models.Model):
    _inherit = 'mac.analitica'

    def api_get_analytic_lines(self):
        """Metodo para API: retorna apenas as linhas analiticas do registo."""
        # A API foi desenhada para devolver um payload enxuto de linhas analiticas
        # sem expor todos os campos tecnicos do modelo.
        self.ensure_one()
        return self.line_ids.read([
            'id',
            'name',
            'date',
            'amount',
            'unit_amount',
            'account_id',
            'partner_id',
            'company_id',
            'currency_id',
        ])

    @api.model
    def api_list_analytic_lines(self, domain=None, limit=100):
        """Metodo para API: lista registos mac.analitica com apenas linhas analiticas."""
        # O domain vem da chamada externa; se nao vier, lista todos os registos.
        records = self.search(domain or [], limit=limit)
        return [
            {
                # Mantemos o id do cabecalho para o consumidor correlacionar com o registo mac.
                'mac_analitica_id': rec.id,
                # Reutiliza o metodo unitario para manter o contrato de payload consistente.
                'analytic_lines': rec.api_get_analytic_lines(),
            }
            for rec in records
        ]
