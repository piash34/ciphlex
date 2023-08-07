# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class Picking(models.Model):
    _inherit = "stock.picking"

    @api.depends('state')
    def _get_invoiced(self):
        for order in self:
            invoice_ids = self.env['account.move'].search([('picking_id','=',order.id)])
            order.invoice_count = len(invoice_ids)
    invoice_count = fields.Integer(string='# of Invoices', compute='_get_invoiced')
    
    def button_view_invoice(self):
        mod_obj = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']
        work_order_id = self.env['account.move'].search([('picking_id', '=', self.id)])
        inv_ids = []
        action = self.env.ref('account.action_move_out_invoice_type').sudo().read()[0]
        context = {
            'default_move_type': work_order_id[0].move_type,
        }
        action['domain'] = [('id', 'in', work_order_id.ids)]
        action['context'] = context
        return action

    
    def _action_done(self):
        action = super(Picking, self)._action_done()
    
        res_config = self.env.company
        if len(self) == 1:
            for picking in self:
                if picking.state == 'done':          
                    if picking.picking_type_id.code == 'incoming':
                        model_id = self.env['ir.model'].sudo().search([('model','=','purchase.order')])
                        is_po_avail_fields = self.env['ir.model.fields'].sudo().search([('name','=','l10n_in_gst_treatment'),('model_id','=',model_id.id)])
                        pur_order  =  self.env['purchase.order'].search([('name', '=',picking.origin)])
                            
                        account_inv_obj = self.env['account.move']
                        journal = self.env['account.journal'].search([('type','=','purchase')],limit=1)
                        if not journal:
                            raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (picking.company_id.name, picking.company_id.id))
                        if self._context.get('flag') == True:
                            for record in self.purchase_ids:
                                if pur_order:
                                    vals  = {
                                    'move_type': 'in_invoice', 
                                    'invoice_origin':record.name ,
                                    'pur_id':picking.purchase_id.id ,
                                    'journal_id': journal.id,  
                                    'purchase_id': picking.purchase_id.id,
                                    'partner_id': picking.partner_id.id,
                                    'picking_id': picking.id ,
                                    'invoice_date':picking.date_done
                                    }
                                    if is_po_avail_fields:
                                        if record.l10n_in_gst_treatment:
                                            vals['l10n_in_gst_treatment'] = record.l10n_in_gst_treatment
                                        
                                    res = account_inv_obj.create(vals)
                                    po_lines = record.order_line
                                    new_lines = self.env['account.move.line']
                                    new_lines = []
                                    for line in po_lines.filtered(lambda l: not l.display_type):
                                        new_lines.append((0,0,line._prepare_account_move_line(res)))                      
                                    res.write({
                                        'invoice_line_ids' : new_lines,
                                        'purchase_id' : False
                                        })               
                                    for inv in res:
                                        if res_config.auto_validate_vendor_bill == True:
                                            inv.action_post()
                                        if self._context.get('validate') == True and self._context.get('flag') == True:
                                                inv.action_post()    
                                        if res_config.auto_validate_vendor_bill == True and res_config.auto_send_mail_vendor_bill == True:
                                            template = self.env.ref('account.email_template_edi_invoice', False)            
                                            send = inv.with_context(force_send=True,model_description='Invoice').message_post_with_template(int(template),email_layout_xmlid="mail.mail_notification_paynow") 
                        else: 
                            if pur_order:
                                vals  = {
                                    'move_type': 'in_invoice', 
                                    'invoice_origin':picking.origin ,
                                    'pur_id':picking.purchase_id.id ,
                                    'journal_id': journal.id,  
                                    'purchase_id': picking.purchase_id.id,
                                    'partner_id': picking.partner_id.id,
                                    'picking_id': picking.id,
                                    'invoice_date':picking.date_done,

                                
                                }
                                if is_po_avail_fields:
                                    if picking.purchase_id.l10n_in_gst_treatment:
                                        vals['l10n_in_gst_treatment'] = picking.purchase_id.l10n_in_gst_treatment
                
                                
                                res = account_inv_obj.create(vals)
                                
                                po_lines = picking.purchase_id.order_line
                                new_lines = self.env['account.move.line']
                                new_lines = []
                                for line in po_lines.filtered(lambda l: not l.display_type):
                                    new_lines.append((0,0,line._prepare_account_move_line(res)))                      
                                res.write({
                                    'invoice_line_ids' : new_lines,
                                    'purchase_id' : False
                                    })               
                                for inv in res:
                                    if res_config.auto_validate_vendor_bill == True:
                                        inv.action_post()
                                    if self._context.get('validate') == True and self._context.get('flag') == True:
                                            inv.action_post()    
                                    if res_config.auto_validate_vendor_bill == True and res_config.auto_send_mail_vendor_bill == True:
                                        template = self.env.ref('account.email_template_edi_invoice', False)            
                                        send = inv.with_context(force_send=True,model_description='Invoice').message_post_with_template(int(template),email_layout_xmlid="mail.mail_notification_paynow")

                        for purchase_line in account_inv_obj.invoice_line_ids:
                            if purchase_line.quantity <= 0:
                                purchase_line.unlink()
                    if picking.picking_type_id.code == 'outgoing':
                        if picking.origin:
                            pass
                        else:
                            picking.update({'origin': self._context.get('default_origin')})    
                        inv_obj = self.env['account.move']
                        invoice_lines =[]
                        invoice_vals = []
                        sale_order_line_obj = self.env['account.move.line']
                        sale_order  =  self.env['sale.order'].search([('name', '=',picking.origin)])
                        journal = self.env['account.move'].with_context(default_move_type='out_invoice')._search_default_journal()
                        model_id = self.env['ir.model'].sudo().search([('model','=','sale.order')])
                        is_avail_fields = self.env['ir.model.fields'].sudo().search([('name','=','l10n_in_gst_treatment'),('model_id','=',model_id.id)])
                        if not journal:
                            raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (picking.company_id.name, picking.company_id.id))
                        
                        if sale_order:
                            vals  = {
                                'invoice_origin': picking.origin,
                                'picking_id':picking.id,
                                'move_type': 'out_invoice',
                                'ref': False,
                                'sale_id':sale_order.id,
                                'ref':sale_order.client_order_ref,
                                'partner_id': sale_order.partner_invoice_id.id,
                                'currency_id': sale_order.pricelist_id.currency_id.id,
                                'invoice_payment_term_id': sale_order.payment_term_id.id,
                                'fiscal_position_id': sale_order.fiscal_position_id.id or sale_order.partner_id.property_account_position_id.id,
                                'team_id': sale_order.team_id.id,
                                'invoice_date' : fields.Datetime.now().date(),
                                'partner_shipping_id':sale_order.partner_shipping_id.id,
                            }
                            
                            
                            

                            if is_avail_fields:
                                if record.l10n_in_gst_treatment:
                                    vals['l10n_in_gst_treatment'] = record.l10n_in_gst_treatment
                                    
                            invoice = inv_obj.create(vals)
                            
                            
                            for so_line in  sale_order.order_line :
                                if so_line.product_id:
                                    if so_line.product_id.type == "service":
                                        if so_line.product_uom_qty != so_line.qty_invoiced:
                                            if so_line.product_id.property_account_income_id:
                                                account_id = so_line.product_id.property_account_income_id
                                            elif so_line.product_id.categ_id.property_account_income_categ_id:
                                                account_id = so_line.product_id.categ_id.property_account_income_categ_id                    
                                            elif journal.default_account_id:
                                                account_id = journal.default_account_id
                                            else:
                                                raise UserError(_('Please define an account for the Product/Category.'))
                                            inv_line = {
                                                    'name': so_line.name,
                                                    'product_id': so_line.product_id.id,
                                                    'product_uom_id': so_line.product_id.uom_id.id,
                                                    'quantity': so_line.product_uom_qty,
                                                    'account_id': account_id.id,
                                                    'tax_ids': [(6, 0, so_line.tax_id.ids)],
                                                    'move_id':invoice.id,
                                                    'price_unit': so_line.price_unit,
                                                    'sale_line_ids': [(4, so_line.id)],
                                                    }
                                            invoice_vals.append((0,0,inv_line))
                                            so_line.write({
                                                'qty_to_invoice':so_line.product_uom_qty
                                            })                                
                                    else:
                                        if so_line.product_id.property_account_income_id:
                                            account = so_line.product_id.property_account_income_id
                                        elif so_line.product_id.categ_id.property_account_income_categ_id:
                                            account = so_line.product_id.categ_id.property_account_income_categ_id
                                        else:
                                            account = self.env['ir.property']._get('property_account_income_categ_id', 'product.category')
                                        if not account :
                                            raise UserError(_('Please define an account for the Product/Category.'))
    
                                        route = self.env['stock.location'].search([('name','=','Dropship')])
                                        if self._context.get('flag') == True and route.id in so_line.product_id.route_ids.ids:
                                            pass
                                        else:
                                            if so_line.product_id.invoice_policy == 'delivery':  
                                                for i in picking.move_ids_without_package.filtered(lambda x : x.sale_line_id == so_line and x.product_id == so_line.product_id and x.state == 'done'):
                                                    inv_line = {
                                                            'name': so_line.name,
                                                            'product_id': so_line.product_id.id,
                                                            'product_uom_id': so_line.product_id.uom_id.id,
                                                            'quantity': i.quantity_done,
                                                            'account_id': account.id,
                                                            'tax_ids': [(6, 0, so_line.tax_id.ids)],
                                                            'move_id':invoice.id,
                                                            'price_unit': so_line.price_unit,
                                                            'sale_line_ids': [(4, so_line.id)],
                                                            }
                                                    invoice_vals.append((0,0,inv_line))

                                                    so_line.write({'qty_to_invoice':so_line.product_uom_qty})
                                            else:
                                                inv_line = {
                                                        'name': so_line.name,
                                                        'product_id': so_line.product_id.id,
                                                        'product_uom_id': so_line.product_id.uom_id.id,
                                                        'quantity': so_line.product_uom_qty,
                                                        'account_id': account.id,
                                                        'tax_ids': [(6, 0, so_line.tax_id.ids)],
                                                        'move_id':invoice.id,
                                                        'price_unit': so_line.price_unit,
                                                        'sale_line_ids': [(4, so_line.id)],
                                                        } 
                                                invoice_vals.append((0,0,inv_line))
                                                
                                                so_line.write({'qty_to_invoice':so_line.product_uom_qty}) 
                                                                   
                            invoice.write({
                                'invoice_line_ids' : invoice_vals
                            })
                            if res_config.auto_validate_customer_invoice == True :
                                invoice.action_post()    
                            if res_config.auto_validate_customer_invoice == True and res_config.auto_send_mail_customer_invoice == True:
                                template = self.env.ref('account.email_template_edi_invoice', False)            
                                send = invoice.with_context(force_send=True,model_description='Invoice').message_post_with_template(int(template),email_layout_xmlid="mail.mail_notification_paynow")

            return action


