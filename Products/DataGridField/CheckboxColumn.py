"""

    Checkbox column

    Copyright 2006, 2007 Radim Novotny

    Licensed under GPL.

"""

from __future__ import nested_scopes
__author__ = "Radim Novotny"
__docformat__ = 'epytext'

from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.DataGridField.Column import Column

class CheckboxColumn(Column):
    """ Allow user select one from on/off options using check buttons.

    Implementation based on RadioColumn.
    """
    security = ClassSecurityInfo()

    security.declarePublic('getMacro')
    def getMacro(self):
        """ Return macro used to render this column in view/edit """
        return "datagrid_checkbox_cell"


# Initializes class security
InitializeClass(CheckboxColumn)
