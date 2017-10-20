# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp import exceptions



class employee_category_merge_wizard(models.TransientModel):
	"""
	This wizard will confirm the all the selected draft invoices
	"""
	_name = "hr.employee.category.merge.wizard"
	_description = "Merge employee category tags"
	new_name = fields.Char('New Name')

	@api.multi
	def merge_tags(self):
		active_ids = self.env.context['active_ids']
		id_tag_to_keep = active_ids[0]
		tag_to_keep = self.env['hr.employee.category'].search([('id', '=', id_tag_to_keep)]) #We keep the first tag only 
		tag_to_keep.name = self.new_name
		all_emps = self.env['hr.employee'].search([])

		for employee in all_emps:
			isTagged = False
			id_categories = []
			for cat in employee.category_ids:
				id_categories.append(cat.id)
			#Check if employee has one of the tags that are to be merged
			for merge_tag in active_ids:
				if merge_tag in id_categories:
					isTagged = True
			#Add the tag to be merged if it's not there
			if (isTagged == True):
				employee.write({'category_ids': [(4, id_tag_to_keep, 0)]})

		#Destroy all tags except the first one
		for id_tag_to_delete in active_ids[1:]:
			tag_to_delete = self.env['hr.employee.category'].search([('id', '=', id_tag_to_delete)])
			tag_to_delete.unlink()
            
		return {'type': 'ir.actions.act_window_close'}
