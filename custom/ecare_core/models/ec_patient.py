from odoo import models, api, fields, _
from odoo.exceptions import AccessError, UserError

import datetime
import requests, json

from logging import getLogger

_logger = getLogger(__name__)


class EcarePatient(models.Model):
    _name = "ec.medical.patient"
    _description = "Patient"

    _inherits = {
        'res.partner': 'partner_id',
    }
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _order = "write_date desc, id desc"
    _rec_name = "name"
    _rec_names_search = ['name', 'mr_num', 'mobile_wife', 'mobile_husband', 'preferred_mobile', 'wife_nic', 'husband_nic']

    # Legacy system fields
    legacy_wife_id = fields.Integer()
    legacy_husband_id = fields.Integer()
    # -- End here.

    partner_id = fields.Many2one(comodel_name="res.partner",
                                 required=True,
                                 ondelete="cascade")

    mr_num = fields.Char('MR No.', index="btree_not_null")
    wife_name = fields.Char('WIFE',
                            tracking=True)

    husband_name = fields.Char('HUSBAND',
                               tracking=True)

    wife_nic = fields.Char(size=15,
                           string='CNIC',
                           tracking=True)

    wife_passport = fields.Char(string="PASSPORT",
                                tracking=True)

    wife_driving_license = fields.Char(string="Driving License",
                                       tracking=True)

    husband_nic = fields.Char(size=15,
                              string='CNIC',
                              tracking=True)

    wife_dob = fields.Date(string='DATE OF BIRTH')
    husband_dob = fields.Date(string='DATE OF BIRTH')
    wife_age = fields.Char(string='Age', compute='_get_age_wife')
    husband_age = fields.Char(string='Age', compute='_get_age_husband')

    husband_passport = fields.Char(string="PASSPORT",
                                   tracking=True)

    husband_driving_license = fields.Char(string="Driving License",
                                          tracking=True)

    phone_res_wife = fields.Char(string='Phone (Res)',
                                 size=14,
                                 tracking=True)
    phone_ofc_wife = fields.Char(string='Phone (Office)',
                                 size=14,
                                 tracking=True)

    mobile_wife = fields.Char(string='MOBILE',
                              size=14,
                              tracking=True)

    phone_res_husband = fields.Char(string='Phone (Res)',
                                    size=14,
                                    tracking=True)
    phone_ofc_husband = fields.Char(string='Phone (Office)',
                                    size=14,
                                    tracking=True)
    mobile_husband = fields.Char(string='MOBILE',
                                 size=14,
                                 tracking=True)

    email_wife = fields.Char(string="Email")
    email_husband = fields.Char(string="Email")

    preferred_mobile = fields.Char(string='Preferred Mobile No.',
                                   size=14,
                                   tracking=True)

    MARITAL_STATUS = [
        ('Unmarried', 'Unmarried'),
        ('Married', 'Married'),
        ('Widowed', 'Widowed'),
        ('Divorced', 'Divorced'),
        ('Separated', 'Separated'),
    ]

    # To be used for wife
    marital_status = fields.Selection(selection=MARITAL_STATUS,
                                      string='MARITAL STATUS',
                                      required=False,
                                      tracking=True,
                                      default="Married")

    # To be used for Husband
    husband_marital_status = fields.Selection(selection=MARITAL_STATUS,
                                      string='MARITAL STATUS',
                                      required=False,
                                      tracking=True,
                                      default="Married")

    married_since = fields.Date(string="Married Since")
    yom = fields.Char('Years of Marriage', compute='get_marriage_years')

    # Father Details
    father_name = fields.Char(string="Father Name",
                              tracking=True)

    father_nic = fields.Char(size=15,
                             tracking=True,
                             string='Father\'s CNIC')

    mobile_number = fields.Char(string="Mobile (Mother)",
                                tracking=True)

    mother_name = fields.Char(string="Mother Name", tracking=True)

    # Next of kin details
    emer_contact_name = fields.Char(string="Contact Name")
    emer_contact_addr = fields.Char(string='Address')
    emer_contact_relation = fields.Selection(string='Relation',
                                             selection=[('m', 'Mother'),('f', 'Father'),
                                                        ('s', 'Sibling'), ('fr', 'Friend'),
                                                        ('u', 'Uncle'), ('a', 'Aunt'),
                                                        ('c', 'Children'),('N/A','N/A')])
    emer_contact_nic = fields.Char(size=15, string="Emergency CNIC",
                                   tracking=True)

    # Tracking is not applicable on Binary fields so don't waste your time in future as well.
    husband_image = fields.Binary(string='Husband Image',
                                  help="This field holds an attachment.")

    _sql_constraints = [
        ('wife_cnic_uniq', 'unique(wife_nic)', 'The wife cnic must be unique !'),
        ('husband_cnic_uniq', 'unique(husband_nic)', 'The husband must be unique !'),
    ]

    def update_write_date(self):
        """ This method is called to update the write_date so that patients gets in the view at first """
        self.write_date = datetime.datetime.now()

    def write(self, vals):
        """
        First time creation is allowed afterwards chnage is not.

        False means key is found but no value
        None means key is not found

        Algo:
        If in self the value of husband and wife is empty let it update.
        Otherwise stop it.
        :param vals:
        :return:
        """
        husband_image = vals.get("husband_image")
        wife_image = vals.get("image_1920")
        admin_user = self.env.user.has_group("ecare_appointment.group_appointment_super_administrator")

        if wife_image != None: # Key found in the vals
            if not self.image_1920 and wife_image:
                # GO AHEAD Don't check anything.
                pass
            elif self.image_1920 and wife_image == False and not admin_user: # Means deletion check for admin
                raise AccessError("Only Administrator can edit/delete photo ids.")
            elif self.image_1920 and wife_image != self.image_1920 and not admin_user and wife_image != None: # Means deleting and uploading new.
                raise AccessError("Only Administrator can edit/delete photo ids.")

        if husband_image != None: # key found in the vals
            if not self.husband_image and husband_image:
                # GO AHEAD Don't check anything.
                pass
            elif self.husband_image and husband_image == False and not admin_user: # Means deletion check for admin
                raise AccessError("Only Administrator can edit/delete photo ids.")
            elif self.husband_image and husband_image != self.husband_image and not admin_user:
                raise AccessError("Only Administrator can edit/delete photo ids.")

        return super(EcarePatient, self).write(vals)


    @api.depends('wife_dob')
    @api.onchange('wife_dob')
    def _get_age_wife(self):
        for rec in self:
            if rec.wife_dob:
                bdate = datetime.datetime.strptime(str(rec.wife_dob), "%Y-%m-%d").date()
                today = datetime.date.today()
                diffdate = today - bdate
                years = diffdate.days / 365
                formonth = diffdate.days - (int(years) * 365.25)
                months = (formonth / 31)
                bday = bdate.day
                tody = datetime.date.today().day
                if tody >= bday:
                    day = tody - bday
                else:
                    day = 31 - (bday - tody)
                if int(years) < 5:
                    rec.wife_age = str(int(years)) + 'Y ' + str(int(months)) + 'M ' + str(day) + 'D'
                else:
                    rec.wife_age = str(int(years)) + ' Years'
            else:
                rec.wife_age = ''

    @api.depends('husband_dob')
    @api.onchange('husband_dob')
    def _get_age_husband(self):
        for rec in self:
            if rec.husband_dob:
                bdate = datetime.datetime.strptime(str(rec.husband_dob), "%Y-%m-%d").date()
                today = datetime.date.today()
                diffdate = today - bdate
                years = diffdate.days / 365
                formonth = diffdate.days - (int(years) * 365.25)
                months = (formonth / 31)
                bday = bdate.day
                tody = datetime.date.today().day
                if tody >= bday:
                    day = tody - bday
                else:
                    day = 31 - (bday - tody)
                if int(years) < 5:
                    rec.husband_age = str(int(years)) + 'Y ' + str(int(months)) + 'M ' + str(day) + 'D'
                else:
                    rec.husband_age = str(int(years)) + ' Years'
            else:
                rec.husband_age = ''

    @api.depends('married_since')
    @api.onchange('married_since')
    def get_marriage_years(self):
        for patient in self:
            if patient.married_since:
                today = datetime.date.today()
                mdate = datetime.datetime.strptime(str(patient.married_since), "%Y-%m-%d").date()
                if mdate > today:
                    patient.dob = today
                    return {

                        'warning': {

                            'title': 'Warning!',

                            'message': 'Date of Marriage should be lesser than or equal to today.'}

                    }
                diffdate = today - mdate
                years = diffdate.days / 365
                formonth = diffdate.days - (int(years) * 365.25)
                months = (formonth / 31)
                bday = mdate.day
                tody = datetime.date.today().day
                if tody >= bday:
                    day = tody - bday
                else:
                    day = 31 - (bday - tody)
                patient.yom = str(int(years)) + 'Y ' + str(int(months)) + 'M ' + str(day) + 'D'
            else:
                patient.yom = ''

    @api.onchange('husband_name', 'wife_name', 'mr_num')
    def _get_patient_name(self):
        for patient in self:
            if patient.wife_name and not patient.husband_name:
                patient_name = patient.wife_name
            elif patient.husband_name and not patient.wife_name:
                patient_name = patient.husband_name
            elif patient.husband_name and patient.wife_name:
                patient_name = str(patient.wife_name + ' W/O ' + patient.husband_name)
            else:
                patient_name = ''

            patient_name = self.get_patient_name_with_mr(patient_name)

            if patient.name != patient_name: # Then call write
                patient.name = patient_name
                patient.display_name = patient_name

    def action_open_patient_slots(self):
        appointments = self.env['ec.booked.slot.record'].search([
            ('partner_id', '=', self.id),
        ])
        if not appointments:
            raise AccessError("No Appointments exist.")

        return {
            "name": _("Booked Appointments"),
            "type": 'ir.actions.act_window',
            "res_model": 'ec.booked.slot.record',
            'view_mode': 'tree,form',
            "target": 'current',
            'domain': [('partner_id', '=', self.id)]
        }

    def action_open_patient_invoices(self):
        if not self.mr_num:
            raise UserError("Please generate MR No.")

        partner_id = self.partner_id
        context = self._context.copy()
        context.update({
            'default_partner_id': partner_id.id,
            'default_move_type': 'out_invoice'
        })
        tree_view_id = self.env.ref('account.view_out_invoice_tree')
        form_view_id = self.env.ref('account.view_move_form')
        return {
            "name": _("Invoices"),
            "type": 'ir.actions.act_window',
            "res_model": 'account.move',
            'view_mode': 'tree,form',
            'views': [(tree_view_id.id, 'tree'), (form_view_id.id, 'form')],
            "target": 'current',
            "context": context,
            'domain': [('partner_id', '=', partner_id.id),
                       ('move_type', 'in', ['out_refund', 'out_invoice'])
                     ]
        }

    def get_patient_name_with_mr(self, patient_name=False):
        patient_name = patient_name or self.name
        if self.mr_num:
            patient_name = self.mr_num + " - " + patient_name

        return patient_name

    def action_register(self):
        self.ensure_one()
        self.constraints_validation()
        self.mr_num = self.env['ir.sequence'].next_by_code('ecare_core.patient.sequence.mr.no') or _('New')
        patient_name = self.get_patient_name_with_mr()
        # have to do it manually otherwise it was throwing error now due to rec_name update.
        self.partner_id.display_name = patient_name
        self.partner_id.name = patient_name

        # POST API to update the data at that side ICSI existing history software

        self.post_data_history_software()

    def constraints_validation(self):
        if self.husband_marital_status != 'Unmarried':
            if not ((self.wife_nic or self.wife_passport) and self.wife_dob and self.mobile_wife and self.married_since):
                raise models.ValidationError(" Wife cnic or passport, dob, mobile, martial status and married since are mandatory")

        if self.marital_status != 'Unmarried':
            if not ((self.husband_nic or self.husband_passport) and self.husband_dob and self.mobile_husband):
                raise models.ValidationError(" Husband cnic, dob , mobile, martial status are mandatory")

    def get_payload(self):
        yom = None
        if self.yom:
            yom = int(self.yom[:self.yom.index('Y')])

        payload = {
            "Female": {
                "Patient_id": 0,
                "First_name": self.wife_name,
                "Surname": "",
                "Address_line1": self.street or "",
                "Address_line2": self.street2 or "",
                "Address_line3": "",
                "City": self.city or "",
                "Postal_code": self.zip or "",
                "Country": self.country_id.name if self.country_id else "",
                "Mobile_no": self.mobile_wife or "",
                "Email": self.email_wife or "",
                "Phone_residence": self.phone_res_wife or "",
                "Phone_office": self.phone_ofc_wife or "",
                "Day_of_birth": self.wife_dob.day if self.wife_dob else "",
                "Month_of_birth": self.wife_dob.month if self.wife_dob else "",
                "Year_of_birth": self.wife_dob.year if self.wife_dob else "",
                "Office_country": "",
                "Mobile_country": ""
            },
            "Male": {
                "Patient_id": 0,
                "First_name": self.husband_name,
                "Surname": "",
                "Address_line1": self.street or "",
                "Address_line2": self.street2 or "",
                "Address_line3": "",
                "City": self.city or "",
                "Postal_code": self.zip or "",
                "Country": self.country_id.name if self.country_id else "",
                "Mobile_no": self.mobile_husband or "",
                "Email": self.email_husband or "",
                "Phone_residence": self.phone_res_husband or "",
                "Phone_office": self.phone_ofc_husband or "",
                "Day_of_birth": self.husband_dob.day if self.husband_dob else "",
                "Month_of_birth": self.husband_dob.month if self.husband_dob else "",
                "Year_of_birth": self.husband_dob.year if self.husband_dob else "",
                "Office_country": "",
                "Mobile_country": ""
            },
            "Couple": {
                "Couple_id": self.mr_num,
                "Marriage_period": yom,
                "Couple_Detail": "",
                "Couple_Address": "",
                "Informed_by": "",
                "Reffered_by": ""
            }
        }
        return payload
    
    def post_data_history_software(self):
        history_software_ip = self.env['ir.config_parameter'].sudo().get_param('ecare_core.icsi.history.software.ip')
        if not history_software_ip:
            raise UserError("History Software Ip is not unavailable. Please contact administrator.")

        history_software_ip = history_software_ip.strip()
        url = f"http://{history_software_ip}:8080/Registration/PostCouple"

        header = {
            'Authorization': 'jq2hCPjOSo/U2vql6WKJ/lVXsmJ4s90K',
            'Content-Type': 'application/json'
        }

        payload = self.get_payload()

        payload = json.dumps(payload) # Make JSON
        try:
            r = requests.post(url=url, data=payload, headers=header)
        except Exception as e:
            _logger.warning(e)
            raise UserError("System is unable to connect with history software. Please contact administrator.")

        if r.status_code != 200:
            _logger.warning("Failure in adding patient  in the icsi history software...")
            _logger.warning(r.content)
        else:
            _logger.info("Patient added in the icsi history software...")
            _logger.info(r.content)
        # Add line in the third party api log
        try:
            api_log_values = {
            'name': 'ICSI History Software: Patient Creation',
            'url': url,
            'payload': payload,
            'response': "Status: " + str(r.status_code) + " " + str(r.content)
            }
            # use this otherwise give rights in the csv
            self.env['third.party.api.log'].sudo().create(api_log_values)
        except Exception as e:
            _logger.warning(e)

    def action_patient_profile_print_report(self):
        self.ensure_one()
        [datas] = self.read()
        return self.env.ref('ecare_reporting.ec_patient_profile_report').report_action(self, data=datas)

