# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    auto_send_mail_customer_invoice = fields.Boolean(string="Auto Customer Invoice send by Email")
    auto_validate_customer_invoice = fields.Boolean(string="Automatic Validate Customer Invoice from Delivery")
    auto_send_mail_vendor_bill = fields.Boolean(string="Auto Vendor Bill send by Email")
    auto_validate_vendor_bill = fields.Boolean(string="Automatic Validate Vendor Bill from Receipt")



class ConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    auto_send_mail_customer_invoice = fields.Boolean(readonly=False,related='company_id.auto_send_mail_customer_invoice',string="Auto Customer Invoice send by Email")
    auto_validate_customer_invoice = fields.Boolean(readonly=False,related='company_id.auto_validate_customer_invoice',string="Automatic Validate Customer Invoice from Delivery")
    auto_send_mail_vendor_bill = fields.Boolean(readonly=False,related='company_id.auto_send_mail_vendor_bill',string="Auto Vendor Bill send by Email")
    auto_validate_vendor_bill = fields.Boolean(readonly=False,related='company_id.auto_validate_vendor_bill',string="Automatic Validate Vendor Bill from Receipt")



