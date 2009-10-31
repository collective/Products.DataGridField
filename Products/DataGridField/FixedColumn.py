"""

    Fixed text column

    Copyright 2006 Red Innovation

    Licensed under GPL.

"""

from __future__ import nested_scopes
__author__ = "Mikko Ohtamaa <mikko@redinnovation.com>"
__docformat__ = 'reStructuredText'

from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.DataGridField.Column import Column

class FixedColumn(Column):
    """ Column with non-changeable text

    Useful with DataGridField.fixed_row property in some use cases.
    """
    security = ClassSecurityInfo()

    def __init__(self, label, default=None, label_msgid=None, visible=True):
        """ Create a column

            @param hide Hide column from displaying
        """
        Column.__init__(self, label, default, label_msgid)
        self.visible = visible

    security.declarePublic('getMacro')
    def getMacro(self):
        """ Return macro used to render this column in view/edit """
        return "datagrid_fixed_cell"


# Initializes class security
InitializeClass(FixedColumn)
