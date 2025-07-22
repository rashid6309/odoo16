# -*- coding: utf-8 -*-
# Developed by Bizople Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details

from odoo import http
from odoo.http import request, content_disposition
import json
import moyasar
import logging

_logger = logging.getLogger(__name__)

class RedirectPayments(http.Controller):

    @http.route(['/.well-known/apple-developer-merchantid-domain-association'], type='http', auth="public", website=True, sitemap=False)
    def applepay_merchant_file(self,**post):
        ir_attach = request.env['ir.attachment'].sudo().search([('res_model','=','payment.provider')],order="id desc",limit=1)
        values={
            'file_data' : ir_attach.raw.decode('ascii'),
        }
        return request.make_response(ir_attach.raw.decode('ascii'), headers=[
            ('Content-Type', 'application/pdf'),
            ('Content-Disposition', content_disposition('apple-developer-merchantid-domain-association')),
        ])

    @http.route(['/payment-status-return'], type='http', auth="public",website=True, sitemap=False)
    def get_moyasar_payment_status(self,**post):
        print("get_moyasar_payment_status POSTTTTTTTTTTTTTTTTTTT ==========================",post)
        print("get_moyasar_payment_status POSTTTTTTTTTTTTTTTTTT post.get('status')T ==========================",post.get('status'))
        print("get_moyasar_payment_status POSTTTTTTTTTTTTTTTTTT post.get('id')T ==========================",post.get('id'))
        status = post.get('status')
        payment_id = post.get('id')

        payment_aquirer = request.env['payment.provider'].sudo().search([('code','=','moyasar')])
        moyasar.api_key = payment_aquirer.moyasar_secret_key
        print("get_moyasar_payment_status moyasar.api_key ==========================",moyasar.api_key)
        print("get_moyasar_payment_status moyasar ==========================",moyasar)
        print("get_moyasar_payment_status moyasar.Payment ==========================",moyasar.Payment)
        payment = moyasar.Payment.fetch(str(payment_id))
        print("get_moyasar_payment_status payment ==========================",payment)
        order = request.website.sale_get_order()
        _logger.info("****************Order Name*************: %s (%s)",order.name, order)
        _logger.info("***************Payment Transaction************** : %s",order.transaction_ids)

        if status == 'paid':
            data = {
                'state': 'done',
                'reference': order.transaction_ids.search([], order="id desc", limit=1).reference,
            }

            print("get_moyasar_payment_status STATUSSS PAIDDD data ==========================",data)
            
            payment_transaction = request.env['payment.transaction'].sudo()._handle_notification_data("moyasar", data)
            print("get_moyasar_payment_status payment_transaction ==========================",payment_transaction)
            tx = request.env['payment.transaction'].sudo().search([('reference', '=', data['reference'])], limit=1)
            tx.write({'moyasar_payment_id' : payment_id })
            values={
            'transaction_id' : tx.id
            }
            return request.redirect("/payment/status")
        else:
            payment_message = payment.source
            print("PAYMENTTTTTTTT MESSAAAAAGEEEEEEEEEEEEEEEEEEEEEEE",payment_message)
            error_message = payment_message.get('message')
            value={
                'error' : error_message,
                'redirect' : '/payment/status',
            }
            data = {
                'state': 'cancel',
                'reference': order.transaction_ids.search([],order="id desc",limit=1).reference,
            }
            print("get_moyasar_payment_status STATUSSS elseeeeeeeee data ==========================",data)
            payment_transaction = request.env['payment.transaction'].sudo()._handle_notification_data("moyasar",data)
            return request.render('payment_moyasar_bizople.payment_error_temp',value)

    @http.route(['/get/moyasar/order'], type='json', auth="public", website=True)
    def savepayments(self, **post):
        order = request.website.sudo().sale_get_order()
        print("order===========================================",order.read())
        amount= ''
        if order.tax_totals:
            tax_json = order.tax_totals
            amount = tax_json['amount_total']
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        
        payment_aquirer = request.env['payment.provider'].sudo().search([('code','=','moyasar')])
        values = {
        'amount' : amount,
        'public_key' : payment_aquirer.moyasar_public_key,
        'callback_url' : base_url,
        'currency' : order.currency_id.name,
        'description' : order.name,
        }
        return values