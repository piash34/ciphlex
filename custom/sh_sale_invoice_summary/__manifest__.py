# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Sales Invoice Summary Report",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Sales",
    "summary": "Sale Invoice Summary Excel,Quotation Summary Report,Sales Report,Customer Invoice Summary Report,Invoice Analysis Report,Payment Summary Report,Manage Customer Invoice,Sale Receipt Report,Print Invoice Summary XLS,Invoice Summary PDF Odoo",
    "description": """This module helps to generate and print sales invoice summary reports of customers in PDF as well as excel format. You can generate reports between any date range. You can generate reports based on invoice status. We provide the option to print reports of more than one company.""",
    "version": "16.0.2",
    "depends": [
        'sale_management'
    ],
    "data": [
        'security/ir.model.access.csv',
        'security/sh_sale_invoice_summary_groups.xml',
        'report/sh_sale_invoice_summary_report_templates.xml',
        'wizard/sh_sale_invoice_summary_wizard_views.xml',
        'views/sh_sale_invoice_summary_views.xml',
    ],
    "images": ["static/description/background.png", ],
    "license": "OPL-1",
    "application": True,
    "auto_install": False,
    "installable": True,
    "price": 25,
    "currency": "EUR"
}
