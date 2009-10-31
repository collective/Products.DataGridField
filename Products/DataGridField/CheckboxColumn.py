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

    WARNING - Please note, the current implementation does not work when
    some field on the form raises validation error. In this case all checkboxes
    are cleared. Do not use CheckboxColumn if your form has some required fields
    or validators active.

    There are no on/off values. Widget view displays HTML character with code
    &#10004; (checkmark) or -
    """
    security = ClassSecurityInfo()

    security.declarePublic('getMacro')
    def getMacro(self):
        """ Return macro used to render this column in view/edit """
        return "datagrid_checkbox_cell"

    security.declarePublic('processCellData')
    def processCellData(self, form, value, context, field, columnId):
        """ Read cell values from raw form data
        """

        newValue = []

        for row in value:

            # we must clone row since
            # row is readonly ZPublished.HTTPRequest.record object
            newRow = {}
            for key in row.keys():
                newRow[key] = row[key]

            orderIndex = row["orderindex_"]
            cellId = "%s.%s.%s" % (field.getName(), columnId, orderIndex)
            if form.has_key(cellId):
                # If check button is set in HTML form
                # it's id appears in form of field.column.orderIndex
                # field value is hardcoded to '1'
                newRow[columnId] = form[cellId]
            else:
                # if item is not in form, user did not check it.
                newRow[columnId] = ''

            newValue.append(newRow)

        return newValue




# Initializes class security
InitializeClass(CheckboxColumn)
