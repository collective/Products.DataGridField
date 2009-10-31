"""

    Lines column - used for list of values

    Licensed under GPL.

"""

from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.DataGridField.Column import Column


class LinesColumn(Column):
    """ Textarea which returns list of lines

    Used eg. as vocabulary definition in PFGDataGrid
    """
    security = ClassSecurityInfo()

    security.declarePublic('getMacro')
    def getMacro(self):
        """ Return macro used to render this column in view/edit """
        return "datagrid_lines_cell"

    security.declarePublic('processCellData')
    def processCellData(self, form, value, context, field, columnId):
        """ Read cell values from raw form data

        Column processing in forms may need special preparations for data if
        widgets use other than <input value> for storing their
        values in fields.

        @param form Submitted form, contains HTML fields
        @param context Archetypes item instance for the submitted form
        @param field Assigned field for this widget
        @param columnId Column what we are operating

        @return new values which are constructed by processing data
        """
        # scan all rows and build list of lines for fields
        newValue = []
        for row in value:

            # we must clone row since
            # row is readonly ZPublished.HTTPRequest.record object
            newRow = {}
            for key in row.keys():
                newRow[key] = row[key]

            # make list of values splited by \n with each item stripped
            newRow[columnId] = [
                v.strip() for v in newRow[columnId].split('\n')]
            # last item should not be empty
            if newRow[columnId] and newRow[columnId][-1] == '':
                newRow[columnId] = newRow[columnId][:-1]
            newValue.append(newRow)

        return newValue

# Initializes class security
InitializeClass(LinesColumn)