class StockImmediateTransferInherit(models.TransientModel):
    _inherit = "stock.immediate.transfer"


    def process(self):
        res = super(StockImmediateTransferInherit, self).process()
        res_config = self.env.company
        pickings_to_do = self.env['stock.picking']
        pickings_not_to_do = self.env['stock.picking']
        for line in self.immediate_transfer_line_ids:
            if line.to_immediate is True:
                pickings_to_do |= line.picking_id
            else:
                pickings_not_to_do |= line.picking_id
        if len(pickings_to_do) > 1:

            for picking in pickings_to_do:
                if picking.state == 'done':            
                    if picking.picking_type_id.code == 'incoming':
                        model_id = self.env['ir.model'].search([('model','=','purchase.order')])
                        is_po_avail_fields = self.env['ir.model.fields'].search([('name','=','l10n_in_gst_treatment'),('model_id','=',model_id.id)])
                        pur_order  =  self.env['purchase.order'].search([('name', '=',picking.origin)])
                            
                        account_inv_obj = self.env['account.move']
                        journal = self.env['account.journal'].search([('type','=','purchase')],limit=1)
                        if not journal:
                            raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (picking.company_id.name, picking.company_id.id))
                        if self._context.get('flag') == True:
                            for record in self.purchase_ids:
                                if pur_order:

                                    vals  = {
                                    'move_type': 'in_invoice', 
                                    'invoice_origin':record.name ,
                                    'pur_id':picking.purchase_id.id ,
                                    'journal_id': journal.id,  
                                    'purchase_id': picking.purchase_id.id,
                                    'partner_id': picking.partner_id.id,
                                    'picking_id': picking.id,
                                    'invoice_date':picking.date_done

                                    }
                                    if is_po_avail_fields:
                                        if record.l10n_in_gst_treatment:
                                            vals['l10n_in_gst_treatment'] = record.l10n_in_gst_treatment
                                    
                                    res = account_inv_obj.create(vals)
                                    po_lines = record.order_line
                                    new_lines = self.env['account.move.line']
                                    new_lines = []
                                    for line in po_lines.filtered(lambda l: not l.display_type):
                                        new_lines.append((0,0,line._prepare_account_move_line(res)))                      
                                    res.write({
                                        'invoice_line_ids' : new_lines,
                                        'purchase_id' : False
                                        })               
                                    for inv in res:
                                        if res_config.auto_validate_invoice == True:
                                            inv.action_post()
                                        if self._context.get('validate') == True and self._context.get('flag') == True:
                                                inv.action_post()    
                                        if res_config.auto_validate_invoice == True and res_config.auto_send_mail_invoice == True:
                                            template = self.env.ref('account.email_template_edi_invoice', False)            
                                            send = inv.with_context(force_send=True,model_description='Invoice').message_post_with_template(int(template),email_layout_xmlid="mail.mail_notification_paynow") 
                        else: 
                            if pur_order:

                                vals  = {
                                    'move_type': 'in_invoice', 
                                    'invoice_origin':picking.origin ,
                                    'pur_id':picking.purchase_id.id ,
                                    'journal_id': journal.id,  
                                    'purchase_id': picking.purchase_id.id,
                                    'partner_id': picking.partner_id.id,
                                    'picking_id': picking.id,
                                    'invoice_date':picking.date_done
     
                                }
                                if is_po_avail_fields:
                                    if picking.purchase_id.l10n_in_gst_treatment:
                                        vals['l10n_in_gst_treatment'] = picking.purchase_id.l10n_in_gst_treatment
                                
                                res = account_inv_obj.create(vals)
                                
                                
                                po_lines = picking.purchase_id.order_line
                                new_lines = self.env['account.move.line']
                                new_lines = []
                                for line in po_lines.filtered(lambda l: not l.display_type):
                                    new_lines.append((0,0,line._prepare_account_move_line(res)))                      
                                res.write({
                                    'invoice_line_ids' : new_lines,
                                    'purchase_id' : False
                                    })               
                                for inv in res:
                                    if res_config.auto_validate_invoice == True:
                                        inv.action_post()
                                    if self._context.get('validate') == True and self._context.get('flag') == True:
                                            inv.action_post()    
                                    if res_config.auto_validate_invoice == True and res_config.auto_send_mail_invoice == True:
                                        template = self.env.ref('account.email_template_edi_invoice', False)            
                                        send = inv.with_context(force_send=True,model_description='Invoice').message_post_with_template(int(template),email_layout_xmlid="mail.mail_notification_paynow")

                        for purchase_line in account_inv_obj.invoice_line_ids:
                            if purchase_line.quantity <= 0:
                                purchase_line.unlink()
                    if picking.picking_type_id.code == 'outgoing':
                        if picking.origin:
                            pass
                        else:
                            picking.update({'origin': self._context.get('default_origin')})    
                        inv_obj = self.env['account.move']
                        invoice_lines =[]
                        invoice_vals = []
                        sale_order_line_obj = self.env['account.move.line']
                        sale_order  =  self.env['sale.order'].search([('name', '=',picking.origin)])
                        journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
                        model_id = self.env['ir.model'].sudo().search([('model','=','sale.order')])
                        is_avail_fields = self.env['ir.model.fields'].sudo().search([('name','=','l10n_in_gst_treatment'),('model_id','=',model_id.id)])
                        if not journal:
                            raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (picking.company_id.name, picking.company_id.id))
                        
                        if sale_order:
                            vals  = {
                                'invoice_origin': picking.origin,
                                'picking_id':picking.id,
                                'move_type': 'out_invoice',
                                'ref': False,
                                'sale_id':sale_order.id,
                                'ref':sale_order.client_order_ref,
                                # 'journal_id': journal.id,  
                                'partner_id': sale_order.partner_invoice_id.id,
                                'currency_id': sale_order.pricelist_id.currency_id.id,
                                'invoice_payment_term_id': sale_order.payment_term_id.id,
                                'fiscal_position_id': sale_order.fiscal_position_id.id or sale_order.partner_id.property_account_position_id.id,
                                'team_id': sale_order.team_id.id,
                                'invoice_date' : fields.Datetime.now().date(),
                                'partner_shipping_id':sale_order.partner_shipping_id.id,
                            }
                            

                          
                            if is_avail_fields:
                                if record.l10n_in_gst_treatment:
                                    vals['l10n_in_gst_treatment'] = record.l10n_in_gst_treatment
                            
                                
                            
                            invoice = inv_obj.create(vals)
                            
                            
                            for so_line in  sale_order.order_line :
                                if so_line.product_id:
                                    if so_line.product_id.type == "service":
                                        if so_line.product_uom_qty != so_line.qty_invoiced:
                                            if so_line.product_id.property_account_income_id:
                                                account_id = so_line.product_id.property_account_income_id
                                            elif so_line.product_id.categ_id.property_account_income_categ_id:
                                                account_id = so_line.product_id.categ_id.property_account_income_categ_id                    
                                            elif journal.default_account_id:
                                                account_id = journal.default_account_id
                                            else:
                                                raise UserError(_('Please define an account for the Product/Category.'))
                                            inv_line = {
                                                    'name': so_line.name,
                                                    'product_id': so_line.product_id.id,
                                                    'product_uom_id': so_line.product_id.uom_id.id,
                                                    'quantity': so_line.product_uom_qty,
                                                    'account_id': account_id.id,

                                                    'tax_ids': [(6, 0, so_line.tax_id.ids)],
                                                    'move_id':invoice.id,
                                                    'price_unit': so_line.price_unit,
                                                    'sale_line_ids': [(4, so_line.id)],
                                                    }
                                            invoice_vals.append((0,0,inv_line))
                                            so_line.write({
                                                'qty_to_invoice':so_line.product_uom_qty
                                            })                                
                                    else:
                                        if so_line.product_id.property_account_income_id:
                                            account = so_line.product_id.property_account_income_id
                                        elif so_line.product_id.categ_id.property_account_income_categ_id:
                                            account = so_line.product_id.categ_id.property_account_income_categ_id
                                        else:
                                            account = self.env['ir.property']._get('property_account_income_categ_id', 'product.category')

                                        
                                        if not account :
                                            raise UserError(_('Please define an account for the Product/Category.'))
    
                                        route = self.env['stock.location'].search([('name','=','Dropship')])
                                        if self._context.get('flag') == True and route.id in so_line.product_id.route_ids.ids:
                                            pass
                                        else:
                                            if so_line.product_id.invoice_policy == 'delivery':     
                                                inv_line = {
                                                        'name': so_line.name,
                                                        'product_id': so_line.product_id.id,
                                                        'product_uom_id': so_line.product_id.uom_id.id,
                                                        'quantity': picking.move_ids_without_package[0].quantity_done,
                                                        'account_id': account.id,
                                                        'tax_ids': [(6, 0, so_line.tax_id.ids)],
                                                        'move_id':invoice.id,
                                                        'price_unit': so_line.price_unit,
                                                        'sale_line_ids': [(4, so_line.id)],
                                                        }
                                            else:
                                                inv_line = {
                                                        'name': so_line.name,
                                                        'product_id': so_line.product_id.id,
                                                        'product_uom_id': so_line.product_id.uom_id.id,
                                                        'quantity': so_line.product_uom_qty,
                                                        'account_id': account.id,
                                                        'tax_ids': [(6, 0, so_line.tax_id.ids)],
                                                        'move_id':invoice.id,
                                                        'price_unit': so_line.price_unit,
                                                        'sale_line_ids': [(4, so_line.id)],
                                                        }
                                                 
                                                        
                                            invoice_vals.append((0,0,inv_line))
                                            so_line.write({
                                                'qty_to_invoice':so_line.product_uom_qty
                                            })                        
                            invoice.write({
                                'invoice_line_ids' : invoice_vals
                            })
                            if res_config.auto_validate_customer_invoice == True :
                                invoice.action_post()    
                            if res_config.auto_validate_customer_invoice == True and res_config.auto_send_mail_customer_invoices == True:
                                template = self.env.ref('account.email_template_edi_invoice', False)            
                                send = invoice.with_context(force_send=True,model_description='Invoice').message_post_with_template(int(template),email_layout_xmlid="mail.mail_notification_paynow")
        return res
