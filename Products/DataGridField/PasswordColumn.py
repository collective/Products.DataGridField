"""

    Password column for DataGridField.

"""

__author__ = "T. Kim Nguyen <nguyen@uwosh.edu>"
__docformat__ = 'plaintext'

# Zope imports
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.DataGridField.Column import Column


class PasswordColumn(Column):
    """ Password column """

    security = ClassSecurityInfo()

    security.declarePublic('getMacro')
    def getMacro(self):
        """ Return macro used to render this column in view/edit """
        return "datagrid_password_cell"


# Initializes class security
InitializeClass(PasswordColumn)
