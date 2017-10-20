from openerp import fields, models, api

class crm_lead(models.Model)
	
	scope_of_works = fields.Text('Scope of works')
	associated_partners = fields.Many2many('Associated Partners', 'res.partner')
	tender_received = fields.Boolean('Tender Received')
	date_submission_tender = fields.Date('Tender Submission date')
	date_start = fields.Date('Project Start date')
	date_finish = fields.Date('Project End date')
