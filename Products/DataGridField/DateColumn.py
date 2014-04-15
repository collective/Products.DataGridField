# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from Products.DataGridField.Column import Column

import time

DATE_FORMAT = '%m/%d/%y'


class DateColumn(Column):
    security = ClassSecurityInfo()

    def __init__(self, label, **kwargs):
        Column.__init__(self, label, **kwargs)

    security.declarePublic('getMacro')

    def getMacro(self):
        """ Return macro used to render this column in view/edit """
        return "datagrid_date_cell"

    def datestr(self, context, date):
        """Return formatted date string from a given DateTime instance.
        """
        if date and hasattr(date, 'strftime'):
            return date.strftime(DATE_FORMAT)
        elif date:
            # Maybe a string or other bad value
            return date
        else:
            return ''

    def processCellData(self, form, value, context, field, columnId):
        """ Read cell values from raw form data
        """
        newValue = []
        for row in value:
            newRow = {}
            for key in row.keys():
                newRow[key] = row[key]
                datestr = row[columnId]
                if datestr:
                    try:
                        tp = time.strptime(datestr, DATE_FORMAT)
                    except ValueError:
                        tp = ''
                    newRow[columnId] = ((tp and DateTime(time.mktime(tp)))
                                        or row[columnId])
            newValue.append(newRow)
        return newValue
