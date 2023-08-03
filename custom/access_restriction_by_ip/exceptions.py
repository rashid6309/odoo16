
from odoo.exceptions import UserError


class IpAllowedDenied(UserError):
    def __init__(self, message="IP not allowed"):
        super().__init__(message)
        self.with_traceback(None)
        self.__cause__ = None
        self.traceback = ('', '', '')