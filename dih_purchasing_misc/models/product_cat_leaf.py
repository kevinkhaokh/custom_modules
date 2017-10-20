from openerp import models, fields, api

class product_cat_leaf(models.Model):
	_name = "product.cat.leaf"

	name = fields.Char('Name of product type')