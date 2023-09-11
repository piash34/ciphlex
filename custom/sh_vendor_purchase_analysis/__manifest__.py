# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Vendor Purchase Analysis Report",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Purchases",
    "summary": "Purchase Order Analysis,PO Analysis Report,RFQ Analysis Report,Request For Quotation Analysis Report,Product Analysis Report,Analyze Vendor Performance,Purchase Stock Analysis,Purchase Product Analysis Ciphlex",
    "description": """In this module, you can generate and print vendor's purchase analysis reports in PDF as well as excel format. You can generate reports between any date range. Purchase orders & products, Report can be generated using these both options. You can also generate a report based on the status of the purchase order/RFQ.""",
    "version": "16.0.2",
    "depends": [
        'purchase'
    ],
    "data": [
        'security/ir.model.access.csv',
        'report/sh_report_purchase_analysis_templates.xml',
        'wizard/sh_vendor_purchase_analysis_wizard_views.xml',
        'views/sh_vendor_purchase_analysis_views.xml',
    ],
    "images": ["static/description/background.png", ],
    "license": "OPL-1",
    "application": True,
    "auto_install": False,
    "installable": True,
    "price": 25,
    "currency": "EUR"
}
