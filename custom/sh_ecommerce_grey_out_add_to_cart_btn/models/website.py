# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields, models

class Website(models.Model):
    _inherit="website"

    sh_disable_add_to_cart = fields.Boolean("Disable Add to cart button")
