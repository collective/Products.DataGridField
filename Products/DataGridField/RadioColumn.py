"""

    Radio button column

    Copyright 2006 Red Innovation

    Licensed under GPL.

"""

from __future__ import nested_scopes
__author__ = "Mikko Ohtamaa <mikko@redinnovation.com>"
__docformat__ = 'reStructuredText'

from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.DataGridField.SelectColumn import SelectColumn


class RadioColumn(SelectColumn):
    """ Allow user select one from many options using radio buttons.

    WARNING: Does not work with validation. All field values will be cleared
    when validation fails on the edit page submit. This is a limitation in
    the current architecture (Archetypes / ZPublisher / DataGridField).

    Some explanation hints:

    In::
        <input type="radio" name=""
    name must be unique among radio button group.

    This is problematic. ZPublisher cannot associate radio buttons to :records
    groups since :records groups are formed as::

        name string:${fieldName}.${column}:records;

    ZPublisher's :records naming convention doesn't allow different per row
    radio button groups. Instead, we assign an unique name for reach
    radio button cell using::

        name string:${fieldName}.${column}.${repeat/rows/number};

    Column.processCellData parses form data and propeply combines
    field value from radio buttons so that Archetypes' field framework
    correctly understand the set value.

    """
    security = ClassSecurityInfo()

    security.declarePublic('getMacro')
    def getMacro(self):
        """ Return macro used to render this column in view/edit """
        return "datagrid_radio_cell"

    security.declarePublic('processCellData')
    def processCellData(self, form, value, context, field, columnId):
        """ Read cell values from raw form data

        Read special table for radio button columns from form data.
        The selected radio button cell id is placed as a cell value.
        """

        newValue = []

        #print "form value:" + str(form)

        for row in value:

            # we must clone row since
            # row is readonly ZPublished.HTTPRequest.record object
            newRow = {}
            for key in row.keys():
                newRow[key] = row[key]

            orderIndex = row["orderindex_"]
            cellId = "%s.%s.%s" % (field.getName(), columnId, orderIndex)
            if form.has_key(cellId):
                # If radio button is set in HTML form
                # it's id appears in form of field.column.orderIndex
                newRow[columnId] = form[cellId]

            newValue.append(newRow)

        return newValue




# Initializes class security
InitializeClass(RadioColumn)
