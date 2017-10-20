# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openpyxl import *

class hr_employee(models.Model):
	_inherit = 'hr.employee'

	@api.multi
	def test_openpyxl(self):
		wb = Workbook()
		wb.save(filename='test.xlsx') #pathSaveTo.get())



