# -*- coding: utf-8 -*-
{
    'name': "op_batch_free",

    'summary': """
        Module để tạo và quản lý các lớp học miền phí""",

    'description': """
        Module để tạo và quản lý các lớp học miền phí
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/op_batch_free.xml',
        'views/op_request_join_batch.xml',
        'security/op_batch_free_security.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}