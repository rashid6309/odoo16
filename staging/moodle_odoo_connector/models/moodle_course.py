from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests


class MoodleCourse(models.Model):
    _name = 'moodle.course'
    _description = 'Moodle Course'

    name = fields.Char(string='Course Name', required=True)
    shortname = fields.Char(string='Short Name', required=True)
    category_id = fields.Many2one('moodle.category', string='Category', required=True)
    idnumber = fields.Char(string='ID Number')
    courseformatoptions_name = fields.Char(string='Course Format Option Name', default='TEMPLATE')
    courseformatoptions_value = fields.Integer(string='Course Format Option Value', default=9)
    format = fields.Char(string='Format', default='tiles')
    startdate = fields.Datetime(string='Start Date')
    enddate = fields.Datetime(string='End Date')
    config_id = fields.Many2one('moodle.config', string='Moodle Configuration', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted')
    ], string='Status', default='draft')
    attendance_json = fields.Text('Attendance')

    def create_moodle_course(self):
        for record in self:
            url = record.config_id.url
            token = record.config_id.token
            payload = {
                'moodlewsrestformat': 'json',
                'wstoken': token,
                'wsfunction': 'core_course_create_courses',
                'courses[0][fullname]': record.name,
                'courses[0][shortname]': record.shortname,
                'courses[0][categoryid]': record.category_id.idnumber,
                'courses[0][idnumber]': record.idnumber,
                'courses[0][courseformatoptions][0][name]': record.courseformatoptions_name,
                'courses[0][courseformatoptions][0][value]': record.courseformatoptions_value,
                'courses[0][format]': record.format,
                'courses[0][startdate]': int(record.startdate.timestamp()) if record.startdate else 0,
                'courses[0][enddate]': int(record.enddate.timestamp()) if record.enddate else 0,
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
                raise UserError(_('Error connecting to Moodle API: %s') % response.text)

    def fetch_attendance_data(self):
        for record in self:
            url = record.config_id.url
            token = record.config_id.token
            payload = {
                'moodlewsrestformat': 'json',
                'wstoken': token,
                'wsfunction': 'gradereport_user_get_grade_items',
                'courseid': record.idnumber,
            }
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                result = response.json()
                if 'exception' in result:
                    raise UserError(_('Moodle API Error: %s') % result['message'])
                else:
                    self.attendance_json = ''
                    self.attendance_json = result['usergrades']
                    # Process attendance data here
                    # Example: You can parse the result and store it in Odoo or perform any other operations
                    pass
            else:
                raise UserError(_('Error connecting to Moodle API: %s') % response.text)
