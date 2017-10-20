# -*- coding: utf-8 -*-

from openerp import models, fields, api

class dashboard(models.Model):
	_name = 'project.dashboard'

	parent_lead = fields.Many2one('crm.lead', compute='_get_parent_lead', required=True, string="Created from Opportunity")
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
	date_start = fields.Date('Start date')
	date_end = fields.Date('End date')

	#Financial 
	amt_work_tbc = fields.Float('Amount of works to be completed')
	budget = fields.Float('Budget for project')
	analytic_account = fields.Many2one(related='parent_lead.analytic_account', string="Analytic Account")

	#Team 
	employees_included = fields.Many2many('hr.employee', string="Employees")

	count_attachments = fields.Integer('Attachments', compute='_count_attachments')
	count_purchases = fields.Integer('Purchases completed', compute='_count_purchases')
	count_invoices = fields.Integer('Invoices', compute='_count_invoices')
	count_ipcs = fields.Integer('IPCs', compute='_count_ipcs')

	@api.depends('analytic_account')
	def _count_attachments(self):
		self.count_attachments = self.env['ir.attachment'].search_count([
			'|', '&', ('res_id', '=', self.id), ('res_model', '=', 'project.dashboard'), '&', ('res_id', '=', self.parent_lead.id), ('res_model', '=', 'crm.lead')
			])

	@api.multi
	def smart_button_attachments(self):
		domain = ([
			'|', '&', ('res_id', '=', self.id), ('res_model', '=', 'project.dashboard'), '&', ('res_id', '=', self.parent_lead.id), ('res_model', '=', 'crm.lead')
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

	#Takes a domain of account.invoice.line and returns a domain of account.invoice containing all concerned invoices
	def _get_invoice_domain_from_lines_domain(self, aDomain):
		invoice_lines = self.env['account.invoice.line'].search(aDomain)
		invoice_ids = []
		for line in invoice_lines:
			invoice_ids.append(line.id)
		invoice_ids_no_duplicates = list(set(invoice_ids))
		result = ([
			('id', 'in', invoice_ids_no_duplicates)
			])
		return result

	@api.multi
	def smart_button_invoices(self):
		domain_lines = ([
			('account_analytic_id.id', '=', self.analytic_account.id), ('invoice_id.type', '=', 'in_invoice')
			])
		domain = self._get_invoice_domain_from_lines_domain(domain_lines)
		view = {
		'views' : [[False, "tree"], [False, "form"]],
		'res_model' : 'account.invoice',
		'target' : 'current',
		'domain' : domain,
		'type' : 'ir.actions.act_window'
		}
		return view

	@api.multi
	def smart_button_ipcs(self):
		domain_lines = ([
			('account_analytic_id.id', '=', self.analytic_account.id), ('invoice_id.type', '=', 'out_invoice')
			])
		domain = self._get_invoice_domain_from_lines_domain(domain_lines)
		view = {
		'views' : [[False, "tree"], [False, "form"]],
		'res_model' : 'account.invoice',
		'target' : 'current',
		'domain' : domain,
		'type' : 'ir.actions.act_window'
		}
		return view

	@api.depends('analytic_account')
	def _count_ipcs(self):
		if self.analytic_account:
			domain_lines = ([
				('account_analytic_id.id', '=', self.analytic_account.id), ('invoice_id.type', '=', 'out_invoice')
				])
			domain = self._get_invoice_domain_from_lines_domain(domain_lines)
			invoice_list = self.env['account.invoice'].search(domain)
			total_sum = 0.0
			for invoice in invoice_list:
				total_sum += invoice.amount_total
			self.count_ipcs = total_sum
		else:
			self.count_ipcs = 0

	@api.depends('analytic_account')
	def _count_invoices(self):
		if self.analytic_account:
			domain_lines = ([
				('account_analytic_id.id', '=', self.analytic_account.id), ('invoice_id.type', '=', 'in_invoice')
				])
			domain = self._get_invoice_domain_from_lines_domain(domain_lines)
			invoice_list = self.env['account.invoice'].search(domain)
			total_sum = 0.0
			for invoice in invoice_list:
				total_sum += invoice.amount_total
			self.count_invoices = total_sum
		else:
			self.count_invoices = 0

	@api.depends('analytic_account')
	def _count_purchases(self):
		if self.analytic_account:	
			purchases = self.env['purchase.order'].search_count([('analytic_account.id', '=', self.analytic_account.id)])
			self.count_purchases = purchases
		else:
			self.count_purchases = 0