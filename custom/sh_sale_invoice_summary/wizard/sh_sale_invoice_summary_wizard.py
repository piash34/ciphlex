# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
import xlwt
import base64
import io
import pytz
from datetime import datetime, timedelta


class SaleInvioceSummaryWizard(models.TransientModel):
    _name = 'sh.sale.invoice.summary.wizard'
    _description = 'Sale Invoice Summary Wizard'

    sh_start_date = fields.Datetime(
        'Start Date', required=True, default=fields.Datetime.now)
    sh_end_date = fields.Datetime(
        'End Date', required=True, default=fields.Datetime.now)
    sh_partner_ids = fields.Many2many(
        'res.partner', string='Customers', required=True)
    sh_status = fields.Selection(
        [('all', 'All'), ('draft', 'Draft'), ('open', 'Open'), ('paid', 'Paid')], string="Status", default='all')
    company_ids = fields.Many2many(
        'res.company', default=lambda self: self.env.companies, string="Companies")

    @api.constrains('sh_start_date', 'sh_end_date')
    def _check_dates(self):
        if self.filtered(lambda c: c.sh_end_date and c.sh_start_date > c.sh_end_date):
            raise ValidationError(_('start date must be less than end date.'))

    def print_report(self):
        datas = self.read()[0]
        return self.env.ref('sh_sale_invoice_summary.sh_sale_invoice_summary_action').report_action([], data=datas)

    def display_report(self):
        datas = self.read()[0]
        report = self.env['report.sh_sale_invoice_summary.sh_sale_invoice_summary_doc']
        data_values = report._get_report_values(
            docids=None, data=datas).get('customer_order_dic')

        self.env['sh.sale.invoice.summary'].search([]).unlink()
        if data_values:
            for customer in data_values:
                for order in data_values[customer]:
                    self.env['sh.sale.invoice.summary'].create({
                        'sh_partner_id': order['partner_id'],
                        'name': order['order_number'],
                        'date_order': order['order_date'],
                        'invoice_number': order['invoice_number'] if order['invoice_number'] else "",
                        'invoice_date': order['invoice_date'] if order['invoice_date'] else False,
                        'invoice_amount': order['invoice_amount'],
                        'invoice_paid_amount': order['invoice_paid_amount'],
                        'invoice_due_amount': order['due_amount']
                    })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Invoice Summary',
            'view_mode': 'tree',
            'res_model': 'sh.sale.invoice.summary',
            'context': "{'create': False,'search_default_group_customer': 1}"
        }

    def print_xls_report(self):
        workbook = xlwt.Workbook(encoding='utf-8')
        heading_format = xlwt.easyxf(
            'font:height 300,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center')
        bold = xlwt.easyxf(
            'font:bold True,height 215;pattern: pattern solid, fore_colour gray25;align: horiz center')
        bold_center = xlwt.easyxf(
            'font:height 240,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center;')
        worksheet = workbook.add_sheet(
            'Sale Invoice Summary', bold_center)
        worksheet.write_merge(
            0, 1, 0, 6, 'Sale Invoice Summary', heading_format)
        left = xlwt.easyxf('align: horiz center;font:bold True')
        center = xlwt.easyxf('align: horiz center;')
        bold_center_total = xlwt.easyxf('align: horiz center;font:bold True')
        date_start = False
        date_stop = False
        if self.sh_start_date:
            date_start = fields.Datetime.from_string(self.sh_start_date)
        else:
            # start by default today 00:00:00
            user_tz = pytz.timezone(self.env.context.get(
                'tz') or self.env.user.tz or 'UTC')
            today = user_tz.localize(fields.Datetime.from_string(
                fields.Date.context_today(self)))
            date_start = today.astimezone(pytz.timezone('UTC'))

        if self.sh_end_date:
            date_stop = fields.Datetime.from_string(self.sh_end_date)
            # avoid a date_stop smaller than date_start
            if date_stop < date_start:
                date_stop = date_start + timedelta(days=1, seconds=-1)
        else:
            # stop by default today 23:59:59
            date_stop = date_start + timedelta(days=1, seconds=-1)
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        start_date = datetime.strftime(pytz.utc.localize(datetime.strptime(str(self.sh_start_date),
                                                                           DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local), DEFAULT_SERVER_DATETIME_FORMAT)
        end_date = datetime.strftime(pytz.utc.localize(datetime.strptime(str(self.sh_end_date),
                                                                         DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local), DEFAULT_SERVER_DATETIME_FORMAT)
        worksheet.write_merge(2, 2, 0, 6, start_date + " to " + end_date, bold)
        worksheet.col(0).width = int(30 * 260)
        worksheet.col(1).width = int(30 * 260)
        worksheet.col(2).width = int(18 * 260)
        worksheet.col(3).width = int(18 * 260)
        worksheet.col(4).width = int(33 * 260)
        worksheet.col(5).width = int(15 * 260)
        worksheet.col(6).width = int(15 * 260)
        customer_order_dic = {}
        for partner_id in self.sh_partner_ids:
            order_list = []
            domain = [
                ("date_order", ">=", fields.Datetime.to_string(date_start)),
                ("date_order", "<=", fields.Datetime.to_string(date_stop)),
                ("partner_id", "=", partner_id.id),
                ('state', 'in', ['sale', 'done']),
            ]
            if self.company_ids:
                domain.append(
                    ('company_id', 'in', self.company_ids.ids))
            search_orders = self.env['sale.order'].sudo().search(domain)
            invoice_ids = []
            if search_orders:
                for order in search_orders:
                    invoiced = True
                    if order.invoice_ids:
                        if self.sh_status == 'draft':
                            for invoice in order.invoice_ids:
                                if invoice.state not in ('draft'):
                                    invoiced = False
                                    break

                        elif self.sh_status == 'open':
                            for invoice in order.invoice_ids:
                                if invoice.state not in ('posted') or invoice.amount_residual == 0.0:
                                    invoiced = False
                                    break

                        elif self.sh_status == 'paid':
                            for invoice in order.invoice_ids:
                                if invoice.state not in ('posted') or invoice.amount_residual != 0.0:
                                    invoiced = False
                                    break

                    if order.invoice_ids and invoiced:
                        for invoice in order.invoice_ids:
                            if invoice.id not in invoice_ids:
                                invoice_ids.append(invoice.id)
                            order_dic = {
                                'order_number': order.name,
                                'order_date': order.date_order.date(),
                                'invoice_number': invoice.name,
                                'invoice_date': invoice.invoice_date,
                                'invoice_currency_id': invoice.currency_id.symbol,
                            }
                            if invoice.move_type == 'out_invoice':
                                order_dic.update({
                                    'invoice_amount': invoice.amount_total,
                                    'invoice_paid_amount': invoice.amount_total - invoice.amount_residual,
                                    'due_amount': invoice.amount_residual,
                                })
                            elif invoice.move_type == 'out_refund':
                                order_dic.update({
                                    'invoice_amount': -(invoice.amount_total),
                                    'invoice_paid_amount': -(invoice.amount_total - invoice.amount_residual),
                                    'due_amount': -(invoice.amount_residual),
                                })
                            order_list.append(order_dic)
            if order_list:
                customer_order_dic.update(
                    {partner_id.name_get()[0][1]: order_list})
        row = 4
        if customer_order_dic:
            for key in customer_order_dic.keys():
                worksheet.write_merge(
                    row, row, 0, 6, key, bold_center)
                row = row + 2
                total_amount_invoiced = 0.0
                total_amount_paid = 0.0
                total_amount_due = 0.0
                worksheet.write(row, 0, "Order Number", bold)
                worksheet.write(row, 1, "Order Date", bold)
                worksheet.write(row, 2, "Invoice Number", bold)
                worksheet.write(row, 3, "Invoice Date", bold)
                worksheet.write(row, 4, "Amount Invoiced", bold)
                worksheet.write(row, 5, "Amount Paid", bold)
                worksheet.write(row, 6, "Amount Due", bold)
                row = row + 1
                for rec in customer_order_dic[key]:
                    worksheet.write(row, 0, rec.get('order_number'), center)
                    worksheet.write(row, 1, str(rec.get('order_date')), center)
                    worksheet.write(row, 2, rec.get('invoice_number'), center)
                    worksheet.write(row, 3, str(
                        rec.get('invoice_date') if rec.get('invoice_date') else ""), center)
                    worksheet.write(row, 4, str(rec.get(
                        'invoice_currency_id')) + "{:.2f}".format(rec.get('invoice_amount')), center)
                    worksheet.write(row, 5, str(rec.get('invoice_currency_id')) + "{:.2f}".format(rec.get(
                        'invoice_paid_amount')), center)
                    worksheet.write(row, 6, str(rec.get(
                        'invoice_currency_id')) + "{:.2f}".format(rec.get('due_amount')), center)
                    total_amount_invoiced = total_amount_invoiced + \
                        rec.get('invoice_amount')
                    total_amount_paid = total_amount_paid + \
                        rec.get('invoice_paid_amount')
                    total_amount_due = total_amount_due + rec.get('due_amount')
                    row = row + 1
                worksheet.write(row, 3, "Total", left)
                worksheet.write(row, 4, "{:.2f}".format(total_amount_invoiced),
                                bold_center_total)
                worksheet.write(row, 5, "{:.2f}".format(
                    total_amount_paid), bold_center_total)
                worksheet.write(row, 6, "{:.2f}".format(
                    total_amount_due), bold_center_total)
                row = row + 2
        else:
            raise UserError('There is no Data Found between these dates...')

        fp = io.BytesIO()
        workbook.save(fp)
        data = base64.encodebytes(fp.getvalue())
        IrAttachment = self.env['ir.attachment']
        attachment_vals = {
            'name': 'Sale_Invoice_Summary.xls',
            'res_model': 'ir.ui.view',
            'type': 'binary',
            'datas': data,
            'public': True,
        }
        fp.close()

        attachment = IrAttachment.search([('name', '=', 'Sale_Invoice_Summary'),
                                          ('type', '=', 'binary'), ('res_model', '=', 'ir.ui.view'
                                                                    )], limit=1)
        if attachment:
            attachment.write(attachment_vals)
        else:
            attachment = IrAttachment.create(attachment_vals)

        # TODO: make user error here

        if not attachment:
            raise UserError('There is no attachments...')

        url = '/web/content/' + str(attachment.id) + '?download=true'
        return {'type': 'ir.actions.act_url', 'url': url,
                'target': 'new'}
