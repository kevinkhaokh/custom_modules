from openerp import fields, api, models

class purchase_order(models.Model):
	_inherit = "purchase.order"


	notes = fields.Text('Terms and Conditions', default="VERY USEFUL TEMPLATE GIVEN BY ANTOINE")