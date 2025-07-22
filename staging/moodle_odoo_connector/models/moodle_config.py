# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import requests

from odoo.exceptions import AccessError, UserError


class MoodleConfig(models.Model):
    _name = 'moodle.config'
    _description = 'Moodle Configuration'

    name = fields.Char(string='Configuration Name', required=True, default='Default Configuration')
    url = fields.Char(string='Moodle URL', required=True)
    token = fields.Char(string='Moodle Token', required=True)
    function = fields.Char(string='Moodle Function', default='core_course_create_categories', required=True)


class MoodleCategory(models.Model):
    _name = 'moodle.category'
    _description = 'Moodle Category'

    name = fields.Char(string='Category Name', required=True)
    parent_id = fields.Integer(string='Parent ID', default=0)
    idnumber = fields.Integer(string='ID Number')
    description = fields.Text(string='Description')
    config_id = fields.Many2one('moodle.config', string='Moodle Configuration', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted')
    ], string='Status', default='draft')

    def create_moodle_category(self):
        for record in self:
            url = record.config_id.url
            token = record.config_id.token
            function = record.config_id.function
            payload = {
                'moodlewsrestformat': 'json',
                'wstoken': token,
                'wsfunction': function,
                'categories[0][name]': record.name,
                'categories[0][parent]': record.parent_id,
                'categories[0][idnumber]': record.idnumber,
                'categories[0][description]': record.description,
            }
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                result = response.json()
                if 'exception' in result:
                    raise UserError(_('Moodle API Error: %s') % result['message'])
                else:
                    record.state = 'posted'
                    record.idnumber = result[0]['id'] or None

            else:
                raise UserError(_('Error connecting to Moodle API'))
