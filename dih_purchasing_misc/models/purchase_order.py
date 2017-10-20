from openerp import models, fields, api
from openerp import exceptions
import datetime

class purchase_order(models.Model):
	_inherit = "purchase.order"

	analytic_account = fields.Many2one('account.analytic.account', required=True)

	#28Sept added, to add on upper right corner
	product_categories = fields.Many2many('product.category')
	leaf_product_categories = fields.Many2many('product.cat.leaf')
	rfq_date = fields.Date('RFQ Date') 
	expected_delivery_date = fields.Date('Expected Delivery Date', required=True) 
	internal_po_number = fields.Char('Internal PO number')

	def _reformat(self, aString):
		lowered = aString.lower()
		step1 = lowered.replace(' ', '.')
		step2 = step1.replace('-', '.')
		step3 = step2.replace('...', '.')
		step4 = step3.replace('..', '.')
		return step4

	@api.model
	def create(self, vals):
		#Autogen the Internal PO Number
		yr = str(datetime.datetime.now().year)
		seqname = self.env['account.analytic.account'].browse(vals['analytic_account']).dih_seqname
		if not seqname:
			raise exceptions.ValidationError('This analytic account has no short-name for internal PO numbers. Please contact the admin')
		seqname_db = 'pn.' + self._reformat(seqname) #WARNING ! There is a hard limit on the analytic account name ###########################
		
		#The branch is here to determine if there is already a sequence for this analytic account in particular
		if self.env['ir.sequence'].search([('name', '=', seqname_db)]):
			nr = self.env['ir.sequence'].next_by_code(seqname_db)
			vals['internal_po_number'] = seqname + '-LBL-PO-' + str(yr) + '/' + str(nr) 
		else:
			newseqtype = self.env['ir.sequence.type'].create({
				'name' : seqname_db,
				'code' : seqname_db,
				})
			newseq = self.env['ir.sequence'].create({
				'code' : seqname_db,
				'name' : seqname_db,
				'padding' : 5,
				'number_next_actual' : 1,
				'number_increment' : 1,
				'implementation' : 'standard'
				})
			nr = self.env['ir.sequence'].next_by_code(seqname_db)
			vals['internal_po_number'] = seqname + '-LBL-PO-' + str(yr) + '/' + str(nr) 

		#Fill scheduled delivery date field on order line according to Expected PO Date
		new_lines = vals['order_line']
		print(new_lines)
		for line in new_lines:
			line[2]['date_planned'] = vals['expected_delivery_date']

		return super(purchase_order, self).create(vals)

	#28Sept added, according to Antoine's specs excel sheet, to add in separate tab
	tnc_contract_type = fields.Selection(
		[('supply_only', 'Supply Only'), ('supply_and_install', 'Supply and Install')],
		string='Contract Type',
		default='supply_only'
		)

	tnc_contract_type_advance = fields.Float('Advance payment (%)')
	tnc_contract_type_delivery = fields.Float('Upon delivery (%)')
	tnc_contract_type_progclaim = fields.Float('Upon progress claim (%)')
	tnc_contract_type_balance = fields.Float('Balance Payment (%)')



	tnc_retention = fields.Selection([
		('not_applicable', 'Not applicable'),
		('applicable', 'Applicable'),
		],
		string='Retention',
		
		)
	tnc_retention_oneach = fields.Float('On each payment (%)')
	tnc_retention_uponcomplete = fields.Float('To be released upon completion (%)')
	tnc_retention_after = fields.Float('To be released after then end of the defect liability period (%)')
	tnc_retention_release = fields.Float('To be released x months after completion (months)')



	tnc_dlp = fields.Selection([
		('not_applicable', 'Not applicable'),
		('applicable', 'Applicable'),
		],
		string='Defect Liability Period',
		
		)
	tnc_dlp_fromcompletionprov = fields.Integer('From completion & provisional acceptance certificate (months)')



	tnc_warranty = fields.Selection([
		('not_applicable', 'Not applicable'),
		('applicable', 'Applicable'),
		],
		string='Warranty',
		
		)
	tnc_warranty_duration = fields.Integer('Manufacturer warranty (months)')



	tnc_delivery_time = fields.Selection([
		('after_po_conf', 'After PO Confirmation'),
		('completion_date', 'Completion Date'),
		],
		string='Delivery time or completion',
		)
	tnc_delivery_time_after_po = fields.Integer('After PO confirmation (days)')
	tnc_delivery_time_completion = fields.Date('Completion date')
	tnc_delivery_time_other = fields.Text('Other remarks')



	tnc_penalty = fields.Selection([
		('not_applicable', 'Not applicable'),
		('applicable', 'Applicable'),
		],
		string='Penalty for delays',
		)
	tnc_penalty_percentage = fields.Integer('Percentage of the total amount per day late')
	tnc_penalty_maximum = fields.Integer('Maximum applicable percentage')


	tnc_other = fields.Text('Other inspection or completion conditions, documentation, manuals')


	tnc_insurance = fields.Text('Insurance conditions')

	@api.onchange('analytic_account', 'order_line')
	def _autofill_analytic_account(self):
		for line in self.order_line:
			line.account_analytic_id = self.analytic_account.id
