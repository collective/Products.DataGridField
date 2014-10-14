"""

    Month column for DataGridField.

"""

__author__ = "T. Kim Nguyen <nguyen@uwosh.edu>"
__docformat__ = 'plaintext'

# Zope imports
from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.DataGridField.Column import Column


class MonthColumn(Column):
    """ Month column """

    security = ClassSecurityInfo()

    security.declarePublic('getMacro')
    def getMacro(self):
        """ Return macro used to render this column in view/edit """
        return "datagrid_month_cell"


# Initializes class security
InitializeClass(MonthColumn)
