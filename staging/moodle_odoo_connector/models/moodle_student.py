from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests


class MoodleStudent(models.Model):
    _name = 'moodle.student'
    _description = 'Moodle Student'

    name = fields.Char(string='Full Name', required=True)
    username = fields.Char(string='Username', required=True)
    password = fields.Char(string='Password', required=True)
    email = fields.Char(string='Email', required=True)
    firstname = fields.Char(string='First Name', required=True)
    lastname = fields.Char(string='Last Name', required=True)
    attendance_increment = fields.Integer(string='Increment', compute='increment_function', store=True)
    auth = fields.Char(string='Auth Method', default='manual')
    idnumber = fields.Char(string='ID Number')
    config_id = fields.Many2one('moodle.config', string='Moodle Configuration', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('inactive', 'Inactive')
    ], string='Status', default='draft')

    def create_moodle_student(self):
        for record in self:
            url = record.config_id.url
            token = record.config_id.token
            payload = {
                'moodlewsrestformat': 'json',
                'wstoken': token,
                'wsfunction': 'core_user_create_users',
                'users[0][username]': record.username,
                'users[0][password]': record.password,
                'users[0][firstname]': record.firstname,
                'users[0][lastname]': record.lastname,
                'users[0][email]': record.email,
                'users[0][auth]': record.auth,
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

    def activate_inactivate_moodle_student(self):
        state = self._context.get('state')
        for record in self:
            # if record.state != 'posted':
            #     raise UserError(_('Only posted students can be inactivated.'))

            url = record.config_id.url
            token = record.config_id.token
            payload = {
                'moodlewsrestformat': 'json',
                'wstoken': token,
                'wsfunction': 'core_user_update_users',
                'users[0][id]': record.idnumber,
                'users[0][suspended]': 0 if state == 'active' else 1,
            }
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                result = response.json()
                if 'exception' in result:
                    raise UserError(_('Moodle API Error: %s') % result['message'])
                else:
                    record.state = 'posted' if state == 'active' else 'inactive'
            else:
                raise UserError(_('Error connecting to Moodle API: %s') % response.text)

    def enroll_student_in_course(self, course_id):
        for record in self:
            # if record.state != 'posted':
            #     raise UserError(_('Only posted students can be enrolled in a course.'))

            url = record.config_id.url
            token = record.config_id.token
            payload = {
                'moodlewsrestformat': 'json',
                'wstoken': token,
                'wsfunction': 'enrol_manual_enrol_users',
                'enrolments[0][roleid]': 5,  # Typically 5 for student role
                'enrolments[0][userid]': record.idnumber,
                'enrolments[0][courseid]': course_id,
            }
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                result = response.json()
                if result and 'exception' in result:
                    raise UserError(_('Moodle API Error: %s') % result['message'])
                # else:
                #     record.message_post(body=_('Student enrolled in course with ID %s') % course_id)
            else:
                raise UserError(_('Error connecting to Moodle API: %s') % response.text)

    def increment_function(self):
        self.attendance_increment = self.attendance_increment + 1
        return {
            'type': 'ir.actions.client',
            'tag': 'soft_reload',
            'context': int(self.attendance_increment)
        }


class MoodleStudentEnrollWizard(models.TransientModel):
    _name = 'moodle.student.enroll.wizard'
    _description = 'Enroll Moodle Student in Course'

    course_id = fields.Many2one('moodle.course', string='Course', required=True)
    student_id = fields.Many2one('moodle.student', string='Student', required=True)

    def enroll_student(self):
        student = self.student_id
        return student.enroll_student_in_course(self.course_id.idnumber)
