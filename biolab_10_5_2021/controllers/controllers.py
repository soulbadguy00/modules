# -*- coding: utf-8 -*-
# from odoo import http


# class StockHub(http.Controller):
#     @http.route('/stock_hub/stock_hub/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_hub/stock_hub/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_hub.listing', {
#             'root': '/stock_hub/stock_hub',
#             'objects': http.request.env['stock_hub.stock_hub'].search([]),
#         })

#     @http.route('/stock_hub/stock_hub/objects/<model("stock_hub.stock_hub"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_hub.object', {
#             'object': obj
#         })
