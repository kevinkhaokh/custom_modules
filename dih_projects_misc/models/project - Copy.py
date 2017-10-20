# -*- coding: utf-8 -*-

from openerp import models, fields, api

class dashboard(models.Model):
	_name = 'project.dashboard'

	parent_lead = fields.Many2one('crm.lead', compute='_get_parent_lead', string="Created from Opportunity")
	parent_lead_id = fields.Integer('parent id')

	@api.depends('parent_lead_id')
	def _get_parent_lead(self):
		self.parent_lead = self.env['crm.lead'].browse(self.parent_lead_id)

	#Information 
	name = fields.Char('Name of project', required=True)
	location = fields.Many2one(related='parent_lead.location', string="Project Location")
	project_type = fields.Selection(related='parent_lead.project_type', string='Type of project')
	architect = fields.Many2one(related='parent_lead.architect', string="Architect")
	organizer = fields.Many2one(related='parent_lead.organizer', string="Organizer")
	owner = fields.Many2one(related='parent_lead.owner', string="Owner")
	customer = fields.Many2one(related='parent_lead.partner_id', string="Customer")
	advancement = fields.Float('Percentage of advancement')

	#Financial 
	amt_work_tbc = fields.Float('Amount of works to be completed')
	budget = fields.Float('Budget for project')
	analytic_account = fields.Many2one(related='parent_lead.analytic_account', string="Analytic Account")

	#Team 
	employees_included = fields.Many2many('hr.employee', string="Employees" )

	count_attachments = fields.Integer('Attachments', compute='_count_attachments')
	count_purchases = fields.Integer('Purchases completed', compute='_count_purchases')
	count_invoices = fields.Integer('Invoices', compute='_count_invoices')
	count_ipcs = fields.Integer('IPCs', compute='_count_ipcs')

	@api.depends('analytic_account')
	def _count_attachments(self):
		self.count_attachments = self.env['ir.attachment'].search_count([('res_id', '=', self.id)])

	@api.multi
	def smart_button_attachments(self):
		domain = ([
			('res_id', '=', self.id)
			])
		view = {
		'views' : [[False, "tree"], [False, "form"]],
		'res_model' : 'ir.attachment',
		'target' : 'current',
		'domain' : domain,
		'type' : 'ir.actions.act_window'
		}
		return view

	@api.multi
	def smart_button_purchases(self):
		domain = ([
			('analytic_account.id', '=', self.analytic_account.id)
			])
		view = {
		'views' : [[False, "tree"], [False, "form"]],
		'res_model' : 'purchase.order',
		'target' : 'current',
		'domain' : domain,
		'type' : 'ir.actions.act_window'
		}
		return view

	@api.multi
	def smart_button_invoices(self):
		domain_lines = ([
			('account_analytic_id.id', '=', self.analytic_account.id), ('invoice_id.type', '=', 'in_invoice')
			])
		invoice_line_ids = self.env['account.invoice.line'].search(domain_lines)
		invoice_ids = []
		for line in invoice_line_ids:
			invoice_ids.append(self.env['account.invoice.line'].browse(line).invoice_id.id)
		view = {
		'views' : [[False, "tree"], [False, "form"]],
		'res_model' : 'account.invoice.line',
		'target' : 'current',
		'domain' : domain,
		'type' : 'ir.actions.act_window'
		}
		return view

	@api.multi
	def smart_button_ipcs(self):
		domain = ([
			('account_analytic_id.id', '=', self.analytic_account.id), ('invoice_id.type', '=', 'out_invoice')
			])
		view = {
		'views' : [[False, "tree"], [False, "form"]],
		'res_model' : 'account.invoice.line',
		'target' : 'current',
		'domain' : domain,
		'type' : 'ir.actions.act_window'
		}
		return view

	@api.depends('analytic_account')
	def _count_ipcs(self):
		if self.analytic_account:
			self.count_ipcs = self.env['account.invoice.line'].search_count([('account_analytic_id.id', '=', self.analytic_account.id), ('invoice_id.type', '=', 'out_invoice')])
		else:
			self.count_ipcs = 0

	@api.depends('analytic_account')
	def _count_invoices(self):
		if self.analytic_account:
			self.count_invoices = self.env['account.invoice.line'].search_count([('account_analytic_id.id', '=', self.analytic_account.id), ('invoice_id.type', '=', 'in_invoice')])
		else:
			self.count_invoices = 0

	@api.depends('analytic_account')
	def _count_purchases(self):
		if self.analytic_account:	
			self.count_purchases = self.env['purchase.order'].search_count([('analytic_account.id', '=', self.analytic_account.id)])
		else:
			self.count_purchases = 0