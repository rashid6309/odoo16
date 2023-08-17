from odoo import models, fields, api
from odoo.exceptions import UserError

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember

from logging import getLogger
_logger = getLogger(__name__)


class SinglePatient(models.Model):
    _name = "ec.individual.patient"

    key = fields.Selection(selection=StaticMember.GENDER_1,
                           required=True,)

    name = fields.Char(string="Name")

    patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                 required=True,
                                 index=True,
                                 string="Patient")


    @api.model
    def create_individuals(self, patient_id):
        """

        :param patient_id: Couple ID
        :return: Creates the male and female patient individual and return that in tuple.
        """
        self.ensure_one()

        if not patient_id:
            _logger.warning("To create individuals patient id is must......")
            raise UserError("Patient is required.")

        # [Female, Male]
        values = [{
            'patient_id': patient_id.id,
            'key': 'female',
            'name': patient_id.wife_name
        }, {
            'patient_id': patient_id.id,
            'key': 'male',
            'name': patient_id.husband_name
        }]

        self.create(values)

        return self.get_individuals(patient_id)

    @api.model
    def get_individuals(self, patient_id):
        """

        :param patient_id: Couple ID
        :return: female_patient ID, Male Patient ID
        """
        self.ensure_one()

        records = self.search(domain=[('patient_id', '=', patient_id.id)])
        female_patient = next( (item for item in records if item.key == 'female'), None)
        male_patient = next( (item for item in records if item.key == 'male'), None)

        if not female_patient and not male_patient:
            _logger.warning("Female or Male id not found. Please fix.....")
            raise UserError("Female or Male id not found. Please contact administrator.")

        return female_patient, male_patient

