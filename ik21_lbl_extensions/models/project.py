# -*- coding: utf-8 -*-

from openerp import models, fields, api
import time
from datetime import datetime, timedelta, date
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

class Project(models.Model):
    _inherit = 'project.project'

    approval_delay = fields.Integer(string="", required=False, )


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.multi
    def _compute_last_day_returning(self):
        for record in self:
            record.last_day_returning = time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    def _compute_project_dates(self):
        for record in self:
            today = datetime.now().date()
            date_submittal = datetime.strptime(record.date_submittal, '%Y-%m-%d')
            last_day_returning = (date_submittal + timedelta(days=record.project_id.approval_delay)).date()
            record.last_day_returning = last_day_returning
            if not record.date_return:
                record.time_left_late = (last_day_returning - today).days
            else:
                date_return = datetime.strptime(record.date_return, '%Y-%m-%d').date()
                record.time_left_late = (last_day_returning - date_return).days

    date_submittal = fields.Date(string="", required=False, default=lambda *a: time.strftime(DEFAULT_SERVER_DATETIME_FORMAT) )
    date_return = fields.Date(string="", required=False, track_visibility='onchange')
    last_day_returning = fields.Date(string="", required=False, compute='_compute_project_dates' )
    time_left_late = fields.Integer(string="Time left / Late", required=False, compute='_compute_project_dates' )

    supplier_id = fields.Many2one(comodel_name="res.partner", string="Supplier", required=False, domain=[('supplier', '=', True)])
    stage_name = fields.Char(related="stage_id.name", required=False, )

    code = fields.Char(string="", required=False, track_visibility='onchange')
    used_for = fields.Char(string="", required=False, track_visibility='onchange')
    location = fields.Text(string="", required=False, track_visibility='onchange')
    description = fields.Text(track_visibility='onchange')
    remarks = fields.Text(string="", required=False, track_visibility='onchange')

