import datetime

from odoo.exceptions import AccessError


class EditingRights:

    @staticmethod
    def check_model_edit_rights(self, model_name, timedate):
        groups_list = ['Physician']  # This is to handle multiple groups in the system
        if self.env.user.has_group('ecare.group_ec_medical_allow_editing'):
            return True
        else:
            model_groups_access = self.env['access.limit.model'].search(args=[('models', '=', model_name)],
                                                                        order="hours desc", limit=1)
            today = datetime.datetime.now()
            diff = ''
            for group in groups_list:
                group_id = self.env['res.groups'].search([('name', '=', group)], limit=1).id
                model_groups_access.search(args=[('group', '=', group_id)])
                if model_groups_access:
                    if timedate:
                        diff = today - timedate
                        hours = divmod(diff.total_seconds(), 3600)[0]
                        if hours > model_groups_access.hours:
                            return True
                        else:
                            raise AccessError(
                                'Can not update as creation time exceeds %shrs.\nEditing limit: %shrs') % (
                                      hours, model_groups_access.hours)
                else:
                    return True

        # access = http.request.env['access.limit'].search([])
        # group = http.request.env['res.groups'].search([('name', '=', 'Physician')], limit=1).id
        # access_limit_for_group = http.request.env['access.limit'].search([('groups', '=', group)], limit=1)
        # if http.request.env.user.has_group('ecare.group_ec_medical_physician'):
        #     if timedate:
        #         diff = today - timedate
        #         hours = divmod(diff.total_seconds(), 3600)[0]
        #         if hours > access_limit_for_group.hours:
        #             if http.request.env.user.has_group('ecare.group_ec_medical_allow_editing'):
        #                 return True
        #             else:
        #                 raise AccessError('Can not update as creation time exceeds %shrs.\nEditing limit: %shrs') % (
        #                         hours, access_limit_for_group.hours)
        #         else:
        #             return True
        # else:
        #     raise AccessError('Kindly assign Physician or Healthcare center role to the user')
