# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions

class crm_lead(models.Model):
	_inherit = 'crm.lead'

	is_already_created = fields.Boolean('Is converted to a project.dashboard sheet', default=False)
	architect = fields.Many2one('res.partner', string="Architect")
	organizer = fields.Many2one('res.partner', string="Organizer")
	owner = fields.Many2one('res.partner', string="Owner")
	location = fields.Many2one('project.location', string="Project Location")
	project_type = fields.Selection([
		('hotel', 'Hotel'),
		('commercial', 'Commercial'),
		('institution', 'Institution'),
		('residential', 'Residential'),
		],
		string='Type of project',
		)
	analytic_account = fields.Many2one('account.analytic.account', string="Analytic Account")
	
	@api.multi
	def button_make_to_project(self):

		if self.is_already_created:
			raise exceptions.ValidationError('A project has already been created for this lead.')

		if not self.analytic_account:
			raise exceptions.ValidationError('Please fill the Analytic Account field before proceeding.')

		new_proj = self.env['project.dashboard'].sudo().create({
			'name' : self.name,
			'parent_lead_id' : self.id,
			})
		self.is_already_created = True
		return {
		'view_type' : 'form',
		'view_mode' : 'form',
		'res_model' : 'project.dashboard',
		'target' : 'current',
		'res_id' : new_proj.id,
		'type' : 'ir.actions.act_window'
		}

class project_location(models.Model):
	_name='project.location'
	name= fields.Char('Project Location')
