{
    'name': 'Gestão de Painéis Solares - JoaoLda',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'JoaoLda - Paineis Solares',
    'author': 'Joao Botelho',
    'depends': ['base', 'sale_management', 'stock', 'crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/paineis_views.xml',
        'views/etiqueta_views.xml',
    ],
    'installable': True,
    'application': True,
}