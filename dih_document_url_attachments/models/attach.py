from openerp import models, fields, api

class ir_attachment(models.Model):
	_inherit = "ir.attachment"

	category = fields.Many2one('ir.attach.category', string="Category")

class ir_attach_category(models.Model):
	_name = "ir.attach.category"
	name = fields.Char('Category')