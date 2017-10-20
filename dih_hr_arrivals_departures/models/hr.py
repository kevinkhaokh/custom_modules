# -*- coding: utf-8 -*-

from openerp import models, fields, api

class hr_dih_movement(models.Model):
	_name = 'hr.dih.movement'
	_inherit = 'mail.thread'

	name = fields.Char('Name', default="Movement")
	emp_id = fields.Many2one('hr.employee', string="Employee", required=True)
	job_title = fields.Many2one('hr.job', related="emp_id.job_id", string="Job Title", readonly=True)
	location = fields.Char(related="emp_id.work_location", string="Work Location", readonly=True)
	nationality = fields.Many2one(related="emp_id.country_id", string="Nationality", readonly=True)
	date = fields.Date('Date', required=True)
	nature_of_move = fields.Selection([
		('departure', 'Check out'),
		('hire', 'Check in')
		],
		required=True,
		string='Check in/out',
		track_visibility='onchange'
		)
	comments = fields.Text('Additional comments')

	completed_depart = fields.Boolean('Check-out process completed', compute='_is_depart_completed', readonly=True, store=True)
	completed_arrive = fields.Boolean('Check-in process completed', compute='_is_arrive_completed', readonly=True, store=True)
	
	@api.depends('depart_it', 'depart_hr', 'depart_finance')
	def _is_depart_completed(self):
		self.completed_depart = (self.depart_it and self.depart_hr and self.depart_finance)

	@api.depends('depart_it', 'depart_hr', 'depart_finance')
	def _is_arrive_completed(self):
		self.completed_arrive = (self.arrive_it and self.arrive_hr and self.arrive_finance)

	#visible only if departure
	depart_it_assets_recovered = fields.Boolean('Assets recovered', track_visibility='onchange')
	depart_it_access_revoked = fields.Boolean('Acces revoked', track_visibility='onchange')
	depart_it = fields.Boolean('IT completed', track_visibility='onchange')
	depart_hr_loans = fields.Boolean('Loans and advances cleared', track_visibility='onchange')
	depart_hr_ins_cancelled = fields.Boolean('Insurance cancelled', track_visibility='onchange')
	depart_hr_leaves_cleared = fields.Boolean('Leaves cleared', track_visibility='onchange')
	depart_hr_comments = fields.Boolean('Additional comments', track_visibility='onchange')
	depart_hr = fields.Boolean('HR completed', track_visibility='onchange')
	depart_finance = fields.Boolean('Finance completed', track_visibility='onchange')

	#visible only if arrival
	arrive_it_evaluate_reqs = fields.Boolean('Requirements evaluated', track_visibility='onchange')
	arrive_it_notes_reqs = fields.Text('Notes on requirements', track_visibility='onchange')
	arrive_it_access_created = fields.Boolean('Access created', track_visibility='onchange')
	arrive_it_prepared = fields.Boolean('Computer prepared', track_visibility='onchange')
	arrive_it_assign_assets = fields.Boolean('Assets assigned', track_visibility='onchange')
	arrive_it = fields.Boolean('IT completed', track_visibility='onchange')
	arrive_hr_ins_done = fields.Boolean('Insurance card handed', track_visibility='onchange')
	arrive_hr = fields.Boolean('HR completed', track_visibility='onchange')
	arrive_finance = fields.Boolean('Finance completed', track_visibility='onchange')

	@api.model
	def check_for_notifs(self):
		if nature_of_move is departure:
			if (not self.completed_depart) and (self.nature_of_move is 'departure'):
				self.make_notifs_depart()
		if nature_of_move is hire:
			if (not self.completed_arrive and (self.nature_of_move is 'hire')):
				self.make_notifs_arrive()

#Notifs if not finished : j-7, j-1, j+2, j+5, j+5...
#Notif Employee has started on j

	@api.model
	def make_notifs_depart(self):
		print('Make notifs depart')
#		todays_date = str(datetime.now().date())
#		followers = self.env['hr.dih.movement'].search([('date', '=', todays_date)])
#		msg_obj = self.env['mail.message']
#		for user in followers:
#			user.has_taken_effect = True
#			user.active = False
#			thread_id = 
#			body = 
#			subject = 
#			user.message_post(thread_id, body=body, subject=subject)

	@api.model
	def make_notifs_arrive(self):
		print('Make notifs arrive')
	#job title
	#location
	#date
	#nationality