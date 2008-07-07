# Zope imports
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.DataGridField.Column import Column

class TextAreaColumn(Column):
    """
    """

    security = ClassSecurityInfo()

    security.declarePublic('getMacro')
    def getMacro(self):
        """ Return macro used to render this column in view/edit """
        return "datagrid_textarea_cell"
    
# Initializes class security
InitializeClass(TextAreaColumn)
