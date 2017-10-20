from openerp import models, fields, api

class res_partner(models.Model):
	_inherit = "res.partner"

	product_cats = fields.Many2one('product.category', string="Product Categories")