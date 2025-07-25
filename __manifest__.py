{
    'name': 'Sale Order Payments',
    'version': '18.0.1.0.0',
    'summary': 'Create customer payments from Sale Orders and link them to invoices.',
    'author': 'Mario',
    'website': '',
    'license': 'AGPL-3',
    'category': 'Sales',
    'depends': [
        'sale_management',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/account_payment_views.xml',
        'wizards/sale_make_payment_views.xml',
    ],
    'installable': True,
}