# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields


class VendorPurchaseAnalysisOrderReport(models.Model):
    _name = 'sh.vendor.purchase.analysis.order'
    _description = 'Vendor Analysis Order'

    name = fields.Char(string='Order Number')
    date_order = fields.Date(string='Order Date')
    user_id = fields.Many2one(
        'res.users', string='Purchase Representative')
    sh_partner_id = fields.Many2one(
        'res.partner', string='Vendor')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                  self: self.env.user.company_id.currency_id.id)
    purchase_amount = fields.Monetary()
    amount_paid = fields.Monetary()
    balance = fields.Monetary()


class VendorPurchaseAnalysisProductReport(models.Model):
    _name = 'sh.vendor.purchase.analysis.product'
    _description = 'Vendor Analysis Product'

    name = fields.Char(string='Order Number')
    date_order = fields.Date(string='Date')
    sh_partner_id = fields.Many2one(
        'res.partner', string='Vendor')
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                  self: self.env.user.company_id.currency_id.id)
    sh_product_id = fields.Many2one(
        comodel_name='product.product', string='Product')
    price = fields.Monetary()
    quantity = fields.Float()
    tax = fields.Float()
    subtotal = fields.Monetary()
