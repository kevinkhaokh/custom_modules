from openerp import models, fields, api

class purchase_order_line(models.Model):
	_inherit = "purchase.order.line"

	def _default_product_cat(self):
		return self.env['product.category'].search([['id', '=', 1]], limit=1)

	product_cat = fields.Many2one('product.category', string="Product Category", default=_default_product_cat)
