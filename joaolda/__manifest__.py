{
    'name': 'Gestão de Painéis Solares - JoaoLda',
    'version': '1.0',
    'category': 'Sales',
    'author': 'Joao Botelho',
    'depends': ['base', 'crm', 'sale_management', 'account', 'mrp', 'project'],

    'data': [
        'security/ir.model.access.csv',
        'views/paineis_views.xml',
        'views/etiqueta_views.xml',
        'views/estetica_views.xml',
        'views/teste_flow_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}